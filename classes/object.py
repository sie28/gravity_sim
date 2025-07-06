import numpy as np
import pandas as pd

class Object:

    def __init__(self, id, col, static, m, loc, vel):
        
        x = loc[0]
        y = loc[1]
        dxdt = vel[0]
        dydt = vel[1]

        df = pd.DataFrame({'t': [0], 'x': [x], 'y': [y], 'dxdt': [dxdt], 'dydt': [dydt]})

        self.id = id
        self.col = col
        self.static = static
        self.m = m
        self.df = df
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        return isinstance(other, Object) and self.id == other.id

    def calc_dist_ang(self, other):
        
        x_list = []
        y_list = []
        
        for obj in [self, other]:
            row = obj.df.iloc[-1]
            x = row['x']
            x_list.append(x)
            y = row['y']
            y_list.append(y)

        dx = x_list[1]-x_list[0]
        dy = y_list[1]-y_list[0]
        
        dist = np.sqrt( (dx)**2 + (dy)**2 )

        pi = np.pi

        if dx == 0:
            if dy == 0:
                ang = 0
            if dy > 0:
                ang = 1/2 * pi
            else:
                ang = 3/2 * pi
        if dx > 0:
            if dy >= 0:
                ang = np.arctan(dy/dx)
            else:
                ang = 2*pi + np.arctan(dy/dx)
        if dx < 0:
            ang = pi +  np.arctan(dy/dx)

        return [dist, ang]
    
    def move(self, dt, acc):

        row = self.df.iloc[-1]

        t_init = row['t']
        t_end = t_init + dt

        x_init = row['x']
        y_init = row['y']

        if self.static == True:
            x_end = x_init
            y_end = y_init
            dxdt_end = 0
            dydt_end = 0

        else:
            dxdt_init = row['dxdt']
            dydt_init = row['dydt']

            d2xdt2 = acc[0]
            d2ydt2 = acc[1]
    
            dxdt_end = dxdt_init + d2xdt2*dt
            dxdt_mid = (dxdt_init + dxdt_end)/2

            dydt_end = dydt_init + d2ydt2*dt
            dydt_mid = (dydt_init + dydt_end)/2

            x_end = x_init + dxdt_mid*dt
            y_end = y_init + dydt_mid*dt

        new_row = pd.DataFrame([{ 't': t_end, 'x': x_end, 'y': y_end, 'dxdt': dxdt_end, 'dydt': dydt_end }])

        self.df = pd.concat([self.df, new_row], ignore_index=True)