import argparse
import os
from pathlib import Path
from api_resources import api_resources
from dump_builder import namespaces as ns
from dump_builder import cluster_wide_dump as cwd

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

    parser.add_argument('-l', '--list', action='store_true', help='print all available api resources in cluster')

    args = parser.parse_args()
    
    # store user inputs in variables
    list_api_arg = args.list
    input_ns = args.namespace
    input_kind = args.kind
    
    print('use -h to see all available options')

    # print all api resources in cluster
    if list_api_arg:
        api_list = api_resources.api_resources()
        for i in range(len(api_list)):
            print(api_list[i])
    
    # make a decision bases on command line arguments
    if input_ns == None and input_kind == None:
        ns_list = ns.get_user_namespaces(RESULTS_DIR)
        namespaced_api = api_resources.namespaced_resources()
        cwd.cluster_wide_dump(ns_list, namespaced_api,RESULTS_DIR)

if __name__ == "__main__":
    main()
