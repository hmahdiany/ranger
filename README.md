# Ranger project

Ranger project makes migration easier from one Kubernetes cluster to another one. It is useful to create a dump from all manifests which has been applied in all user defined namespaces orother cluster wide objects. All dumps will be saved in `dump` directory.

## How to use
Ranger supports some options to create dump files based on user input arguments. Here are available cli options:

| Option | Description |
| --- | --- |
| -h, --help | prints help output and all available options |
| -l, --list | prints all available api resources in cluster |
| -ns, --namespace | specify target namespaces, could be more than one namespace seperated by space (if not specified all user defined namespaces will be dumped) |
| --kind | specify target kinds, could be more than one seperated by space (if not specified all kinds in a namespace will be dumped) |

## Examples
- dump all kinds in all user defined namespaces:
  - python3 ranger.py

- dump all kinds in `gitlab` and `ingress-nginx` namespaces:
  - python3 ranger.py --namespace gitlab ingress-nginx

- dump only `services` and `configmaps` in all user defined namespaces:
  - python3 ranger.py --kind services configmaps

- dump `deployments` and `secrets` in `gitlab` namespace
  - python3 ranger.py --namespace gitlab --kind deployments secrets
