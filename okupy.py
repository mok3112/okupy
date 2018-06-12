#!/usr/bin/env python3

import os
import sys
from importlib import import_module
from multiprocessing import Pool, Queue, Manager

from settings import APPS, ARGS, KWARGS
from src.utils.times import str_to_secs
from src.utils.processes import run_apps, sleep_process


def main():
    if len(sys.argv) != 2:
        # Invalid invocation.
        print('Error: Usage is ./okupy <time>')
        sys.exit(1)

    secs = str_to_secs(sys.argv[1])
    
    if (secs == -1):
        # Invalid time input.
        print('Invalid time input. Suffixes of \'s\', \'m\', or \'h\' are allowed.')
        sys.exit(1)
    
    """
    The code below is used to import the classes from the settings.py file.
    We can then instantiate the classes however we want by just iterating over
    the list.

    The app list should be passed over to another thread that actually runs 
    the applications in the background.
    """
    app_list = []
    for app_name in APPS:
        module = import_module(APPS.get(app_name))
        app = getattr(module, app_name)
        app_list.append(app)
    print(app_list)

    print('okupy pid is {}'.format(os.getpid()))

    manager = Manager()
    queue = manager.Queue()

    pool = Pool(processes=2)
    pool.apply_async(sleep_process, args=(secs, queue))
    pool.apply(run_apps, args=(app_list, ARGS, KWARGS, queue))
    
    
    
    
    

if __name__ == '__main__':
    main()
