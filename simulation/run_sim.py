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
from simulation.read_json import read_json


def run_sim(in_file_names):

    cwd = os.getcwd()
    inputs_dir = os.path.join(cwd, 'inputs')

    domains = []

    for dm in in_file_names:
        
        input_file = os.path.join(inputs_dir, f'{dm}.json')

        domain = read_json(dm, input_file)
        domains.append(domain)

    simulation = Simulation(domains)
    print(domains) ###
    simulation.begin()
    simulation.export()

    simulation.visualise()