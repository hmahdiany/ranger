import os
from pathlib import Path
from v1 import namespaces
from v1 import configmaps
from v1 import secrets
from v1 import services
from apps_v1 import deployments

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
    print("dumping all namespaces in cluster")
    all_ns = namespaces.get_user_namespaces()
    namespaces.create_namespace_yaml_file(all_ns, RESULTS_DIR)

    # use configmaps package to dump all configmaps in all namespaces
    # save them in results/<namespace name>/configmaps
    print("dumping configmaps in all namespaces")
    configmaps.get_configmaps(all_ns, RESULTS_DIR)

    # use secrets package to dump all secrets in all namespaces
    # save them in results/<namespace name>/secrets
    print("dumping secrets in all namespaces")
    secrets.get_secrets(all_ns, RESULTS_DIR)

    # use deployments package to dump all deployments in all namespaces
    # save them in results/<namespace name>/deployments
    print("dumping deployments in all namespaces")
    deployments.get_deployments(all_ns, RESULTS_DIR)

    # use services package to dump all services in all namespaces
    # save them in results/<namespace name>/services
    print("dumping services in all namespaces")
    services.get_services(all_ns, RESULTS_DIR)


if __name__ == "__main__":
    main()
