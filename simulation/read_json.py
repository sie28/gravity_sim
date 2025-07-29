# Standard library imports
import os

# Third-party imports
import pandas as pd
import json

# Local imports
from classes.domain import Domain
from classes.object import Object
from classes.simulation import Simulation


def read_json(dm, input_file):

        with open(input_file) as f:
            json_data = json.load(f)

        in_param = json_data['in_param']

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

        return Domain(dm, in_param, objects, input_file)