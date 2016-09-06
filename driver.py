#!/usr/bin/env python

import os, sys, glob, fnmatch, imp, py_compile
import argparse
import ConfigParser

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--config_mode", dest="config_mode", help="If set, script sets up a default config file, and writes it", action="store_true")
    args = parser.parse_args()

    script_path = os.path.abspath(__file__)

    config_functions = {}
    analysis_functions = {}

    for root, dirnames, filenames in os.walk('.'):
        for dirname in dirnames:
            for subdir, subdirs, subfilenames in os.walk( os.path.join(root, dirname) ):
                for filename in fnmatch.filter(subfilenames, '*.py'):
                    if ( filename != "__init__.py" ):
                        match = os.path.join(subdir, filename)
                        package_name = "%s.%s"%( subdir[2:], filename[:-3])
                        print " Found: %s -- Packagename: %s"%(match, package_name)
                        package = __import__(package_name)
                        module = getattr(package, filename[:-3])
                        config_func = getattr(module, '%s_configs'%(filename[:-3]))
                        config_functions[match] = config_func
                        analysis_func = getattr(module, '%s_analysis'%(filename[:-3]))
                        analysis_functions[match] = analysis_func

    if ( args.config_mode ):
        configs = ConfigParser.SafeConfigParser()
        for pkg, func in config_functions.items():
            print " -- Calling config for: %s"%(pkg)
            func(configs)

        with open('default.config', 'w+') as configfile:
            configs.write(configfile)
    else:
        for pkg, func in analysis_functions.items():
            print " -- Calling analysis for: %s"%(pkg)
            func()

# vim: et ts=4 sts=4
