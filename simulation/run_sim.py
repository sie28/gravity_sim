# Standard library imports
import os

# Third-party imports
import pandas as pd
import numpy as np
import json

# Local imports
from classes.domain import Domain
from classes.object import Object
from classes.simulation import Simulation


def run_sim(in_file_names):

    cwd = os.getcwd()
    inputs_dir = os.path.join(cwd, 'inputs')

    domains = []

    for dm in in_file_names:

        input_file = os.path.join(inputs_dir, f'{dm}.json')

        with open(input_file) as f:
            json_data = json.load(f)

        in_param = json_data['in_param']
        dt = in_param['dt']
        t_end = in_param['t_end']
        fps = in_param['fps']

        objects_df = pd.DataFrame(json_data['objects'])

        objects = []
        for row in objects_df.itertuples():
            id = row.id
            col = row.colour
            static = row.static
            m = row.mass
            loc = row.loc
            vel = row.vel
            obj = Object(id=id, col=col, static=static, m=m, loc=loc, vel=vel)
            objects.append(obj)

        domain = Domain(dm, objects)
        domains.append(domain)

    t_n = np.ceil(t_end/dt + 1)

    t_list = np.linspace(0, t_end, int(t_n))

    simulation = Simulation(t_list, domains)
    simulation.begin()
    simulation.export()

    simulation.visualise(fps)