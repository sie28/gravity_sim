import os

import pandas as pd
import json


def gen_dom_tmplt():

    in_param = {'dt': 1, 't_end': 10, 'fps': 250}

    obj_data = {'id':[1, 2], 'colour':['b', 'r'], 'static':['FALSE', 'FLASE'], 'mass':[1, 1], 'loc':[[0, 0], [1, 0]], 'vel':[[0, 0], [0, 0]]}
    obj_df = pd.DataFrame(obj_data)
    json_df = obj_df.to_dict(orient='records')

    json_data = {'in_param': in_param, 'objects': json_df}

    cwd = os.getcwd()
    inputs_dir = os.path.join(cwd, 'inputs')
    tmplt_name = os.path.join(inputs_dir, 'domain_template.json')

    if os.path.exists(tmplt_name):
        os.remove(tmplt_name)

    with open(tmplt_name, 'w') as f:
        json.dump(json_data, f, indent=2)

if __name__ == '__main__':
    gen_dom_tmplt()