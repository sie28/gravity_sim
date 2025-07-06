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