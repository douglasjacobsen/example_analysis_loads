#!/usr/bin/env python

def moc_configs(configs):
    print " Setting up MOC configs"
    configs.add_section('moc')
    configs.set('moc', 'perform', 'false')
    configs.set('moc', 'min_lat', '-90')
    configs.set('moc', 'max_lat', '90')

def moc_analysis():
    print " Performing up MOC analysis"
