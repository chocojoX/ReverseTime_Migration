import numpy as np
from utils import *



class Configuration(object):
    def __init__(self, N=100, R0=100, reflector_pos=(10,20), omega=2*np.pi, B=0, n_freq=1, config="circular"):
        if config=="circular":
            self.transducer_pos = create_circular_transducers(N, R0)
        elif config== "linear":
            self.transducer_pos = create_linear_transducers(N, R0)
        else:
            print("Config '%s' not yet implemented, please, try either 'circular' or 'linear'" %sconfig)

        self.N = N            # Number of transducers
        self.R0 = R0          # Scale of the transducers repartition
        self.reflector_pos = reflector_pos   # Matrix of position of the transducers

        self.omega = omega    # Central frequency to be emitted
        self.B = B            # Width of the broadband (B=0 means the signal is harmonic)
        self.n_freq = n_freq  # Number of frequencies to usein the broadband
        if self.B == 0:
            # If the signal is harmonic, only consider one frequency (this line should not be called, its role is mainly to anticipate bugs)
            self.n_freq = 1
            print("Warning, B=0 and n_freq=%i. n_freq has therefore been set to 1 because the source emits an harmonic signal." %n_freq)
        self.frequencies = np.linspace(self.omega-self.B, self.omega+self.B, self.n_freq)
                              # All frequencies to be simulated


    def generate_dataset(self):
        # TODO To be tested
        self.dataset = np.zeros((self.N, self.N, self.n_freq))
        for i in range(self.N):
            for j in range(i, self.N):
                # We only need to compute half of them since the dataset is symmetric
                x1 = self.transducer_pos[i, :]
                x2 = self.transducer_pos[j, :]
                for omega in self.frequencies:
                    G_hat = compute_born_approx(omega, x1, x2, xelf.reflector_pos)
                    self.dataset[i, j, omega] = G_hat
                    self.dataset[j, i, omega] = G_hat


    def RT_Imaging(self):
        # TODO implement the RT imaging from self.dataset
        pass


    def KM_Imaging(self):
        # TODO implement the RT imaging from self.dataset
        pass


    def theoretical_Imaging(self):
        # TODO Do the theoretical imaging using the first Bessale function



if __name__=="__main__":
    conf = Configuration(N=100, R0=100, reflector_pos=(10,20), omega=2*np.pi, B=0, n_freq=1, config="circular")
    conf.generate_dataset()
    conf.RT_Imaging()
