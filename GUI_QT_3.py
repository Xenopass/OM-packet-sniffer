
import threading
import sys

import struct
import msgpack
import pandas as pd
from PySide6.QtCore import QThread, Signal, QObject, QModelIndex, QAbstractTableModel
from PySide6.QtGui import QIcon, QTextCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidget, QTableWidgetItem
import ui_OM_Sniffer as ui
from tools_string import find_sects, find_and_fuse_duel_dicts, get_sect_members, normalize_utf8, save_list_csv
from tree_code import tree_model
from scapy.all import sniff, TCP, IP
from Pandas_shenanigans import sect_duels_data
from matchmaking import matchmaking_from_DF
from interface_code import get_interface_for_port


# -----------------------------
# Console emitter
# -----------------------------
class EmittingStream(QObject):
    text_written = Signal(str)

    def write(self, text):
        if text:
            self.text_written.emit(str(text))

    def flush(self):
        pass

# -----------------------------
# Sniffer that runs in background
# -----------------------------

class SnifferWorker(QObject):
    payload_sent = Signal(bytes)
    finished = Signal()

    def __init__(self, stop_event, interface=None):
        super().__init__()
        self.interface = interface
        self.stop_event = stop_event

    # @Slot()
    def run(self):
        """Start sniffing. Runs in a separate thread."""
        print("Sniffer started")

        def handle_packet(pkt):
            # Only process TCP packets on port 8583
            if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
                return
            tcp = pkt[TCP]
            if tcp.sport != 8583 or not tcp.payload:
                return

            payload_bytes = bytes(tcp.payload)
            self.payload_sent.emit(payload_bytes)

        if self.interface is None:
            self.interface = get_interface_for_port(8583)

        sniff(
            iface = self.interface,
            prn=handle_packet,
            filter="tcp src port 8583 ",
            store=False,
            stop_filter=lambda _: self.stop_event.is_set()
        )

        print("Sniffer stopped")
        self.finished.emit()

    # @Slot()
    def stop(self):
        """Set the flag so sniffing will stop."""
        self.stop_event.set()

# -----------------------------
# Msgpack unpacker + processing
# -----------------------------

class RobustMsgPackDecoder:
    def __init__(self):
        self.buffer = bytearray()
        self.unpacker = msgpack.Unpacker(
            raw=True,
            strict_map_key=False,  # allows non-string keys
            use_list=True
        )

    def feed(self, data: bytes):
        self.buffer.extend(data)
        self.unpacker.feed(self.buffer)

        results = []
        consumed = 0

        try:
            for obj in self.unpacker:
                results.append(obj)
                consumed = self.unpacker.tell()
        except Exception as e:
            # Catch any unpacking error
            print("⚠️ MsgPack decoding error:", e)
            print("Buffer causing error (hex):", self.buffer.hex())
            consumed = len(self.buffer)  # skip entire buffer to prevent infinite loop

        if consumed:
            del self.buffer[:consumed]

        return results

# -----------------------------
# payload splitter
# -----------------------------

class PacketSplitter:
    def __init__(self):
        self.buffer = bytearray()
        self.MAGIC = b"\x5A\x4D"
        self.HEADER_SIZE = 10  # 2 magic + 4 flags + 4 length
        self.MAX_PAYLOAD = 1_000_000 #sanity check

    def feed(self, data: bytes):
        """
        Feed raw bytes, return a list of raw payloads (bytes)
        """
        self.buffer.extend(data)
        payloads = []

        while True:
            # 1) find magic
            pos = self.buffer.find(self.MAGIC)
            if pos == -1:
                # keep only last byte in case 'Z' is split
                self.buffer[:] = self.buffer[-1:]
                break

            if pos > 0:
                del self.buffer[:pos]

            # 2) wait for full header
            if len(self.buffer) < self.HEADER_SIZE:
                break

            # 3) read length (uint16 BE)
            payload_len = struct.unpack(">L", self.buffer[6:10])[0]


            if payload_len <= 0 or payload_len > self.MAX_PAYLOAD:
                print("crazy, I was crazy once\n")
                # invalid header → resync
                del self.buffer[:2]
                continue

            total_len = self.HEADER_SIZE + payload_len

            # 4) wait for full frame
            if len(self.buffer) < total_len:
                break

            # 5) extract payload only
            payload = bytes(self.buffer[self.HEADER_SIZE:total_len])
            payloads.append(payload)

            # 6) consume frame
            del self.buffer[:total_len]

        return payloads

