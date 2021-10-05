# Trigger dependencies creator

from pyzabbix import ZabbixAPI

# Connect to zabbix
zabbix = ZabbixAPI('URL')
zabbix.login('APILOGIN', 'PASSWORD')


# get trigger info
def triggerget(hostid, description):
    result = zabbix.trigger.get(
        # groupids = groupids,
        hostids=hostid,
        search={"description": description}
    )
    return result


# get hosts info by groupid
def hostsget(groupids, *inventory):
    result = zabbix.host.get(
        groupids=groupids,
        selectInventory=[inventory],
        filter={'status': '0'}  # only enabled hosts
    )
    return result


# get one host info by host id
def hostget(hostid):
    result = zabbix.host.get(
        hostids=hostid,
        filter={'status': '0'}
    )
    return result


# setup trigger dependencies
def settriggerdep(triggerdepof, triggerdepon):
    zabbix.trigger.adddependencies(
        triggerid=triggerdepof,  # Dependent
        dependsOnTriggerid=triggerdepon  # main trigger
    )


# set hosts any inventory volume
def setinventory(hostid, inventory, text):
    result = zabbix.host.update(
        hostid=hostid,
        inventory={inventory: text}
    )
    return result


# get hosts interface ip address + type interface filter
def getipaddress(hostid, inftype):
    result = zabbix.hostinterface.get(
        hostids=hostid,
        filter={'type': inftype}
    )
    return result


# remove all trigger dependencies
def deltriggerdep(hostgrid, triggerdescription):
    hosts = hostsget(hostgrid)
    for i in hosts:
        try:
            trigger_id = triggerget(i["hostid"], triggerdescription)[0]['triggerid']
            zabbix.trigger.deletedependencies(triggerid=trigger_id)  # trigger with dependencies
        except:
            pass


# add trigger dependensies + ip filtering
def adddepbyip(slavehostsgrid, mainhostsgrid, interfacetype):
    hosts_slave = hostsget(slavehostsgrid)  # dependent trigger
    hosts_main = hostsget(mainhostsgrid)
    for i in hosts_slave:
        for j in hosts_main:
            ip_i = (getipaddress(i['hostid'], interfacetype)[0]['ip']).split('.')[0:3]
            ip_j = (getipaddress(j['hostid'], interfacetype)[0]['ip']).split('.')[0:3]
            if ip_i == ip_j:
                # print(ip_i, ip_j)
                try:
                    trigger_slave = triggerget(i["hostid"], "Unavailable by ICMP ping")
                    trigger_master = triggerget(j["hostid"], "Unavailable by ICMP ping")
                    settriggerdep(trigger_slave[0]['triggerid'], trigger_master[0]['triggerid'])
                except:
                    print("Error")
                    pass
            else:
                pass


# print(hostsget(64)[4])
# print((getipaddress(11348, 2)))
# adddepbyip(64, 63, 1)
# deltriggerdep(64, 'Unavailable by ICMP ping')
zabbix.user.logout()
