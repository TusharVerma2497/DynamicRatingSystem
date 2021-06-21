#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess
#import psutil

def main():
    # exist=False
    # for i in psutil.process_iter():
    #     try:
    #         if i.name().lower() == 'memcached.exe':
    #             print(i)
    #             exist=True
    #     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    #         pass
    # if exist == False:
    #     os.system('START '+str(os.getcwd())+'\\'+'memcached.exe -m 512 -vvv')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dynamicRatingSystem.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
