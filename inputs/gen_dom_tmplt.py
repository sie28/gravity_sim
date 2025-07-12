import os

import pandas as pd


def gen_dom_tmplt():

    data = {'id':['X'], 'colour':['X'], 'static':['X'], 'mass':['X'], 'loc_x':['X'], 'loc_y':['X'], 'vel_x':['X'], 'vel_y':['X']}
    domain = pd.DataFrame(data)

    cwd = os.getcwd()
    inputs_dir = os.path.join(cwd, 'inputs')
    tmplt_name = os.path.join(inputs_dir, 'domain_template.json')

    if os.path.exists(tmplt_name):
        os.remove(tmplt_name)

    domain.to_json(tmplt_name, orient='records', indent=4)

if __name__ == '__main__':
    gen_dom_tmplt()