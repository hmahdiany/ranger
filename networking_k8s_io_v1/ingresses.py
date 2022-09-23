from v1 import namespaces as getns
from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def get_ingresses(all_namespaces, result_dir):
    """
    this function dumps all ingresses in user's namespaces
    it uses namespaces module from v1 package
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir
    ING_DIR = "ingresses"
    
    for ns in all_namespaces:

        # create a directory named ingresses to store all confimaps
        # in a namespace
        if os.path.exists(BASE_DIR/RESULTS_DIR/ns/ING_DIR):
            print(ING_DIR, 'directory already exists')
        else:
            print('creating', ING_DIR, 'directory for', ns, 'namespace')
            os.mkdir(BASE_DIR/RESULTS_DIR/ns/ING_DIR)

        # create an empty list to list all ingresses in a namespace
        all_ingresses = []

        # execute command line to append all ingresses in a namespace
        # to all_ingresses list
        get_ing = "kubectl get ing -n " + ns + "| grep -v 'NAME' | awk '{print $1}'"
        ing_cmd = subprocess.Popen(get_ing, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = ing_cmd.communicate()

        if error:
            print("an error occured: ", error.decode('ascii'))

        # append all ingresses in a namespace to all_ingresses list
        for i in output.decode('ascii').split('\n'):
            if i != '':
                all_ingresses.append(i)

        # iterate through all_ingresses list to dump all ingresses in a namespace
        for ing in all_ingresses:

            # execute command line to get user's namespaces in json format
            # and convert it to yaml format
            cmd = "kubectl get ing -o json -n " + ns + " " + ing
            get_ing = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output, error = get_ing.communicate()
            try:
                json_obj = json.loads(output.decode('ascii'))
                ing_name = json_obj['metadata']['name'] + '.yaml'
                del json_obj['metadata']['resourceVersion']
                del json_obj['metadata']['creationTimestamp']
                del json_obj['metadata']['uid']
                del json_obj['status']
                with open(os.path.join(BASE_DIR/RESULTS_DIR/ns/ING_DIR, ing_name), 'w') as f:
                    yaml.dump(json_obj, f)
            except:
                print(error)

if __name__ == "__main__":

    # define result directory
    RESULTS_DIR = "results"

    all_ns = getns.get_user_namespaces()
    get_ingresses(all_ns, RESULTS_DIR)