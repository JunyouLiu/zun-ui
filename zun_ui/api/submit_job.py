import os
import csv
import DB
import commands
import time
import json
import paramiko
import pandas
import threading



# masterIP = '192.168.1.6'
# filepath = '/opt/test.txt'
# containername = 'hadoop-master'
# jar = '/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.2.jar'
# jobtemplate = 'wordcount'
# jobname = 'test'
# inputfile = '/test.txt'
# outputfile = '/wordcount1'
# clustername = 'qh-test'
sourceshell = 'source /opt/stack/devstack/openrc admin admin;'



def writecsv(request, masterIP, appID, containername):
# def writecsv(jobname, jobtemplate, clustername, containername, masterIP, appID, outputfile):
    jobname = request.DATA.get("jobname")
    jobtemplate = request.DATA.get("jobtemplate")
    clustername = request.DATA.get("clustername")
    outputfile = request.DATA.get("outputfilename")
    with open('/opt/stack/job.csv', 'a+') as f:
        fieldnames = ['jobname', 'jobtemplate', 'clustername', 'containername', 'masterIP', 'appID', 'outputfile', "status"]
        write = csv.DictWriter(f, fieldnames=fieldnames)
        reader = csv.DictReader(f)
        if reader.fieldnames != fieldnames:
            write.writeheader()
        write.writerows([{'jobname': jobname, 'jobtemplate': jobtemplate, 'clustername': clustername,
                          'containername': containername, 'masterIP': masterIP, 'appID': appID, 'outputfile': outputfile, "status": 'creating'}])
        f.close()
    return True


def readcsv():
    if os.path.exists('/opt/stack/job.csv') == True:
        with open('/opt/stack/job.csv', 'a+') as f:
            reader = list(csv.DictReader(f))
            return reader
    else:
        return False

def container_submit_job(request, containername):
    # jarname = request.DATA['jar']
    # jar = '/opt/' + jarname
    jar = "/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.2.jar"
    jobtemplate = request.DATA.get("jobtemplate")
    inputfile = request.DATA['inputfile']
    outputfile = request.DATA.get("outputfilename")
    os.system(sourceshell + 'zun exec' + ' ' + containername + ' ' + 'bash hadoop.sh' + ' ' + jar + ' ' + jobtemplate + ' /'
              + inputfile + ' /' + outputfile)
    str = commands.getstatusoutput(sourceshell + 'zun exec' + ' ' + containername + ' ' + 'cat output.txt')
    str = str[1]
    b = str.find('Submitted application')
    while b == -1:
        time.sleep(1)
        str = commands.getstatusoutput(sourceshell + 'zun exec' + ' ' + containername + ' ' + 'cat output.txt')
        str = str[1]
        b = str.find('Submitted application')
    appID = str[b + 22:b + 52]
    os.system(sourceshell + 'zun exec' + ' ' + containername + ' ' + 'rm -rf output.txt')
    return appID


