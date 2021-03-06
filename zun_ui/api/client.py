#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import shlex
import os
import csv
import DB

from django.conf import settings

from horizon import exceptions
from horizon.utils.memoized import memoized
from openstack_dashboard.api import base

from neutronclient.v2_0 import client as neutron_client
from zunclient import api_versions
from zunclient.common import template_format
from zunclient.common import utils
from zunclient.v1 import client as zun_client

# YSP
import yaml
from kubernetes import client, config, utils
import json
import getpass
from zun_ui.api import k8s_client
from zun_ui.api import cfy

LOG = logging.getLogger(__name__)

CONTAINER_CREATE_ATTRS = zun_client.containers.CREATION_ATTRIBUTES
CAPSULE_CREATE_ATTRS = zun_client.capsules.CREATION_ATTRIBUTES
BIGDATACLUSTER_CREATE_ATTRS = zun_client.bigdataClusters.CREATION_ATTRIBUTES
IMAGE_PULL_ATTRS = zun_client.images.PULL_ATTRIBUTES
API_VERSION = api_versions.APIVersion(api_versions.DEFAULT_API_VERSION)


def capsule_show(request, id):
    return zunclient(request).capsules.get(id)


def get_auth_params_from_request(request):
    """Extracts properties needed by zunclient call from the request object.

    These will be used to memoize the calls to zunclient.
    """
    endpoint_override = ""
    try:
        endpoint_override = base.url_for(request, 'container')
    except exceptions.ServiceCatalogException:
        LOG.debug('No Container Management service is configured.')
        return None
    return (
        request.user.username,
        request.user.token.id,
        request.user.tenant_id,
        endpoint_override
    )


@memoized
def zunclient(request):
    (
        username,
        token_id,
        project_id,
        endpoint_override
    ) = get_auth_params_from_request(request)

    LOG.debug('zunclient connection created using the token "%s" and url'
              ' "%s"' % (token_id, endpoint_override))
    api_version = API_VERSION
    if API_VERSION.is_latest():
        c = zun_client.Client(
            username=username,
            project_id=project_id,
            auth_token=token_id,
            endpoint_override=endpoint_override,
            api_version=api_versions.APIVersion("1.1"),
        )
        api_version = api_versions.discover_version(c, api_version)
    c = zun_client.Client(username=username,
                          project_id=project_id,
                          auth_token=token_id,
                          endpoint_override=endpoint_override,
                          api_version=api_version)
    return c


def get_auth_params_from_request_neutron(request):
    """Extracts properties needed by neutronclient call from the request object.

    These will be used to memoize the calls to neutronclient.
    """
    return (
        request.user.token.id,
        base.url_for(request, 'network'),
        base.url_for(request, 'identity')
    )


@memoized
def neutronclient(request):
    (
        token_id,
        neutron_url,
        auth_url
    ) = get_auth_params_from_request_neutron(request)
    insecure = getattr(settings, 'OPENSTACK_SSL_NO_VERIFY', False)
    cacert = getattr(settings, 'OPENSTACK_SSL_CACERT', None)

    LOG.debug('neutronclient connection created using the token "%s" and url'
              ' "%s"' % (token_id, neutron_url))
    c = neutron_client.Client(token=token_id,
                              auth_url=auth_url,
                              endpoint_url=neutron_url,
                              insecure=insecure, ca_cert=cacert)
    return c


def _cleanup_params(attrs, check, **params):
    args = {}
    run = False

    for (key, value) in params.items():
        if key == "run":
            run = value
        elif key == "cpu_policy":
            args[key] = value
        elif key == "cpu":
            args[key] = float(value)
        elif key == "memory" or key == "disk":
            args[key] = int(value)
        elif key == "privileged":
            if value == True:
                args[key] = value
            else:
                del params[key]
        elif key == "host":
            args[key] = value
        elif key == "interactive" or key == "mounts" or key == "nets" \
                or key == "security_groups" or key == "hints"\
                or key == "auto_remove" or key == "auto_heal":
            args[key] = value
        elif key == "restart_policy":
            args[key] = utils.check_restart_policy(value)
        elif key == "environment" or key == "labels":
            values = {}
            vals = value.split(",")
            for v in vals:
                kv = v.split("=", 1)
                values[kv[0]] = kv[1]
            args[str(key)] = values
        elif key == "command":
            args[key] = shlex.split(value)
        elif key in attrs:
            if value is None:
                value = ''
            args[str(key)] = str(value)
        elif check:
            raise exceptions.BadRequest(
                "Key must be in %s" % ",".join(attrs))

    return args, run


def _delete_attributes_with_same_value(old, new):
    '''Delete attributes with same value from new dict

    If new dict has same value in old dict, remove the attributes
    from new dict.
    '''
    for k in old.keys():
        if k in new:
            if old[k] == new[k]:
                del new[k]
    return new


def container_create(request, **kwargs):
    args, run = _cleanup_params(CONTAINER_CREATE_ATTRS, True, **kwargs)
    response = None
    if run:
        response = zunclient(request).containers.run(**args)
    else:
        response = zunclient(request).containers.create(**args)
    return response


def container_update(request, id, **kwargs):
    '''Update Container

    Get current Container attributes and check updates.
    And update with "rename" for "name", then use "update" for
    "cpu" and "memory".
    '''

    # get current data
    container = zunclient(request).containers.get(id).to_dict()
    if container["memory"] is not None:
        container["memory"] = int(container["memory"].replace("M", ""))
    args, run = _cleanup_params(CONTAINER_CREATE_ATTRS, True, **kwargs)

    # remove same values from new params
    _delete_attributes_with_same_value(container, args)

    # do update
    if len(args):
        zunclient(request).containers.update(id, **args)

    return args


