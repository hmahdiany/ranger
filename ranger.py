import argparse
import os
from pathlib import Path
from v1 import namespaces
from v1 import configmaps
from v1 import secrets
from v1 import services
from apps_v1 import deployments
from batch_v1 import cronjobs
from networking_k8s_io_v1 import ingresses

def main():
    # set base directory and create results directory
    BASE_DIR = Path(__file__).resolve().parent
    RESULTS_DIR = 'dump'

    if os.path.exists(BASE_DIR/RESULTS_DIR):
        print(RESULTS_DIR, 'directory already exists')
    else:
        print('creating', RESULTS_DIR, 'directory')
        os.mkdir(BASE_DIR/RESULTS_DIR)

    # parse input arguments
    # valid arguments are --namespace followed by a list of namespaces. if not specified all namespaces will be considered.
    # and --kind followed by a list of Kubernetes kind to dump. if not specified all kinds will be dumped
    parser = argparse.ArgumentParser(description='dump k8s manifests', allow_abbrev=False, prog='ranger', usage='ranger [options] value')

    parser.add_argument('-ns', '--namespace', metavar='name', nargs='+', help='namespace name [could be a list seperated by space] if not specified all namespaces will be used')

    parser.add_argument('--kind', nargs='+',  help='kind name [could be a list seperated by space] if not specified all kinds in a namespace will be dumped')

    args = parser.parse_args()
    
    # store user inputs in variables
    input_ns = args.namespace
    input_kind = args.kind
    

    # use namespaces module to get all user's namespaces 
    # and create yaml file for them
    if input_ns == None:
        print("dumping all namespaces in cluster")
        all_ns = namespaces.get_user_namespaces()
        namespaces.create_namespace_yaml_file(all_ns, RESULTS_DIR)
    else:
        print("dumping", input_ns, "namespaces")
        namespaces.create_namespace_yaml_file(input_ns, RESULTS_DIR)

    # use configmaps module to dump all configmaps in all namespaces
    # save them in results/<namespace name>/configmaps
    if input_ns == None:
        print("dumping configmaps in all namespaces")
        configmaps.get_configmaps(all_ns, RESULTS_DIR)
    else:
        print("dumping configmaps in ", input_ns, "namespaces")
        configmaps.get_configmaps(input_ns, RESULTS_DIR)
    
    # use secrets module to dump all secrets in all namespaces
    # save them in results/<namespace name>/secrets
    if input_ns == None:
        print("dumping secrets in all namespaces")
        secrets.get_secrets(all_ns, RESULTS_DIR)
    else:
        secrets.get_secrets(input_ns, RESULTS_DIR)

    # use deployments module to dump all deployments in all namespaces
    # save them in results/<namespace name>/deployments
    if input_ns == None:
        print("dumping deployments in all namespaces")
        deployments.get_deployments(all_ns, RESULTS_DIR)
    else:
        deployments.get_deployments(input_ns, RESULTS_DIR)

    # use services module to dump all services in all namespaces
    # save them in results/<namespace name>/services
    if input_ns == None:
        print("dumping services in all namespaces")
        services.get_services(all_ns, RESULTS_DIR)
    else:
        services.get_services(input_ns, RESULTS_DIR)

    # use ingresses module to dump all ingresses in all namespaces
    # save them in results/<namespace name>/ingresses
    if input_ns == None:
        print("dumping ingresses in all namespaces")
        ingresses.get_ingresses(all_ns, RESULTS_DIR)
    else:
        ingresses.get_ingresses(input_ns, RESULTS_DIR)

    # use cronjobs module to dump all cronjobs in all namespaces
    # save them in results/<namespace name>/cronjobs
    if input_ns == None:
        print("dumping cronjobs in all namespaces")
        cronjobs.get_cronjobs(all_ns, RESULTS_DIR)
    else:
        cronjobs.get_cronjobs(input_ns, RESULTS_DIR)


if __name__ == "__main__":
    main()
