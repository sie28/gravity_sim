from simulation.run_sim import run_sim

    
if __name__ == '__main__':

    in_file_names = ['domain_1']
    fps = 250
    t_end = 10
    dt = 2

    run_sim(in_file_names, t_end, dt, fps)