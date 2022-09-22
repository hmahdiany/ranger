from . import namespaces as getns
from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def get_secrets(all_namespaces, result_dir):
    """
    this function dumps all secrets in user's namespaces
    it uses namespaces module from v1 package
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir
    SECRETS_DIR = "secrets"
    
    for ns in all_namespaces:

        # create a directory named secrets to store all confimaps
        # in a namespace
        if os.path.exists(BASE_DIR/RESULTS_DIR/ns/SECRETS_DIR):
            print(SECRETS_DIR, 'directory already exists')
        else:
            print('creating', ns, 'directory')
            os.mkdir(BASE_DIR/RESULTS_DIR/ns/SECRETS_DIR)

        # create an empty list to list all secrets in a namespace
        all_secrets = []

        # execute command line to append all secrets in a namespace
        # to all_secrets list
        get_secrets = "kubectl get secrets -n " + ns + "| grep -v 'NAME' | awk '{print $1}'"
        secrets_cmd = subprocess.Popen(get_secrets, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = secrets_cmd.communicate()

        if error:
            print("an error occured: ", error.decode('ascii'))

        # append all secrets in a namespace to all_secrets list
        for i in output.decode('ascii').split('\n'):
            if i != '':
                all_secrets.append(i)

        # iterate through all_confimaps list to dump all confimaps in a namespace
        for secret in all_secrets:

            # execute command line to get user's namespaces in json format
            # and convert it to yaml format
            cmd = "kubectl get secrets -o json -n " + ns + " " + secret
            get_secret = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output, error = get_secret.communicate()
            try:
                json_obj = json.loads(output.decode('ascii'))
                secret_name = json_obj['metadata']['name'] + '.yaml'
                del json_obj['metadata']['resourceVersion']
                del json_obj['metadata']['creationTimestamp']
                del json_obj['metadata']['uid']
                with open(os.path.join(BASE_DIR/RESULTS_DIR/ns/SECRETS_DIR, secret_name), 'w') as f:
                    yaml.dump(json_obj, f)
            except:
                print(error)

if __name__ == "__main__":

    # define result directory
    RESULTS_DIR = "results"

    all_ns = getns.get_user_namespaces()
    get_secrets(all_ns, RESULTS_DIR)