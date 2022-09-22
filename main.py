import os
from pathlib import Path
from v1 import namespaces
from v1 import configmaps

def main():
    # set base directory and create results directory
    BASE_DIR = Path(__file__).resolve().parent
    RESULTS_DIR = 'results'

    if os.path.exists(BASE_DIR/RESULTS_DIR):
        print(RESULTS_DIR, 'directory already exists')
    else:
        print('creating', RESULTS_DIR, 'directory')
        os.mkdir(BASE_DIR/RESULTS_DIR)

    # use namespaces package to get all user's namespaces 
    # and create yaml file for them
    print("exporting all user's namespaces")
    all_ns = namespaces.get_user_namespaces()
    namespaces.create_namespace_yaml_file(all_ns, RESULTS_DIR)

    # Use configmaps package to get all configmaps in all namespaces
    # save them in results/<namespace name>/configmaps
    print("exporting configmaps in all namespaces")
    configmaps.get_configmaps(all_ns, RESULTS_DIR)


if __name__ == "__main__":
    main()
