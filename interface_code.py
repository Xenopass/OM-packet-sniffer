import psutil
from scapy.all import get_if_list, get_if_addr

def get_interface_for_port(port):
    #Find local IP used by that port
    local_ip = None
    for conn in psutil.net_connections(kind="tcp"):
        if conn.raddr and conn.raddr.port == port:
            local_ip = conn.laddr.ip
            break

    if not local_ip:
        return None

    #Match IP with Scapy interface list
    for iface in get_if_list():
        try:
            if get_if_addr(iface) == local_ip:
                return iface
        except:
            pass

    return None

if "__main__" == __name__:
    iface_name = get_interface_for_port(8583)
    print("Scapy iface:", iface_name)