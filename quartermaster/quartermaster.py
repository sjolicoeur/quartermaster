# Quartermaster
# runs on all dockers
# registers images to the ETCD

from docker import Client
from docker.utils import kwargs_from_env
import os
from urlparse import urlparse
import etcd
import time
import logging

log = logging.getLogger(__name__)
env = kwargs_from_env(assert_hostname=False)
env['version'] = os.getenv('DOCKER_API_VERSION', '1.15')
client = Client(**env)
ROOT_KEY = os.getenv('QUARTERMASTER_ROOT_KEY','/ha_quartermaster')
TIMEOUT = 60 * 3 # 3 minutes
get_docker_host = lambda: urlparse(os.getenv('DOCKER_HOST')).hostname

def get_name(name):
    split_name = name.split(".", 1)
    if len(split_name) == 1:
        return "Unknown", split_name[0]
    return split_name[0], split_name[1]      

def list_containers():
    containers_to_serve = []
    docker_host_ip = get_docker_host()
    for container in client.containers():
        if container['Ports']:
            for port in container['Ports']:
                if port['Type'] in ['tcp', u'tcp']:
                    service, name = get_name(container['Names'][0])
                    containers_to_serve.append({
                        "name": name, 
                        "ip": docker_host_ip,
                        "port": port['PublicPort'],
                        "service": service.replace("/", "")
                    })
    return containers_to_serve

def write_to_etcd(container_listing):
    etcd_client = etcd.Client(host=get_docker_host())
    for app in container_listing:
        key = "%(root_key)s/%(app_name)s/%(ip)s/%(port)s" % {
            "root_key": ROOT_KEY,
            "app_name": app['name'],
            "ip": app['ip'],
            "port": app['port']
        }
        log.info("settings key: %s to '%s'" % (key, app['service']))
        etcd_client.write(key, app['service'], ttl=TIMEOUT*3)


if __name__ == '__main__':
    flag = True
    while(flag):
        log.info("Getting the containers listing")
        containers_list = list_containers()
        log.info("Writting to ETCD")
        write_to_etcd(containers_list)
        time.sleep(TIMEOUT)
