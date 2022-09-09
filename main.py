import os
from pathlib import Path
import v1

def main():
    # set base directory and create results directory
    BASE_DIR = Path(__file__).resolve().parent
    RESULTS_DIR = 'results'

    if os.path.exists(BASE_DIR/RESULTS_DIR):
        print(RESULTS_DIR, 'directory already exists')
    else:
        print('creating', RESULTS_DIR, 'directory')
        os.mkdir(BASE_DIR/RESULTS_DIR)

    # use namespaces package to get all user namespaces 
    # and create yaml file for them
    all_ns = v1.namespaces.get_user_namespaces()
    v1.namespaces.create_namespace_yaml_file(all_ns, RESULTS_DIR)

if __name__ == "__main__":
    main()
