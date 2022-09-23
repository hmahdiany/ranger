from v1 import namespaces as getns
from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def get_deployments(all_namespaces, result_dir):
    """
    this function dumps all deployments in user's namespaces
    it uses namespaces module from v1 package
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir
    DEPLOY_DIR = "deployments"
    
    for ns in all_namespaces:

        # create a directory named deployments to store all confimaps
        # in a namespace
        if os.path.exists(BASE_DIR/RESULTS_DIR/ns/DEPLOY_DIR):
            print(DEPLOY_DIR, 'directory already exists')
        else:
            print('creating', DEPLOY_DIR, 'directory for', ns, 'namespace')
            os.mkdir(BASE_DIR/RESULTS_DIR/ns/DEPLOY_DIR)

        # create an empty list to list all deployments in a namespace
        all_deployments = []

        # execute command line to append all deployments in a namespace
        # to all_deployments list
        get_deploy = "kubectl get deploy -n " + ns + "| grep -v 'NAME' | awk '{print $1}'"
        deploy_cmd = subprocess.Popen(get_deploy, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = deploy_cmd.communicate()

        if error:
            print("an error occured: ", error.decode('ascii'))

        # append all deployments in a namespace to all_deployments list
        for i in output.decode('ascii').split('\n'):
            if i != '':
                all_deployments.append(i)

        # iterate through all_deployments list to dump all deployments in a namespace
        for deployment in all_deployments:

            # execute command line to get user's namespaces in json format
            # and convert it to yaml format
            cmd = "kubectl get deploy -o json -n " + ns + " " + deployment
            get_deploy = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output, error = get_deploy.communicate()
            try:
                json_obj = json.loads(output.decode('ascii'))
                deploy_name = json_obj['metadata']['name'] + '.yaml'
                del json_obj['metadata']['resourceVersion']
                del json_obj['metadata']['creationTimestamp']
                del json_obj['metadata']['uid']
                del json_obj['status']
                with open(os.path.join(BASE_DIR/RESULTS_DIR/ns/DEPLOY_DIR, deploy_name), 'w') as f:
                    yaml.dump(json_obj, f)
            except:
                print(error)

if __name__ == "__main__":

    # define result directory
    RESULTS_DIR = "results"

    all_ns = getns.get_user_namespaces()
    get_deployments(all_ns, RESULTS_DIR)