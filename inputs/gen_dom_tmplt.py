import os

import pandas as pd


def gen_dom_tmplt():

    columns = ['id', 'colour', 'static', 'mass', 'loc_x', 'loc_y', 'vel_x', 'vel_y']
    domain = pd.DataFrame(columns=columns)

    cwd = os.getcwd()
    inputs_dir = os.path.join(cwd, 'inputs')
    tmplt_name = os.path.join(inputs_dir, 'domain_template.csv')

    if os.path.exists(tmplt_name):
        os.remove(tmplt_name)

    domain.to_csv(tmplt_name, index=False)