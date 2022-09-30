import subprocess
import os
from pathlib import Path
import json
import yaml
from yaml.loader import SafeLoader

def create_namespace_yaml_file(all_namespaces, result_dir):
    """
    this function creates yaml files for all user namespaces
    which has been listed in all_namespaces list
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir

    for ns in all_namespaces:

        # create a directory for each namespace in the list
        if os.path.exists(BASE_DIR/RESULTS_DIR/ns):
            print(ns, 'directory already exists')
        else:
            print('creating', ns, 'directory')
            os.mkdir(BASE_DIR/RESULTS_DIR/ns)

        # execute command line to get user's namespaces in json format
        # and convert it to yaml format
        cmd = "kubectl get ns -o json " + ns
        all_ns = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = all_ns.communicate()
        try:
            json_obj = json.loads(output.decode('ascii'))
            del json_obj['metadata']['resourceVersion']
            del json_obj['metadata']['creationTimestamp']
            del json_obj['metadata']['uid']
            del json_obj['status']
            with open(os.path.join(BASE_DIR/RESULTS_DIR/ns, 'namespace.yaml'), 'w') as f:
                yaml.dump(json_obj, f)
        except:
            print(error)

def get_user_namespaces(RESULTS_DIR):
    """
    this function creates a list of all namesapces
    in a kubernetes cluster except those that start
    with kube prefix
    """

    # create an empty list for all namespaces
    all_namespaces = []

    # command line to get all namespaces with ai prefix
    get_ns = "kubectl get ns | grep  -v '^kube' | grep -v 'NAME' | awk '{print $1}'"

    # execute get_ns command to capture user's namespaces
    cmd = subprocess.Popen(get_ns, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    output, error = cmd.communicate()

    if error:
        print("an error occured: ", error.decode('ascii'))

    # append user namespaces to all_namespaces list
    for i in output.decode('ascii').split('\n'):
        if i != '':
            all_namespaces.append(i)

    # # save dump file for namespaces
    # create_namespace_yaml_file(all_namespaces, RESULTS_DIR)
    # return all_namespaces list 
    return all_namespaces


