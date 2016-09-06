#!/usr/bin/env python

import os, sys, glob, fnmatch, imp, py_compile

script_path = os.path.abspath(__file__)

configs = {}
analyses = {}

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
                    configs[match] = config_func
                    analysis_func = getattr(module, '%s_analysis'%(filename[:-3]))
                    analyses[match] = analysis_func

for pkg, func in configs.items():
    print " -- Calling config for: %s"%(pkg)
    func()


for pkg, func in analyses.items():
    print " -- Calling analysis for: %s"%(pkg)
    func()

# vim: et ts=4 sts=4
