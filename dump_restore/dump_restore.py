import os
from pathlib import Path
import subprocess


def restore(ns_list, kind_list, kubeconfig):

    # convert kubeconfig from posix path to string so it cloud be concatenate
    KUBECONFIG = str(kubeconfig)

    # set base directory and dump folder
    DUMP_FOLDER = "dump"

    # check if kubeconfig exists
    if os.path.exists(kubeconfig):
        pass
    
    else:
        print(kubeconfig, "file not found")

    # create namespace first
    for ns in ns_list: 
        path = str(DUMP_FOLDER + "/" + ns + '/namespace.yaml')
        
        print("***creating namespaces")
        cmd = "kubectl --kubeconfig " + KUBECONFIG + " create -R -f " + path
        applied_ns = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        output, error = applied_ns.communicate()
        if error:
            print("an error occured: ", error.decode('ascii'))

