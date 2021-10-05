from pyzabbix import ZabbixAPI


def getHostnames(zbxurl, apilogin, apipasswd, problemname):
    zbx = ZabbixAPI(zbxurl)
    zbx.login(apilogin, apipasswd)

    items = zbx.problem.get(
        severity=['3', '4'], #change severity if you need
        search={'name': problemname}, #problen name, like Zabbix agent doesn\'t work
        # groupids = [ '1' ] #hosts group filter
    )
    serverlist = []
    for i in range(0, len(items)):
        problem = zbx.trigger.get(triggerids=items[i]['objectid'], selectHosts='extended')
        hostid = problem[0]['hosts'][0]['hostid']
        hostname = zbx.host.get(hostids=hostid)[0]["host"]
        serverlist.append(hostname)
        result = serverlist
        # print(result)
    return result


#print(getHostnames('URL', 'LOGIN', 'PASSWOR', 'PROBLEMNAME'))
