import json, os
from zabbix.api import ZabbixAPI

# if {'ZABBIXURL', 'ZABBIXUSERNAME', 'ZABBIXPASSWORD'} not in os.environ:
#     raise SystemExit(1)

#Get Zabbix API Info
zapi = ZabbixAPI(url=os.environ.get('ZABBIXURL'), user=os.environ.get('ZABBIXUSERNAME'), password=os.environ.get('ZABBIXPASSWORD'))

def zabbixGetHosts():
    try:
        result = zapi.do_request('host.get',
        {
            "output": [
                "hostid",
                "host",
            ],
            "selectInterfaces": [
                "ip"
            ],
            "selectGroups" : [
                "name"
            ],
            "selectTags" : [
            ],
            "monitored_hosts": 1
        }
        )
        return result.get('result')
    except:
        return False

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

zbxDiscovery = zabbixGetHosts()

r = dict()
promExport = list()

for row in zbxDiscovery:
    r.update({row['interfaces'][0]['ip']: 'labels' })
del r['127.0.0.1']

for host in r:
    labels = dict()
    for row in zbxDiscovery:
        if row['interfaces'][0]['ip'] == host:
            labels.update({'hostname': row['host']})
            gr = list ()
            for label in row['groups']: gr.append(label['name'])
            labels.update({'group': '|'.join(gr)})            
    promExport.append({'targets': [host], 'labels': labels})

r = json.dumps(promExport, default=set_default, ensure_ascii=False)

if r is not None:
    f = open('targets/targets.json', 'w')
    f.write(r)
    f.close()
