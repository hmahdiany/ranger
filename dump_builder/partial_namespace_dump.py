from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def partial_namespace_dump(ns_list, kind_list, result_dir):
    """
    create a dump from specific kinds passed through --kind option in 
    specific namespaces passed through --namespace option
    """

    # set base directory and create namespaces directory
    BASE_DIR = Path(__file__).resolve().parent.parent
    RESULTS_DIR = result_dir

    for ns in ns_list:
        for kind in kind_list:
            
            TARGET_DIR = kind

            # create directory for each kind
            if os.path.exists(BASE_DIR/RESULTS_DIR/ns/TARGET_DIR):
                pass
            else:
                os.mkdir(BASE_DIR/RESULTS_DIR/ns/TARGET_DIR)

            # create an empty list for all objects in namespace
            object_list = []

            # execute command line to append all objects to object_list
            print("***getting all", kind, "objects in", ns, "namespace")
            obj_cmd = "kubectl get " + kind + " -n " + ns + "| grep -v 'NAME' | awk '{print $1}'"
            obj_list = subprocess.Popen(obj_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            output, error = obj_list.communicate()

            if error:
                print("an error occured: ", error.decode('ascii'))

                # append all configmaps in a namespace to object_list list
            for i in output.decode('ascii').split('\n'):
                if i != '':
                    object_list.append(i)

            # create dump
            for obj in object_list:
                
                kind_cmd = "kubectl get " + kind + " -o json -n " + ns + " " + obj
                get_kind = subprocess.Popen(kind_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
                output, error = get_kind.communicate()
                try:
                    json_obj = json.loads(output.decode('ascii'))
                    obj_name = json_obj['metadata']['name'] + '.yaml'
                    if obj_name == "kube-root-ca.crt.yaml" or obj_name == "kubernetes.yaml":
                        continue
                    del json_obj['metadata']['resourceVersion']
                    del json_obj['metadata']['creationTimestamp']
                    del json_obj['metadata']['uid']
                    if 'spec' in json_obj:
                        if 'clusterIP' in json_obj['spec']:
                            del json_obj['spec']['clusterIP']
                        if 'clusterIPs' in json_obj['spec']:
                            del json_obj['spec']['clusterIPs']
                    if 'status' in json_obj:
                        del json_obj['status']
                    with open(os.path.join(BASE_DIR/RESULTS_DIR/ns/TARGET_DIR, obj_name), 'w') as f:
                        yaml.dump(json_obj, f)
                except:
                    print("error: couldn't write dump file for ", obj, "of kind", kind, "in", ns, "namespace")