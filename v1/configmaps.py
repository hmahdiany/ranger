from . import namespaces as getns
from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def get_configmaps(all_namespaces, result_dir):
    """
    this function dumps all configmaps in user's namespaces
    it uses namespaces module from v1 package
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir
    CM_DIR = "configmaps"
    
    for ns in all_namespaces:

        # create a directory named configmaps to store all confimaps
        # in a namespace
        if os.path.exists(BASE_DIR/RESULTS_DIR/ns/CM_DIR):
            print(CM_DIR, 'directory already exists')
        else:
            print('creating', CM_DIR, 'directory for', ns, 'namespace')
            os.mkdir(BASE_DIR/RESULTS_DIR/ns/CM_DIR)

        # create an empty list to list all configmaps in a namespace
        all_configmaps = []

        # execute command line to append all configmaps in a namespace
        # to all_configmaps list
        get_cm = "kubectl get cm -n " + ns + "| grep -v 'NAME' | awk '{print $1}'"
        cm_cmd = subprocess.Popen(get_cm, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = cm_cmd.communicate()

        if error:
            print("an error occured: ", error.decode('ascii'))

        # append all configmaps in a namespace to all_configmaps list
        for i in output.decode('ascii').split('\n'):
            if i != '':
                all_configmaps.append(i)

        # iterate through all_confimaps list to dump all confimaps in a namespace
        for cm in all_configmaps:

            # execute command line to get user's namespaces in json format
            # and convert it to yaml format
            cmd = "kubectl get cm -o json -n " + ns + " " + cm
            get_cm = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output, error = get_cm.communicate()
            try:
                json_obj = json.loads(output.decode('ascii'))
                cm_name = json_obj['metadata']['name'] + '.yaml'
                del json_obj['metadata']['resourceVersion']
                del json_obj['metadata']['creationTimestamp']
                del json_obj['metadata']['uid']
                with open(os.path.join(BASE_DIR/RESULTS_DIR/ns/CM_DIR, cm_name), 'w') as f:
                    yaml.dump(json_obj, f)
            except:
                print(error)

if __name__ == "__main__":

    # define result directory
    RESULTS_DIR = "results"

    all_ns = getns.get_user_namespaces()
    get_configmaps(all_ns, RESULTS_DIR)