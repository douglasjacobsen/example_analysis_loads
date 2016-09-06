def plotting_configs(configs):
    print " Setting up plotting configs"
    configs.add_section('plotting')
    configs.set('plotting', 'perform', 'false')
    configs.set('plotting', 'num_color_levels', '9')


def plotting_analysis():
    print " Plotting analysis"
