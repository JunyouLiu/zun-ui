#
# kubernetes client
#

from os import  path
import yaml
from kubernetes import client, config, utils
import json
from os import system
import getpass
import uuid
from zun_ui.api import cfy

#system("whoami")


def list_all_pods():

    # user_name = getpass.getuser()
    # print(user_name)
    # print ("---")
    # config_file = open('//.kube/config', 'r')
    # print (config_file.read())

    # load  k8s-config
    config.load_kube_config("//.kube/config")

    v1 = client.CoreV1Api()
    result_set = v1.list_pod_for_all_namespaces(watch = False)

    # format to a json file
    pods_info = "{\"pods_info\":["
    # print type(result_set)
    for item_pod in result_set.items:
        pods_info = pods_info + "{"
        pods_info = pods_info + "\"pods_name\":" + json.dumps(item_pod.metadata.name) + ","
        pods_info = pods_info + "\"pods_namespace\":" + json.dumps(item_pod.metadata.namespace) + ","
        pods_info = pods_info + "\"pods_labels\":" + json.dumps(item_pod.metadata.labels) + ","
        id = str(uuid.uuid4())
        print id
        pods_info = pods_info + "\"id\":" + json.dumps(id) + "},"

        print ("%s\n" % item_pod.metadata.name)
        print ("%s\n" % item_pod.metadata.labels)
        print ("%s" % item_pod.metadata.namespace)
        # print ("-----------")
    pods_info = pods_info[:-1]
    pods_info = pods_info + "]}"
    # print pods_info
    # print result_set
    return pods_info


def create_deployment_from_yaml(json_file):
# def create_deployment_from_yaml():
    # load  k8s-config
    config.load_kube_config("//.kube/config")
    # XXXyaml = get_file()
    k8s_client = client.ApiClient()
    # utils.create_from_yaml(k8s_client, yaml_file)
    # cfy.create_from_yaml(k8s_client, "/root/yaml-file/deployment_test.yaml")
    print "k8s_client:", json_file
    cfy.create_from_yaml_single_item(k8s_client, json_file)

    # utils.create_from_yaml(k8s_client, "/root/yaml-file/vh/virtualhadoop1.yaml")
    # utils.create_from_yaml(k8s_client, "/root/yaml-file/vh/virtualhadoop2.yaml")

    # deployment_test.yaml
    # utils.create_from_yaml(k8s_client, "deployment_test.yaml")
    # k8s_client = client.ApiClient()

    # k8s_api = client.ExtensionsV1beta1Api(k8s_client)
    # extensions/v1beta1 
    # deps = k8s_api.read_namespaced_deployment("XXX.deployment", "default")
    # print ("Deployment {0} created".format(deps.metadata.name) )

if __name__ == "__main__":
    # list_all_pods()
    create_deployment_from_yaml()
