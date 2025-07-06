# Standard library imports
import os

# Third-party imports
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Local imports
from classes.domain import Domain
from classes.object import Object
from classes.simulation import Simulation


def gen_dom_tmplt():

    columns = ['id', 'colour', 'static', 'mass', 'loc_x', 'loc_y', 'vel_x', 'vel_y']
    domain = pd.DataFrame(columns=columns)

    cwd = os.getcwd()
    inputs_dir = os.path.join(cwd, 'inputs')
    tmplt_name = os.path.join(inputs_dir, 'domain_template.csv')

    if os.path.exists(tmplt_name):
        os.remove(tmplt_name)

    domain.to_csv(tmplt_name, index=False)
    

if __name__ == '__main__':

    in_file_names = ['domain_1']

    cwd = os.getcwd()
    inputs_dir = os.path.join(cwd, 'inputs')

    domains = []

    for dm in in_file_names:
        input_file = os.path.join(inputs_dir, f'{dm}.csv')
        objects_df = pd.read_csv(input_file, skip_blank_lines=True)

        objects = []

        for row in objects_df.itertuples():
            id = row.id
            col = row.colour
            static = row.static
            m = row.mass
            loc = [row.loc_x, row.loc_y]
            vel = [row.vel_x, row.vel_y]
            obj = Object(id=id, col=col, static=static, m=m, loc=loc, vel=vel)
            objects.append(obj)

        domain = Domain(dm, objects)
        domains.append(domain)

    t_end = 250
    dt = 2
    t_n = np.ceil(t_end/dt + 1)

    t_list = np.linspace(0, t_end, int(t_n))

    simulation = Simulation(t_list, domains)
    simulation.begin()
    simulation.export()

    fps = 250
    simulation.visualise(fps)
