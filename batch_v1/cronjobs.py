from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def get_cronjobs(all_namespaces, result_dir):
    """
    this function dumps all cronjobs in user's namespaces
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir
    CJ_DIR = "cronjobs"
    
    for ns in all_namespaces:

        # create a directory named cronjobs to store all confimaps
        # in a namespace
        if os.path.exists(BASE_DIR/RESULTS_DIR/ns/CJ_DIR):
            print(CJ_DIR, 'directory already exists')
        else:
            print('creating', CJ_DIR, 'directory for', ns, 'namespace')
            os.mkdir(BASE_DIR/RESULTS_DIR/ns/CJ_DIR)

        # create an empty list to list all cronjobs in a namespace
        all_cronjobs = []

        # execute command line to append all cronjobs in a namespace
        # to all_cronjobs list
        get_cj = "kubectl get cj -n " + ns + "| grep -v 'NAME' | awk '{print $1}'"
        cm_cmd = subprocess.Popen(get_cj, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = cm_cmd.communicate()

        if error:
            print("an error occured: ", error.decode('ascii'))

        # append all cronjobs in a namespace to all_cronjobs list
        for i in output.decode('ascii').split('\n'):
            if i != '':
                all_cronjobs.append(i)

        # iterate through all_cronjobs list to dump all cronjobs in a namespace
        for cj in all_cronjobs:

            # execute command line to get user's namespaces in json format
            # and convert it to yaml format
            cmd = "kubectl get cj -o json -n " + ns + " " + cj
            get_cj = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output, error = get_cj.communicate()
            try:
                json_obj = json.loads(output.decode('ascii'))
                cj_name = json_obj['metadata']['name'] + '.yaml'
                del json_obj['metadata']['resourceVersion']
                del json_obj['metadata']['creationTimestamp']
                del json_obj['metadata']['uid']
                with open(os.path.join(BASE_DIR/RESULTS_DIR/ns/CJ_DIR, cj_name), 'w') as f:
                    yaml.dump(json_obj, f)
            except:
                print(error)
