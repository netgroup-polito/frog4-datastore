#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line

version = '1.0'

if __name__ == "__main__":

    if sys.argv[1] == "runserver":
        import logging
        from ConfigParser import SafeConfigParser

        i = 1
        confFile = None
        for param in sys.argv:
            if param == "--d":
                if len(sys.argv) > i:
                    confFile = sys.argv[i]
                    break
                else:
                    print("Wrong params usage --d [conf-file]")
                    os.exit(1)
            i = i + 1
        parser = SafeConfigParser()
        if confFile is not None:
            parser.read(confFile)
        else:
            confFile = "config/default-config.ini"
            parser.read(confFile)
        os.environ.setdefault("DATASTORE_CONFIG_FILE", confFile)
        logging.basicConfig(filename=parser.get('logging', 'filename'), format='%(asctime)s %(levelname)s:%(message)s',
                            level=parser.get('logging', 'level'))
        addr = parser.get('rest_server', 'address')
        port = parser.get('rest_server', 'port')
        params = []
        params.append(sys.argv[0])
        params.append(sys.argv[1])
        params.append(addr + ":" + str(port))
        logging.info('Running \'FROG v.4 datastpore\' with version %s', version)
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datastore_main.settings")
        execute_from_command_line(params)

    else:
        os.environ.setdefault("DATASTORE_CONFIG_FILE", "config/default-config.ini")
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datastore_main.settings")
        execute_from_command_line(sys.argv)
