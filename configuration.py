import numpy as np
from utils import *



class Configuration(object):
    def __init__(self, N=100, R0=100, reflector_pos=(10,20), omega=2*np.pi, B=0, n_freq=1, config="circular", precision_step=1., representation_size=200):
        if config=="circular":
            self.transducer_pos = create_circular_transducers(N, R0)
        elif config== "linear":
            self.transducer_pos = create_linear_transducers(N, R0)
        else:
            print("Config '%s' not yet implemented, please, try either 'circular' or 'linear'" %sconfig)

        self.precision_step = precision_step    # Step between two pixels where the values of the imaging are computed
        self.representation_size = representation_size   # Size of Omega (which is a square)
        self.n_pixels = int(2*representation_size/precision_step + 1)

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
        # TODO Python matrices can't naturally handle complex numbers.
        # We need to adapt somehow
        self.dataset = np.zeros((self.N, self.N, self.n_freq), "complex")
        for i in range(self.N):
            for j in range(i, self.N):
                # We only need to compute half of them since the dataset is symmetric
                x1 = self.transducer_pos[i, :]
                x2 = self.transducer_pos[j, :]
                for o, omega in enumerate(self.frequencies):
                    G_hat = compute_born_approx(omega, x1, x2, self.reflector_pos)
                    # TODO Debug : G_hat is NAN for the moment
                    self.dataset[i, j, o] = G_hat
                    self.dataset[j, i, o] = G_hat


    def RT_Imaging(self):
        # TODO implement the RT imaging from self.dataset
        pass


    def KM_Imaging(self):
        # TODO implement the RT imaging from self.dataset
        pass


    def theoretical_Imaging(self, omega, show=True):
        X, Y = create_mesh(self.representation_size, self.precision_step)
        im = np.sqrt((X - self.reflector_pos[0])**2 + (Y - self.reflector_pos[1])**2)
        im = J0(omega*im)**2
        im = (im-im.min())/(im.max()-im.min()+0.0000001)
        if show:
            message = "Theoretical imaging"
            im = (255*im).astype("uint8")
            plot_config(transducer_pos=self.transducer_pos, reflector_pos=[self.reflector_pos], pressure=im, n_pixels=self.n_pixels, limits=self.representation_size, message=message)
        return im




if __name__=="__main__":
    conf = Configuration(N=100, R0=90, reflector_pos=(10,20), omega=2*np.pi, B=0, n_freq=1, config="circular", representation_size=100, precision_step=0.5)
    conf.theoretical_Imaging(1)
    conf.generate_dataset()
    conf.RT_Imaging()
