class Simulation:
    
    def __init__(self, domains):
        self.domains = domains

    def begin(self):
            
            for domain in self.domains:
                domain.begin()

    def visualise(self):

        for domain in self.domains:
            domain.visualise()

    def export(self):

        for domain in self.domains:
            domain.export()