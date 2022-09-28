from pathlib import Path
import os
import subprocess
import json
import yaml
from yaml.loader import SafeLoader

def dump_builder(ns_list, kind_list, result_dir):
    """
    create a dump for target kubernetes kinds
    """