# -----------------------------
# table from CSV
# -----------------------------

class CustomTableModel(QTableWidget):

    def __init__(self, data: pd.DataFrame=None):
        QAbstractTableModel.__init__(self)
        self.dataframe = data

    def setTable(self, data):
        self.setColumnCount(self.dataframe.shape[0])
        self.setRowCount(self.dataframe.shape[1])

        for i in range(1,self.dataframe.shape[0]):
            for j in range(self.dataframe.shape[1]):
                item = QTableWidgetItem(self.dataframe[i,j])
                self.setItem(i, j, item)



# -----------------------------
# Main window
# -----------------------------

class MainWindow(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Oh My Sniff")
        self.setWindowIcon(QIcon('OMS_Icon.png'))

        #variables
        self.payload = bytearray()
        self.dataframed_data = pd.DataFrame()
        self.dataframed_sects = dict()
        self.objects =list()
        self.dict_of_objects = dict()

        self.check_options = [self.CheckB_search_Sects , self.CheckB_search_duel, self.CheckB_search_Demonbend]

        self.decoder = RobustMsgPackDecoder()

        # Thread-safe stop flag
        self.stop_event = threading.Event()

        # Worker + thread
        self.sniffer = SnifferWorker(self.stop_event)
        self.sniff_thread = QThread()
        self.sniffer.moveToThread(self.sniff_thread)
        self.sniff_thread.started.connect(self.sniffer.run)
        self.sniffer.finished.connect(self.sniff_thread.quit)
        self.sniffer.finished.connect(lambda: print("Thread finished"))

        # Connect signals
        self.btn_start_sniff.clicked.connect(self.start_sniffing)
        self.btn_finish_sniff.clicked.connect(self.stop_sniffing)
        self.btn_process_data.clicked.connect(self.process_packets)
        self.sniffer.payload_sent.connect(self.handle_payload)
        self.ComboB_Object_selector.currentTextChanged.connect(self.combo_text_changed)
        self.Btn_Matchmaking.clicked.connect(self.Matchmaking_function)

        # Create stream
        self.stdout_stream = EmittingStream()
        self.stdout_stream.text_written.connect(self.normal_output_written)

        self.stderr_stream = EmittingStream()
        self.stderr_stream.text_written.connect(self.normal_output_written)

        sys.stdout = self.stdout_stream
        sys.stderr = self.stderr_stream

    ###---------------------------------------
    ###Matchmaking Functions
    ###---------------------------------------

    def Matchmaking_function(self):
        name_firstSect = self.Combo_First_sect_selector.currentText()
        name_secondSect = self.Combo_Second_sect_selector.currentText()

        self.matchmaking_dataframe = matchmaking_from_DF(name_firstSect, name_secondSect)

        options = {'display.max_rows': None,
                   'display.max_columns': None,
                   'display.max_colwidth': None}

        for option, value in options.items():
            pd.set_option(option, value)

        print(self.matchmaking_dataframe)

        rows, cols = self.matchmaking_dataframe.shape

        self.Table_matchmaking.setRowCount(rows)
        self.Table_matchmaking.setColumnCount(cols)

        self.Table_matchmaking.setHorizontalHeaderLabels(
            [str(col) for col in self.matchmaking_dataframe.columns]
        )
        self.Table_matchmaking.verticalHeader().setVisible(False)

        for i in range(rows):
            for j in range(cols):
                value = self.matchmaking_dataframe.iloc[i, j]
                # print(value)

                item = QTableWidgetItem(str(value))
                self.Table_matchmaking.setItem(i, j, item)
        self.Table_matchmaking.resizeColumnsToContents()


    ###---------------------------------------
    ###Console Functions
    ###---------------------------------------

    def normal_output_written(self, text):
        self.Txt_Console_output.moveCursor(QTextCursor.MoveOperation.End)
        self.Txt_Console_output.insertPlainText(text)
        self.Txt_Console_output.ensureCursorVisible()

    ###---------------------------------------
    ###Tree Functions
    ###---------------------------------------

    def combo_text_changed(self, i):
        tree_model(self,self.dict_of_objects[i])

    ###---------------------------------------
    ###Sniffing Functions
    ###---------------------------------------

    def start_sniffing(self):
        # Reset stop flag
        self.stop_event.clear()
        self.sniff_thread.start()
        print("Thread started")

    def stop_sniffing(self):
        self.sniffer.stop()  # sets the stop_event
        print("Stop requested")

    ###---------------------------------------
    ###Processing Packets Function
    ###---------------------------------------

    def handle_payload(self, payload_r):
        print("Got packet:", payload_r[:10])  # or do whatever with it
        self.payload += payload_r

    def process_packets(self):

        if not any(cb.isChecked() for cb in self.check_options):
            QMessageBox.warning(
                self,
                "Missing selection",
                "Please select at least one option before starting."
            )
            return
        print("processing packets")
        payload_splitter = PacketSplitter()
        # payload_packs = self.payload.split(sep="5a4d000000000000")
        payload_packs=payload_splitter.feed(bytes(self.payload))
        payload_packs_binary = [ s for s in payload_packs if len(s) > 1000]
        print(f"found {len(payload_packs)} payloads packs correctly formatted")
        print(f"found {len(payload_packs_binary)} payloads with long enough binary payloads")

        for payload_part in payload_packs_binary:

            decoded_payload_part = self.decoder.feed(payload_part)
            # print(f'raw decode payload: {decoded_payload_part}')
            # print(payload_part, "\n")
            if len(decoded_payload_part) > 0:
                normalized_payload_part = normalize_utf8(decoded_payload_part)
                self.objects.append(normalized_payload_part)
                # print(f'normalized decoded payload:\n {normalized_payload_part}')

        print(f"Decoded {len(self.objects)} objects of the {len(payload_packs_binary)} payloads packs correctly formatted")

        # printing decoded msgpacks
        for obj in self.objects:
            print(f"\nThose objects are :")
            print(type(obj).__name__)

        ###___________________________
        ###Sect research
        ###___________________________

        if self.CheckB_search_Sects.isChecked():
            print(f"\nChecking Sects:")
            sect_info = find_sects(self.objects)
            number_members = 0
            new_sect = []
            for sect in sect_info:
                if sect["name"] not in self.dataframed_sects.keys():
                    new_sect.append(sect["name"])
                    self.dataframed_sects[sect["name"]] = get_sect_members(sect)
                    self.dict_of_objects[sect["name"]] = sect
                    number_members += len(sect["members"])
                    print(f'\nsect name : {sect["name"]}')
                    save_list_csv(self.dataframed_sects[sect["name"]], str(sect["name"]))
                    # print(self.dataframed_sects[sect["name"]])
            self.lcd_total_members.display(number_members)
            self.lcd_Number_sect_found.display(len(sect_info))

            self.Combo_First_sect_selector.addItems(new_sect)
            self.Combo_Second_sect_selector.addItems(new_sect)

        ###___________________________
        ###Duel research
        ###___________________________
        if self.CheckB_search_duel.isChecked():
            print(f"\nChecking Duels:")
            duel_info = find_and_fuse_duel_dicts(self.objects)
            if len(duel_info):
                print(f"found duel dicts")
            print(duel_info.keys())
            self.dict_of_objects["duel_info"] = duel_info
            self.Check_Sect_duel_found.setChecked(True)
            try:
                self.lcd_number_battles.display(len(duel_info['battles']))
            except:
                print("fights not found")

            try :
                _ = self.dataframed_sects['SilentDawn']
            except:
                try:
                    self.dataframed_sects['SilentDawn'] = pd.read_csv('playersSilentDawn.csv').values.tolist()
                except:
                    print("SilentDawn not found")
                else:
                    print("prout 1")
                    found = True
            else:
                print("prout 2")
                found = True
            if found:
                self.dataframed_data = sect_duels_data(self.dict_of_objects["duel_info"], self.dataframed_sects['SilentDawn'])

        self.dict_of_objects["all_objects"]= self.objects
        self.ComboB_Object_selector.addItems([ i for i  in list(self.dict_of_objects) if self.ComboB_Object_selector.findText(i) == -1 ])


    ###---------------------------------------
    ###matchmaking Tab Function
    ###---------------------------------------

    def setTable(self, table, dataframe):
        table.setColumnCount(dataframe.shape[0])
        table.setRowCount(dataframe.shape[1])

        for i in range(1,dataframe.shape[0]):
            for j in range(dataframe.shape[1]):
                item = QTableWidgetItem(dataframe[i,j])
                table.setItem(i, j, item)
# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
