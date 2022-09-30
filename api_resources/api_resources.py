import os
import subprocess

def api_resources():
    """
    get all api resources which are currently available through api server
    """

    cmd = "kubectl api-resources | grep -v 'NAME' | awk '{print $1}'"
    get_api = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    output, error = get_api.communicate()

    if error:
            print("an error occured: ", error.decode('ascii'))

    api_list = []
    for i in output.decode('ascii').split('\n'):
        if i != '':
            api_list.append(i)
    
    return api_list

def namespaced_resources():
    """
    get all api resources which are namespace wide
    """

    cmd = "kubectl api-resources | grep -v 'NAME' | grep 'true' | awk '{print $1}'"
    get_api = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    output, error = get_api.communicate()

    if error:
        print("an error occured: ", error.decode('ascii'))

    namespaced_api = []
    for i in output.decode('ascii').split('\n'):
        if i != '':
            namespaced_api.append(i)

    return namespaced_api

def cluster_wide_resources():
    """
    get all api resources which are cluster_widewide
    """

    cmd = "kubectl api-resources | grep -v 'NAME' | grep 'false' | awk '{print $1}'"
    get_api = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    output, error = get_api.communicate()

    if error:
        print("an error occured: ", error.decode('ascii'))

    cluster_wide_api = []
    for i in output.decode('ascii').split('\n'):
        if i != '':
            cluster_wide_api.append(i)

    return cluster_wide_api