def container_delete(request, **kwargs):
    return zunclient(request).containers.delete(**kwargs)


def container_list(request, limit=None, marker=None, sort_key=None,
                   sort_dir=None):
    return zunclient(request).containers.list(limit, marker, sort_key,
                                              sort_dir)


def container_show(request, id):
    return zunclient(request).containers.get(id)


def container_logs(request, id):
    args = {}
    args["stdout"] = True
    args["stderr"] = True
    return zunclient(request).containers.logs(id, **args)


def container_start(request, id):
    return zunclient(request).containers.start(id)


def container_stop(request, id, timeout):
    return zunclient(request).containers.stop(id, timeout)


def container_restart(request, id, timeout):
    return zunclient(request).containers.restart(id, timeout)


def container_rebuild(request, id, **kwargs):
    return zunclient(request).containers.rebuild(id, **kwargs)


def container_commit(request, id, reponame):
    return zunclient(request).containers.commit(id, reponame)


def container_pause(request, id):
    return zunclient(request).containers.pause(id)


def container_unpause(request, id):
    return zunclient(request).containers.unpause(id)


def container_execute(request, id, command):
    args = {"command": command}
    return zunclient(request).containers.execute(id, **args)


def container_kill(request, id, signal=None):
    return zunclient(request).containers.kill(id, signal)


def container_attach(request, id):
    return zunclient(request).containers.attach(id)


def container_resize(request, id, width, height):
    return zunclient(request).containers.resize(id, width, height)


def container_network_attach(request, id):
    network = request.DATA.get("network") or None
    zunclient(request).containers.network_attach(id, network)
    return {"container": id, "network": network}


def container_network_detach(request, id):
    network = request.DATA.get("network") or None
    zunclient(request).containers.network_detach(id, network)
    return {"container": id, "network": network}


def port_update_security_groups(request):
    port = request.DATA.get("port") or None
    security_groups = request.DATA.get("security_groups") or None
    kwargs = {"security_groups": security_groups}
    neutronclient(request).update_port(port, body={"port": kwargs})
    return {"port": port, "security_group": security_groups}


def availability_zone_list(request):
    list = zunclient(request).availability_zones.list()
    return list


def capsule_list(request, limit=None, marker=None, sort_key=None,
                 sort_dir=None):
    return zunclient(request).capsules.list(limit, marker, sort_key, sort_dir)


def capsule_show(request, id):
    return zunclient(request).capsules.get(id)


def capsule_create(request, **kwargs):
    args, run = _cleanup_params(CAPSULE_CREATE_ATTRS, True, **kwargs)
    args["template"] = template_format.parse(args["template"])
    print 'template', args["template"]
    return zunclient(request).capsules.create(**args)

# YSP

# no use
def bigdataCluster_list(request, limit=None, marker=None, sort_key=None, sort_dir=None):
    # return zunclient(request).bigdataClusters.list(limit, marker, sort_key, sort_dir)
    return zunclient(request).bigdataClusters.list(limit, marker, sort_key, sort_dir)

def bigdataCluster_create(request, **kwargs):
    args, run = _cleanup_params(BIGDATACLUSTER_CREATE_ATTRS, True, **kwargs)
    # yaml file -> file
    yaml_file = str(args["template"])

    yaml_file_segement = yaml_file.split('---')
    for yaml_f in yaml_file_segement:
        # args["template"] = template_format.parse(args["template"])
        args["template"] = template_format.parse(yaml_f)
        json_file = args["template"]
        k8s_client.create_deployment_from_yaml(json_file)
    # print yaml_file
    # args["template"] = template_format.parse(args["template"])
    #
    # json_file = args["template"]
    # print "client:", json_file
    # k8s_client.create_deployment_from_yaml(json_file)
    return

def create_by_proprity_test(request, **kwargs):
    args, run = _cleanup_params(BIGDATACLUSTER_CREATE_ATTRS, True, **kwargs)
    print args, run
    return


def capsule_delete(request, **kwargs):
    return zunclient(request).capsules.delete(**kwargs)


def image_list(request, limit=None, marker=None, sort_key=None,
               sort_dir=None):
    return zunclient(request).images.list(limit, marker, sort_key,
                                          sort_dir)


def image_create(request, **kwargs):
    args, run = _cleanup_params(IMAGE_PULL_ATTRS, True, **kwargs)
    return zunclient(request).images.create(**args)


def image_delete(request, id, **kwargs):
    return zunclient(request).images.delete(id, **kwargs)


def host_list(request, limit=None, marker=None, sort_key=None, sort_dir=None):
    return zunclient(request).hosts.list(limit, marker, sort_key, sort_dir)


def host_show(request, id):
    return zunclient(request).hosts.get(id)


# Job submit
def writecsv(request, master_IP, appID):
    jobname = request.data.get("jobname")
    jobtemplate = request.data.get("jobtemplate")
    clustername = request.data.get("clustername")
    outputfile = request.data.get("outputfile")
    with open('/root/job.csv', 'a+') as f:
        fieldnames = ['jobname', 'jobtemplate', 'clustername', 'masterIP', 'appID', 'outputfile']
        write = csv.DictWriter(f, fieldnames=fieldnames)
        reader = csv.DictReader(f)
        if reader.fieldnames != fieldnames:
            write.writeheader()
        write.writerows([{'jobname': jobname, 'jobtemplate': jobtemplate, 'clustername': clustername,
                          'masterIP': master_IP, 'appID': appID, 'outputfile': outputfile}])
        f.close()
    return True


def readcsv():
    file_path = '/root/job.csv'
    if os.path.exists(file_path) == True:
        with open(file_path, 'a+') as f:
            reader = list(csv.DictReader(f))
            return reader
    else:
        return False