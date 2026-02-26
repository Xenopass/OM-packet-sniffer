# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_OM_Sniffer.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLCDNumber, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QTableWidget,
    QTableWidgetItem, QTextEdit, QTreeView, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(964, 639)
        MainWindow.setIconSize(QSize(64, 64))
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.TabShape.Triangular)
        self.Open_save_directory_window = QAction(MainWindow)
        self.Open_save_directory_window.setObjectName(u"Open_save_directory_window")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.gridLayout_3 = QGridLayout(self.tab)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.Txt_Console_output = QTextEdit(self.tab)
        self.Txt_Console_output.setObjectName(u"Txt_Console_output")
        self.Txt_Console_output.setReadOnly(True)

        self.gridLayout.addWidget(self.Txt_Console_output, 5, 0, 1, 1)

        self.line = QFrame(self.tab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.line_2 = QFrame(self.tab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_start_sniff = QPushButton(self.tab)
        self.btn_start_sniff.setObjectName(u"btn_start_sniff")

        self.horizontalLayout.addWidget(self.btn_start_sniff)

        self.btn_finish_sniff = QPushButton(self.tab)
        self.btn_finish_sniff.setObjectName(u"btn_finish_sniff")

        self.horizontalLayout.addWidget(self.btn_finish_sniff)

        self.btn_process_data = QPushButton(self.tab)
        self.btn_process_data.setObjectName(u"btn_process_data")

        self.horizontalLayout.addWidget(self.btn_process_data)


        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setAutoFillBackground(True)

        self.verticalLayout.addWidget(self.label)

        self.CheckB_search_duel = QCheckBox(self.tab)
        self.CheckB_search_duel.setObjectName(u"CheckB_search_duel")

        self.verticalLayout.addWidget(self.CheckB_search_duel)

        self.CheckB_search_Demonbend = QCheckBox(self.tab)
        self.CheckB_search_Demonbend.setObjectName(u"CheckB_search_Demonbend")

        self.verticalLayout.addWidget(self.CheckB_search_Demonbend)

        self.CheckB_search_Sects = QCheckBox(self.tab)
        self.CheckB_search_Sects.setObjectName(u"CheckB_search_Sects")

        self.verticalLayout.addWidget(self.CheckB_search_Sects)

        self.checkBox = QCheckBox(self.tab)
        self.checkBox.setObjectName(u"checkBox")

        self.verticalLayout.addWidget(self.checkBox)


        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label_4 = QLabel(self.tab)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.lcd_Number_sect_found = QLCDNumber(self.tab)
        self.lcd_Number_sect_found.setObjectName(u"lcd_Number_sect_found")
        self.lcd_Number_sect_found.setDigitCount(2)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lcd_Number_sect_found)

        self.label_3 = QLabel(self.tab)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.lcd_total_members = QLCDNumber(self.tab)
        self.lcd_total_members.setObjectName(u"lcd_total_members")
        self.lcd_total_members.setDigitCount(3)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lcd_total_members)


        self.horizontalLayout_2.addLayout(self.formLayout)

        self.line_3 = QFrame(self.tab)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName(u"formLayout_4")
        self.label_7 = QLabel(self.tab)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.label_6 = QLabel(self.tab)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.lcd_number_battles = QLCDNumber(self.tab)
        self.lcd_number_battles.setObjectName(u"lcd_number_battles")

        self.formLayout_4.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lcd_number_battles)

        self.Check_Sect_duel_found = QCheckBox(self.tab)
        self.Check_Sect_duel_found.setObjectName(u"Check_Sect_duel_found")
        self.Check_Sect_duel_found.setCheckable(False)
        self.Check_Sect_duel_found.setTristate(False)

        self.formLayout_4.setWidget(0, QFormLayout.ItemRole.FieldRole, self.Check_Sect_duel_found)


        self.horizontalLayout_2.addLayout(self.formLayout_4)

        self.line_4 = QFrame(self.tab)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_4)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.label_8 = QLabel(self.tab)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.lcd_demonbend_participants = QLCDNumber(self.tab)
        self.lcd_demonbend_participants.setObjectName(u"lcd_demonbend_participants")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lcd_demonbend_participants)

        self.Check_demonbend_found = QCheckBox(self.tab)
        self.Check_demonbend_found.setObjectName(u"Check_demonbend_found")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.Check_demonbend_found)


        self.horizontalLayout_2.addLayout(self.formLayout_2)


        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 0, 1, 1)

        self.label_9 = QLabel(self.tab)
        self.label_9.setObjectName(u"label_9")

        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)


        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.gridLayout_5 = QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.groupBox = QGroupBox(self.tab_3)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_6 = QGridLayout(self.groupBox)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.formLayout_3 = QFormLayout()
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.Combo_First_sect_selector = QComboBox(self.groupBox)
        self.Combo_First_sect_selector.setObjectName(u"Combo_First_sect_selector")

        self.formLayout_3.setWidget(0, QFormLayout.ItemRole.FieldRole, self.Combo_First_sect_selector)

        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.Combo_Second_sect_selector = QComboBox(self.groupBox)
        self.Combo_Second_sect_selector.setObjectName(u"Combo_Second_sect_selector")

        self.formLayout_3.setWidget(1, QFormLayout.ItemRole.FieldRole, self.Combo_Second_sect_selector)


        self.gridLayout_6.addLayout(self.formLayout_3, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(self.tab_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.gridLayout_8 = QGridLayout(self.groupBox_3)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.Btn_Matchmaking = QPushButton(self.groupBox_3)
        self.Btn_Matchmaking.setObjectName(u"Btn_Matchmaking")

        self.gridLayout_8.addWidget(self.Btn_Matchmaking, 0, 0, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)


        self.gridLayout_5.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.line_5 = QFrame(self.tab_3)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout_5.addWidget(self.line_5, 0, 1, 1, 1)

        self.groupBox_2 = QGroupBox(self.tab_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setCheckable(False)
        self.gridLayout_7 = QGridLayout(self.groupBox_2)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.gridLayout_7.setContentsMargins(0, 6, 0, 0)
        self.Table_matchmaking = QTableWidget(self.groupBox_2)
        self.Table_matchmaking.setObjectName(u"Table_matchmaking")

        self.gridLayout_7.addWidget(self.Table_matchmaking, 0, 0, 1, 1)


        self.gridLayout_5.addWidget(self.groupBox_2, 0, 2, 1, 1)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.gridLayout_4 = QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_5 = QLabel(self.tab_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_3.addWidget(self.label_5)

        self.ComboB_Object_selector = QComboBox(self.tab_2)
        self.ComboB_Object_selector.setObjectName(u"ComboB_Object_selector")
        self.ComboB_Object_selector.setEditable(False)

        self.horizontalLayout_3.addWidget(self.ComboB_Object_selector)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.treeView = QTreeView(self.tab_2)
        self.treeView.setObjectName(u"treeView")

        self.verticalLayout_2.addWidget(self.treeView)


        self.gridLayout_4.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_2, "")

        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 964, 33))
        self.menuOvermortal = QMenu(self.menubar)
        self.menuOvermortal.setObjectName(u"menuOvermortal")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
#if QT_CONFIG(shortcut)
        self.label_5.setBuddy(self.ComboB_Object_selector)
#endif // QT_CONFIG(shortcut)

        self.menubar.addAction(self.menuOvermortal.menuAction())
        self.menuOvermortal.addAction(self.Open_save_directory_window)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Overmortal Data sniffer", None))
        self.Open_save_directory_window.setText(QCoreApplication.translate("MainWindow", u"&Save Directory", None))
        self.btn_start_sniff.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.btn_finish_sniff.setText(QCoreApplication.translate("MainWindow", u"Finish", None))
        self.btn_process_data.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"What will you look out for ?", None))
        self.CheckB_search_duel.setText(QCoreApplication.translate("MainWindow", u"Duel info", None))
        self.CheckB_search_Demonbend.setText(QCoreApplication.translate("MainWindow", u"DemonBend", None))
        self.CheckB_search_Sects.setText(QCoreApplication.translate("MainWindow", u"Sect info", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Dunnow yet", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Number of sect found:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"members", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Sect duel found", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"number of battles found", None))
        self.Check_Sect_duel_found.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Demonbend Abyss found", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Number of participants", None))
        self.Check_demonbend_found.setText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Console :", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Collect Data", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Choose the Sect to matchmake", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"First Sect", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Second Sect", None))
        self.groupBox_3.setTitle("")
        self.Btn_Matchmaking.setText(QCoreApplication.translate("MainWindow", u"Matchmaking", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Matchmaking Table", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Matchmaking", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"&Lists found :", None))
        self.ComboB_Object_selector.setCurrentText("")
        self.ComboB_Object_selector.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Pick a list to display", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Processed Data", None))
        self.menuOvermortal.setTitle(QCoreApplication.translate("MainWindow", u"&Parameters", None))
    # retranslateUi

