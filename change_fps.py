import os
from simulation.read_json import read_json


domain_name = 'domain_sample_bounce'
new_fps = 2000

cwd = os.getcwd()
dom_dir = os.path.join(cwd, 'outputs', domain_name)

in_file = os.path.join(dom_dir, 'dom_data.json')

domain = read_json(f'{domain_name}_fps_{new_fps}', in_file)
domain.in_params['fps'] = new_fps

for obj in domain.objects:
    obj_data_file = os.path.join(dom_dir, f'obj_{obj.id}.json')
    obj.import_results(obj_data_file)

domain.export()
domain.visualise()