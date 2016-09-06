#!/usr/bin/env python

import os, sys, glob, fnmatch, imp, py_compile
import argparse
import ConfigParser

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-c", "--config_mode", dest="config_mode", help="If set, script sets up a default config file, and writes it", action="store_true")
    parser.add_argument("-f", "--config_file", dest="config_filename", help="Name of config file to use. Defaults to default.config")
    args = parser.parse_args()

    if ( not args.config_filename ):
        args.config_filenam = 'default.config'

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
                        config_functions[filename[:-3]] = config_func
                        analysis_func = getattr(module, '%s_analysis'%(filename[:-3]))
                        analysis_functions[filename[:-3]] = analysis_func

    if ( args.config_mode ):
        configs = ConfigParser.SafeConfigParser()
        for pkg, func in config_functions.items():
            print " -- Calling config for: %s"%(pkg)
            func(configs)

        with open('default.config', 'w+') as configfile:
            configs.write(configfile)
    else:
        configs = ConfigParser.SafeConfigParser()
        configs.read( args.config_filename )
        for pkg, func in analysis_functions.items():
            perform = configs.get( pkg, 'perform')

            if ( perform == 'true' ):
                print " -- Calling analysis for: %s"%(pkg)
                func()
            else:
                print " -- Analysis for %s is disabled"%(pkg)

# vim: et ts=4 sts=4
