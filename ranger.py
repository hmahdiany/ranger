import argparse
import os
from pathlib import Path
from api_resources import api_resources
from dump_builder import namespaces as ns
from dump_builder import cluster_wide_dump as cwd
from dump_builder import partial_kind_dump as pkd
from dump_builder import namespace_wide_dump as nwd
from dump_builder import partial_namespace_dump as pnd

def main():
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
        cluster_wide_api_list = [*set(api_resources.cluster_wide_resources())] # *set removes duplicate values in a list
        print("*****Cluster wide api resources*****")
        for i in range(len(cluster_wide_api_list)):
            print(cluster_wide_api_list[i])
        print("-" * 20)

        namespaced_wide_api_list = [*set(api_resources.namespaced_resources())] # *set removes duplicate values in a list
        print("*****Namespaced wide api resources*****")
        for i in range(len(namespaced_wide_api_list)):
            print(namespaced_wide_api_list[i])
    else:
        # set base directory and create results directory
        BASE_DIR = Path(__file__).resolve().parent
        RESULTS_DIR = 'dump'

        if os.path.exists(BASE_DIR/RESULTS_DIR):
            print(RESULTS_DIR, 'directory already exists')
        else:
            print('creating', RESULTS_DIR, 'directory')
            os.mkdir(BASE_DIR/RESULTS_DIR)
    
        # make a decision based on command line arguments

        # create a cluster dump if no input argument is passed through command line
        if input_ns == None: 
            ns_list = ns.get_user_namespaces(RESULTS_DIR)
            ns.create_namespace_yaml_file(ns_list, RESULTS_DIR)
            namespaced_api = api_resources.namespaced_resources()

            if input_kind == None:
                cwd.cluster_wide_dump(ns_list, namespaced_api, RESULTS_DIR)

            # create a dump for specific kinds which are passed through --kind command line object
            elif input_kind != None:
                for kind in input_kind:
                    if kind not in namespaced_api:
                        print(kind, "is not a namespaced api")
                        input_kind.remove(kind)
                    
                pkd.partial_kind_dump(ns_list, input_kind, RESULTS_DIR)

        elif input_ns != None:
            ns_list = ns.get_user_namespaces(RESULTS_DIR)
            for namespace in input_ns:
                if namespace not in ns_list:
                    print(namespace, "namespace does not exists")
                    input_ns.remove(namespace)
            ns.create_namespace_yaml_file(input_ns, RESULTS_DIR)

            namespaced_api = api_resources.namespaced_resources()

            if input_kind == None:
                nwd.namespace_wide_dump(input_ns, namespaced_api, RESULTS_DIR)

            elif input_kind != None:
                for kind in input_kind:
                    if kind not in namespaced_api:
                        print(kind, "is not a namespaced api")
                        input_kind.remove(kind)
                pnd.partial_namespace_dump(input_ns, input_kind, RESULTS_DIR)
    

if __name__ == "__main__":
    main()
