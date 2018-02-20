import numpy as np
from utils import *



class Configuration(object):
    def __init__(self, N=100, R0=100, reflector_pos=(10,20)):
        self.transducer_pos = create_circular_transducers(N, R0)
        self.N = N
        self.R0 = R0
        self.reflector_pos = reflector_pos


    def generate_dataset(self, omega):
        self.dataset = np.zeros((self.N, self.N))
        for i in range(self.N):
            for j in range(i, self.N):
                # We only need to compute half of them since the dataset is symmetric
                x1 = self.transducer_pos[i, :]
                x2 = self.transducer_pos[j, :]
                G_hat = compute_born_approx(omega, x1, x2, xelf.reflector_pos)
                self.dataset[i, j] = G_hat
                self.dataset[j, i] = G_hat
        pass
