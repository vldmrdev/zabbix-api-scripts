from pyzabbix import ZabbixAPI
import csv

# Connect to zabbix
zbx = ZabbixAPI('URL')
zbx.login('APILOGIN', 'PASSWORD')

# csv reading
with open('vpns.csv') as f:
    incl_col1 = [0] # first column
    incl_col2 = [1] # second column
    reader = csv.reader(f, delimiter=';')
    for row in reader:
        itemname = list(row[i] for i in incl_col1)
        keyname = "key." + str(*itemname) # v1
        #keyname = f'key {*itemname}' #v2
        oid = list(row[i] for i in incl_col2)
        # Creating item for hostid
        item = zbx.item.create(
            hostid=11636,
            name=str(*itemname),
            key_=keyname,
            type=4,
            value_type=3,
            snmp_oid=str(*oid),
            snmp_community="orion",
            delay="120s",
            applications=["8961"]
        )

# Logout from Zabbix
zbx.user.logout()