def sftpput(masterIP, localfile, remotefile):
    p_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
    transport = paramiko.Transport(masterIP, 22)
    transport.connect(username='root', pkey=p_key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.put(localfile, remotefile)
    transport.close()


def sftpget(masterIP, remotefile, localfile):
    p_key = paramiko.RSAKey.from_private_key_file('/root/.ssh/id_rsa')
    transport = paramiko.Transport(masterIP, 22)
    transport.connect(username='root', pkey=p_key)
    sftp = paramiko.SFTPClient.from_transport(transport)
    if remotefile[-1] == '/':
        remotefile = remotefile[:-1]
        localfile = localfile + remotefile[remotefile.rfind('/'):]
    else:
        localfile = localfile + remotefile[remotefile.rfind('/'):]
    os.system('mkdir ' + localfile)
    for f in sftp.listdir(remotefile):
        print os.path.join(remotefile + '/'+f)
        sftp.get(os.path.join(remotefile + '/' + f), os.path.join(localfile + '/' + f))
    transport.close()


def upload_file(request, containername, inputfilepath, jarpath):
# def upload_file(request, containername, masterIP, inputfilepath, jarpath):
    inputfilename = request.DATA['inputfile']
    jarname = request.DATA['jar']
    # sftpput(masterIP, inputfilepath, '/opt/hdfsnfs/'+inputfilename)  /opt/hdfsnfs is hdfs nfs gateway directory
    os.system(sourceshell + 'zun cp ' + inputfilepath + ' ' + containername + ':/opt/')
    os.system(sourceshell + 'zun exec ' + containername + ' mv /opt/' + inputfilename + ' /opt/hdfsnfs') # hdfsnfs directory cannot get file by zun cp directly, so container need mv file to hdfsnfs.
    # os.system(sourceshell + 'zun exec ' + containername + ' hdfs dfs -put /opt/' + inputfilename+ ' /') #if container is not hdfs nfs container, user need to hdfs put files to hdfs
    # sftpput(masterIP, jarpath, '/opt/'+jarname)
    return True


def download_file(containername, outputfilename):
    os.system(sourceshell + 'zun exec ' + containername + ' hdfs dfs -put /' + outputfilename + ' /opt/')
    os.system(sourceshell + 'zun exec ' + containername + ' tar cpvf' + outputfilename + '.tar /opt/' + outputfilename)
    os.system(sourceshell + 'zun cp ' + containername + ':/root/' + outputfilename + '.tar /opt/')
    return True


def get_master_details(request):
    clustername = request.DATA.get("clustername")
    return DB.get_master_details_from_clustername(clustername)


def get_status(containername, masterIP, appID):
    yarnInfo = get_yarn_info(containername, masterIP, appID)
    for item in yarnInfo['app']:
        if item['state'] == 'FINISHED':
            return item['finalStatus']
        else:
            return item['state']


def get_yarn_info(containername, masterIP, appID):
    appresult = commands.getstatusoutput(
        sourceshell + 'zun exec ' + containername + ' ' + 'curl --compressed -H "Accept:application/json" -X GET "http://' +
        masterIP + ':8088/ws/v1/cluster/apps/' + appID + '"')
    appresult = appresult[1]
    appresult = appresult[appresult.find('{"app"'):]
    appresult = json.loads(appresult)
    return appresult
    # result = commands.getstatusoutput(sourceshell + 'zun exec ' + containername + ' ' + 'curl --compressed -H "Accept:application/json" -X GET "http://' +
    #                                   masterIP + ':8088/ws/v1/cluster/apps"')
    # result = result[1]
    # if result[-1] == '}':
    #     a = result.find('{"apps"')
    #     if a != -1:
    #         while result[a:].find('--') != -1:
    #             result = commands.getstatusoutput(sourceshell +
    #                 'zun exec ' + containername + ' ' + 'curl --compressed -H "Accept:application/json" -X GET "http://' +
    #                 masterIP + ':8088/ws/v1/cluster/apps"')
    #             result = result[1]
    #             if result[-1] == '}':
    #                 a = result.find('{"apps"')
    #         result = json.loads(result[a:])
    # else:
    #     a = result.find('{"apps"')
    #     b = result.rfind('}')
    #     if a != -1:
    #         while result[a:b+1].find('--') != -1:
    #             result = commands.getstatusoutput(sourceshell +
    #                 'zun exec ' + containername + ' ' + 'curl --compressed -H "Accept:application/json" -X GET "http://' +
    #                 masterIP + ':8088/ws/v1/cluster/apps"')
    #             result = result[1]
    #             if result[-1] == '}':
    #                 a = result.find('{"apps"')
    #                 b = result.rfind('}')
    #         result = json.loads(result[a:b+1])
    return result


class LoopTimer(threading._Timer):
    """Call a function after a specified number of seconds:


            t = LoopTi
            mer(30.0, f, args=[], kwargs={})
            t.start()
            t.cancel()     # stop the timer's action if it's still waiting


    """

    def __init__(self, interval, function, args=[], kwargs={}):
        threading._Timer.__init__(self, interval, function, args, kwargs)

    def run(self):
        '''self.finished.wait(self.interval)
        if not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
        self.finished.set()'''
        while True:
            self.finished.wait(self.interval)
            if self.finished.is_set():
                self.finished.set()
                break
            self.function(*self.args, **self.kwargs)

def fun_timer():
    data = pandas.read_csv('/opt/stack/job.csv', index_col=0)
    for index in range(len(data['appID'])):
        data['status'][index] = get_status(data['containername'][index], data['masterIP'][index], data['appID'][index])
    data.to_csv('/opt/stack/job.csv')
    # d = pandas.read_csv('/root/job.csv', index_col=0)


def submit_job(request):
    clustername = request.DATA['clustername']
    masterinfo = DB.get_master_details_from_clustername(clustername)
    masterIP = masterinfo['ip']
    containername = masterinfo['name']+'-hadoop'
    inputfilepath = os.path.join("/opt/upload/inputfile_upload", request.DATA['inputfile'])
    jar = '/usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-2.9.2.jar' # zun cp cannot transport jar. jar can only be transported by sftp. sftp need floating IP
    # jar = os.path.join("/opt/upload/jar_upload", request.DATA['jar'])
    upload_file(request, containername, inputfilepath, jar)
    # upload_file(request, containername, masterIP, inputfile, jar) #if containers own floating IP, it is the way to upload files.
    appID = container_submit_job(request, containername)
    writecsv(request, masterIP, appID, containername)
    t = LoopTimer(5, fun_timer)
    t.start()