import pandas as pd
import numpy as np
from itertools import combinations
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import os


class Simulation:
    
    def __init__(self, t_list, domains):
        self.t_list = t_list
        self.domains = domains

    def begin(self):
        
        for t0, t1 in zip(self.t_list, self.t_list[1:]):
            dt = t1-t0
            
            for domain in self.domains:
                domain.timestep(dt)

    def visualise(self, fps):

        for domain in self.domains:
            domain.visualise(fps)

    def export(self):

        for domain in self.domains:
            domain.export()


class Domain:
    
    def __init__(self, id, objects):
        self.id = id
        self.objects = objects

        cwd = os.getcwd()
        self.dir = os.path.join(cwd, id)

    def calc_acc(self):

        G = 6.6743*(10**-11)

        acc_dict = {}
        for obj in self.objects:
            acc_dict[obj] = [0, 0]

        for obj_pair in combinations(self.objects, 2):
            obj_1 = obj_pair[0]
            obj_2 = obj_pair[1]
            [dist, ang] = obj_1.calc_dist_ang(obj_2)

            coeff = G/(dist**2)
            x_coeff = np.cos(ang)*coeff
            y_coeff = np.sin(ang)*coeff

            x_acc_1 = x_coeff*obj_2.m
            y_acc_1 = y_coeff*obj_2.m

            x_acc_2 = -x_coeff*obj_1.m
            y_acc_2 = -y_coeff*obj_1.m

            old_acc_obj_1 = acc_dict[obj_1]
            old_acc_obj_2 = acc_dict[obj_2]

            acc_dict[obj_1] = [old_acc_obj_1[0] + x_acc_1, old_acc_obj_1[1] + y_acc_1]
            acc_dict[obj_2] = [old_acc_obj_2[0] + x_acc_2, old_acc_obj_2[1] + y_acc_2]

        return acc_dict

    def move_objs(self, acc_dict, dt):
        
        for obj in self.objects:
            acc = acc_dict[obj]
            obj.move(dt, acc)

    def timestep(self, dt):
        
        acc_dict = self.calc_acc()
        self.move_objs(acc_dict, dt)
        
    def visualise(self, fps):
        
        def get_frame_data(frame_idx):
            xs, ys, dxdts, dydts = [], [], [], []
            for obj in self.objects:
                row = obj.df.iloc[frame_idx]
                xs.append(row['x'])
                ys.append(row['y'])
                dxdts.append(row['dxdt'])
                dydts.append(row['dydt'])
            return np.array(xs), np.array(ys), np.array(dxdts), np.array(dydts)

        def init():
            scat.set_offsets(np.zeros((n_objects, 2)))
            scat.set_color(colours)
            quiver.set_offsets(np.zeros((n_objects, 2)))
            quiver.set_UVC(np.zeros(n_objects), np.zeros(n_objects))
            return scat, quiver
        
        def update(frame_idx):
            xs, ys, dxdts, dydts = get_frame_data(frame_idx)
            scat.set_offsets(np.c_[xs, ys])
            quiver.set_offsets(np.c_[xs, ys])
            quiver.set_UVC(dxdts, dydts)
            return scat, quiver

        n_objects = len(self.objects)
        n_frames = len(self.objects[0].df['t'])
        colours = []
        for obj in self.objects:
            colours.append(obj.col)

        xs_0, ys_0, dxdts_0, dydts_0 = get_frame_data(0)

        fig, ax = plt.subplots()

        x_min, x_max, y_min, y_max = self.find_xy_bounds()
        x_lower = x_min - 1/2*(x_max-x_min)
        x_upper = x_max + 1/2*(x_max-x_min)
        y_lower = y_min - 1/2*(y_max-y_min)
        y_upper = y_max + 1/2*(y_max-y_min)
        ax.set_xlim(x_lower, x_upper)
        ax.set_ylim(y_lower, y_upper)
        
        scat = ax.scatter(xs_0, ys_0)
        quiver = ax.quiver(xs_0, ys_0, dxdts_0, dydts_0, scale=0.005, scale_units='xy', angles='xy')
        
        ani = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=True)
        file = os.path.join(self.dir, f'movement_fps={fps}.mp4')
        ani.save(file, fps=fps)

    def find_xy_bounds(self):
        
        all_xs = []
        all_ys = []
        
        for obj in self.objects:
            
            xs = obj.df['x']
            ys = obj.df['y']
            all_xs.append(xs)
            all_ys.append(ys)

            min_x = np.min(all_xs)
            max_x = np.max(all_xs)
            min_y = np.min(all_ys)
            max_y = np.max(all_ys)

        return min_x, max_x, min_y, max_y

    def export(self):

        os.makedirs(self.dir, exist_ok=True)

        for file in os.listdir(self.dir):
            os.remove(os.path.join(self.dir, file))

        for obj in self.objects:
            file = os.path.join(self.dir, f'obj_{obj.id}.csv')
            obj.df.to_csv(file, index=False)


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

    in_file_names = ['domain_5']

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

    t_end = 25000
    dt = 2
    t_n = np.ceil(t_end/dt + 1)

    t_list = np.linspace(0, t_end, int(t_n))

    simulation = Simulation(t_list, domains)
    simulation.begin()
    simulation.export()

    fps = 250
    simulation.visualise(fps)


    # i = 4

    # if i==1:
    #     t_list = np.linspace(0, 2000, 2001)
    #     obj_1 = Object(1, 'b', static=False, m=10**3, loc=[10, 0], vel=[0, 0.058])
    #     obj_2 = Object(2, 'r', static=True, m=5*10**8, loc=[0, 0], vel=[0, 0])
    #     objects = [obj_1, obj_2]
    # elif i==2:
    #     t_list = np.linspace(0, 2000, 2001)
    #     obj_1 = Object(1, 'b', static=False, m=5*10**7, loc=[10, 0], vel=[0, 0.058])
    #     obj_2 = Object(2, 'r', static=False, m=5*10**8, loc=[0, 0], vel=[0, 0])
    #     objects = [obj_1, obj_2]
    # elif i==3:
    #     t_list = np.linspace(0, 10000, 10001)
    #     obj_1 = Object(1, 'b', static=False, m=1*10**6, loc=[1, 0], vel=[0, 0.005])
    #     obj_2 = Object(2, 'r', static=False, m=1*10**6, loc=[0, 0], vel=[0, -0.005])
    #     objects = [obj_1, obj_2]
    # elif i==4:
    #     t_list = np.linspace(0, 500, 2501)
    #     obj_1 = Object(1, 'b', static=False, m=3*10**4, loc=[0, 0], vel=[0, 0.0005])
    #     obj_2 = Object(2, 'r', static=False, m=1*10**4, loc=[1, 0], vel=[-0.005, 0])
    #     obj_3 = Object(3, 'g', static=False, m=3*10**5, loc=[0, 1], vel=[0.005, 0])
    #     obj_4 = Object(4, 'k', static=False, m=3*10**5, loc=[1, 1], vel=[0, -0.0005])
    #     objects = [obj_1, obj_2, obj_3, obj_4]


    # domain = Domain(i, objects)
    # domains = [domain]
    # simulation = Simulation(t_list, domains)
    # simulation.begin()
    # simulation.export()
    # fps = 100
    # simulation.visualise(fps)