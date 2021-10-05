from pyzabbix import ZabbixAPI
import socket

# Connect to zabbix
zabbix = ZabbixAPI('URL')
zabbix.login('APILOGIN', 'PASSWORD')

hosts = zabbix.host.get(
    # hostids = [ 'hostid' ] ,
    output=["host"],
    # groupids = ["15"],
)


# print(let(hosts))
def portChecker(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((hostname, port))
    if result == 0:
        return True
        sock.close()
    else:
        return False
        sock.close()


for i in hosts:
    try:
        port = portChecker(i.get('host'), 22)
        # print(i.get('host'))
        if "sp" in i.get('host') and port:
            print(i.get('host'))
    except:
        print(i.get('host'), "server could not be resolved")
