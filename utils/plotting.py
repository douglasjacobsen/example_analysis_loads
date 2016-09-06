def plotting_configs(configs):
    print " Setting up plotting configs"
    configs.add_section('plotting_generic')
    configs.set('plotting_generic', 'num_color_levels', '9')


def plotting_analysis():
    print " Plotting analysis"
