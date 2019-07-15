sourceshell = 'source /opt/stack/devstack/openrc admin admin;'
import commands
import json

result = commands.getstatusoutput(sourceshell + 'zun exec hadoop-master curl --compressed -H "Accept:application/json" -X GET "http://192.168.1.8:8088/ws/v1/cluster/apps/application_1561980355039_0004"')
result = result[1]
result = result[result.find('{"app"'):]
print json.loads(result)