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