import os

sourceshell = 'source /opt/stack/devstack/openrc admin admin;'


def download_file(containername, containerID, outputfilename):
    os.system(sourceshell + 'zun exec ' + containername + ' hdfs dfs -get /' + outputfilename + ' /opt/')
    os.system(sourceshell + 'zun exec ' + containername + ' tar cpvf ' + outputfilename + '.tar /opt/' + outputfilename)
    os.system('docker cp ' + containerID + ':/root/' + outputfilename + '.tar /opt/stack/')
    return True

if __name__ == '__main__':
    download_file("hadoop-cluster-7ccc7f695c-nskfm-hadoop", "zun-922a61e1-8de5-40e6-ac60-480bed754033", "wordcount1")