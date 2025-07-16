# Standard library imports
import os

# Third-party imports
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import matplotlib as mpl
mpl.rcParams['animation.ffmpeg_path'] = os.path.join('C:', 'ffmpeg', 'bin', 'ffmpeg.exe')


class Domain:
    
    def __init__(self, id, in_params, objects):
        self.id = id
        self.in_params = in_params
        self.objects = objects

        self.extract_walls()

        cwd = os.getcwd()
        self.dir = os.path.join(cwd, 'outputs', id)

    def extract_walls(self):
        self.x_wall_lower = self.in_params['x_wall_lower']
        self.x_wall_upper = self.in_params['x_wall_upper']
        self.y_wall_lower = self.in_params['y_wall_lower']
        self.y_wall_upper = self.in_params['y_wall_upper']

    def begin(self):

        t_end = self.in_params['t_end']
        dt = self.in_params['dt']

        t_n = np.ceil(t_end/dt + 1)
        self.t_list = np.linspace(0, t_end, int(t_n))

        for t0, t1 in zip(self.t_list, self.t_list[1:]):
            self.timestep(dt)

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

    def check_bounce(self):

        for obj in self.objects:
            
            if self.x_wall_lower != None or self.x_wall_upper != None:
                x_loc = obj.df['x'].iloc[-1]
                x_vel = obj.df['dxdt'].iloc[-1]

                if self.x_wall_lower != None:
                    if x_loc < self.x_wall_lower:
                        obj.df.loc[obj.df.index[-1], 'dxdt'] = np.max([x_vel, -x_vel])

                if self.x_wall_upper != None:
                    if x_loc > self.x_wall_upper:
                        obj.df.loc[obj.df.index[-1], 'dxdt'] = np.min([x_vel, -x_vel])

            if self.y_wall_lower != None or self.y_wall_upper != None:
                y_loc = obj.df['y'].iloc[-1]
                y_vel = obj.df['dydt'].iloc[-1]

                if self.y_wall_lower != None:
                    if y_loc < self.y_wall_lower:
                        obj.df.loc[obj.df.index[-1], 'dydt'] = np.max([y_vel, -y_vel])

                if self.y_wall_upper != None:
                    if y_loc > self.y_wall_upper:
                        obj.df.loc[obj.df.index[-1], 'dydt'] = np.min([y_vel, -y_vel])

    def move_objs(self, acc_dict, dt):
        
        for obj in self.objects:
            acc = acc_dict[obj]
            obj.move(dt, acc)

    def timestep(self, dt):
        
        acc_dict = self.calc_acc()
        self.check_bounce()
        self.move_objs(acc_dict, dt)
        
    def visualise(self):
        
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

        fps = self.in_params['fps']

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

        for x_line in [self.x_wall_lower, self.x_wall_upper]:
            if x_line != None:
                ax.axvline(x=x_line, color='r', linestyle='--')

        for y_line in [self.y_wall_lower, self.y_wall_upper]:
            if y_line != None:
                ax.axhline(y=y_line, color='r', linestyle='--')
        
        ani = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=True)
        file = os.path.join(self.dir, f'movement_fps_{fps}.mp4')
        Writer = FFMpegWriter(fps=fps, codec='libx264')
        ani.save(file, writer=Writer)

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

