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

def dump_namespace(result_dir, input_ns = None):
    """
    this function creates a dump for all namespaces which are in input list
    """

    if input_ns is None:
        print("dumping all namespaces in cluster")
        all_ns = namespaces.get_user_namespaces()
        namespaces.create_namespace_yaml_file(all_ns, result_dir)
        return all_ns
    else:
        print("dumping", input_ns, "namespaces")
        namespaces.create_namespace_yaml_file(input_ns, result_dir)

def cluster_wide_dump(result_dir):
    """
    this function dumps all kinds in all user defined namespaces
    it us used when no input arguments are spcecified by client
    """

    all_ns = dump_namespace(result_dir)

    print("dumping configmaps in all namespaces")
    configmaps.get_configmaps(all_ns, result_dir)

    print("dumping cronjobs in all namespaces")
    cronjobs.get_cronjobs(all_ns, result_dir)

    print("dumping deployments in all namespaces")
    deployments.get_deployments(all_ns, result_dir)

    print("dumping ingresses in all namespaces")
    ingresses.get_ingresses(all_ns, result_dir)

    print("dumping secrets in all namespaces")
    secrets.get_secrets(all_ns, result_dir)

    print("dumping services in all namespaces")
    services.get_services(all_ns, result_dir)

def partial_kind_dump(input_kind, result_dir):
    """
    this function dumps some kinds which are specified as input argument
    in all namespaces
    """

    all_ns = dump_namespace(result_dir)

    for kind in input_kind:
        if kind == 'configmaps':
            print("dumping configmaps in all namespaces")
            configmaps.get_configmaps(all_ns, result_dir)

        elif kind == 'cronjobs':
            print("dumping cronjobs in all namespaces")
            cronjobs.get_cronjobs(all_ns, result_dir)

        elif kind == 'deployements':
            print("dumping deployments in all namespaces")
            deployments.get_deployments(all_ns, result_dir)

        elif kind == 'ingresses':
            print("dumping ingresses in all namespaces")
            ingresses.get_ingresses(all_ns, result_dir)

        elif kind == 'secrets':
            print("dumping secrets in all namespaces")
            secrets.get_secrets(all_ns, result_dir)

        elif kind == 'services':
            print("dumping services in all namespaces")
            services.get_services(all_ns, result_dir)

        else:
            print(kind, 'is not a valid kind')

def namespace_wide_dump(input_ns, result_dir):
    """
    this function dumps all kinds in some namespaces which are specified
    as input argument
    """
    
    dump_namespace(result_dir, input_ns)

    print("dumping configmaps in ", input_ns, "namespaces")
    configmaps.get_configmaps(input_ns, result_dir)

    print("dumping cronjobs in ", input_ns, "namespaces")
    cronjobs.get_cronjobs(input_ns, result_dir)

    print("dumping deployments in ", input_ns, "namespaces")
    deployments.get_deployments(input_ns, result_dir)

    print("dumping ingresses in ", input_ns, "namespaces")
    ingresses.get_ingresses(input_ns, result_dir)

    print("dumping secrets in ", input_ns, "namespaces")
    secrets.get_secrets(input_ns, result_dir)

    print("dumping services in ", input_ns, "namespaces")
    services.get_services(input_ns, result_dir)

def partial_namespace_dump(input_ns, input_kind, result_dir):
    """
    this function dumps some kinds in some namespaces
    """
    
    dump_namespace(result_dir, input_ns)

    for kind in input_kind:
        if kind == 'configmaps':
            print("dumping configmaps in all namespaces")
            configmaps.get_configmaps(input_ns, result_dir)

        elif kind == 'cronjobs':
            print("dumping cronjobs in all namespaces")
            cronjobs.get_cronjobs(input_ns, result_dir)

        elif kind == 'deployements':
            print("dumping deployments in all namespaces")
            deployments.get_deployments(input_ns, result_dir)

        elif kind == 'ingresses':
            print("dumping ingresses in all namespaces")
            ingresses.get_ingresses(input_ns, result_dir)

        elif kind == 'secrets':
            print("dumping secrets in all namespaces")
            secrets.get_secrets(input_ns, result_dir)

        elif kind == 'services':
            print("dumping services in all namespaces")
            services.get_services(input_ns, result_dir)

        else:
            print(kind, 'is not a valid kind')

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
    
    if input_ns == None and input_kind == None:
        cluster_wide_dump(RESULTS_DIR)

    elif input_ns == None and input_kind != None:
        partial_kind_dump(input_kind, RESULTS_DIR)

    elif input_ns != None and input_kind == None:
        namespace_wide_dump(input_ns, RESULTS_DIR)

    else:
        partial_namespace_dump(input_ns, input_kind, RESULTS_DIR)

if __name__ == "__main__":
    main()
