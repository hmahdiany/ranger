from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def get_services(all_namespaces, result_dir):
    """
    this function dumps all services in user's namespaces
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir
    SVC_DIR = "services"
    
    for ns in all_namespaces:

        # create a directory named services to store all confimaps
        # in a namespace
        if os.path.exists(BASE_DIR/RESULTS_DIR/ns/SVC_DIR):
            print(SVC_DIR, 'directory already exists')
        else:
            print('creating', SVC_DIR, 'directory for', ns, 'namespace')
            os.mkdir(BASE_DIR/RESULTS_DIR/ns/SVC_DIR)

        # create an empty list to list all services in a namespace
        all_services = []

        # execute command line to append all services in a namespace
        # to all_services list
        get_svc = "kubectl get svc -n " + ns + "| grep -v 'NAME' | awk '{print $1}'"
        svc_cmd = subprocess.Popen(get_svc, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = svc_cmd.communicate()

        if error:
            print("an error occured: ", error.decode('ascii'))

        # append all services in a namespace to all_services list
        for i in output.decode('ascii').split('\n'):
            if i != '':
                all_services.append(i)

        # iterate through all_services list to dump services in a namespace
        for svc in all_services:

            # execute command line to get user's namespaces in json format
            # and convert it to yaml format
            cmd = "kubectl get svc -o json -n " + ns + " " + svc
            get_svc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output, error = get_svc.communicate()
            try:
                json_obj = json.loads(output.decode('ascii'))
                svc_name = json_obj['metadata']['name'] + '.yaml'
                del json_obj['metadata']['resourceVersion']
                del json_obj['metadata']['creationTimestamp']
                del json_obj['metadata']['uid']
                del json_obj['spec']['clusterIP']
                del json_obj['spec']['clusterIPs']
                del json_obj['status']
                with open(os.path.join(BASE_DIR/RESULTS_DIR/ns/SVC_DIR, svc_name), 'w') as f:
                    yaml.dump(json_obj, f)
            except:
                print(error)
