import numpy as np
from utils import *



class Configuration(object):
    def __init__(self, N=100, R0=100, reflector_pos=(10,20), omega=2*np.pi, B=0, n_freq=1, config="circular", precision_step=1., representation_size=200, noise_level=0):
        self.config=config
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

        self.c0 = 1           # Wave celerity
        self.omega = omega    # Central frequency to be emitted
        self.B = B            # Width of the broadband (B=0 means the signal is harmonic)
        self.n_freq = n_freq  # Number of frequencies to usein the broadband
        self.sigma = noise_level
        if self.B == 0 and self.n_freq!=1:
            # If the signal is harmonic, only consider one frequency (this line should not be called, its role is mainly to anticipate bugs)
            self.n_freq = 1
            print("Warning, B=0 and n_freq=%i. n_freq has therefore been set to 1 because the source emits an harmonic signal." %n_freq)
        self.frequencies = np.linspace(self.omega-self.B, self.omega+self.B, self.n_freq)
                              # All frequencies to be simulated


    def generate_dataset(self):
        self.dataset = np.zeros((self.N, self.N, self.n_freq), "complex")
        for i in range(self.N):
            for j in range(i, self.N):
                # We only need to compute half of them since the dataset is symmetric
                x1 = self.transducer_pos[i, :]
                x2 = self.transducer_pos[j, :]
                for o, omega in enumerate(self.frequencies):
                    G_hat = compute_born_approx(omega, x1, x2, self.reflector_pos, include_direct_path=False)
                    self.dataset[i, j, o] = G_hat
                    self.dataset[j, i, o] = G_hat
        noise = 0.5 * self.sigma * (np.random.randn(self.N, self.N, self.n_freq) + np.random.randn(self.N, self.N, self.n_freq)*1j)
        self.dataset = self.dataset+noise


    def filter_imaging(self, background, X, Y):
        background = np.abs(background)
        """ Takes the imaging as input and deletes detection too close to the transduers """
        if self.config=="circular":
            for i in range(X.shape[0]):
                for j in range(Y.shape[0]):
                    x, y = (X[i, j], Y[i, j])
                    if dist((x, y), (0, 0))>=0.95*self.R0:
                        background[i, j] = background.min()
        elif self.config == "linear":
            background[Y<1.1] = background.min()
        return background



    def RT_Imaging(self, show=True, save=None):
        X, Y = create_mesh(self.representation_size, self.precision_step)
        self.n_pixels = X.shape[0]
        background = np.zeros_like(X, "complex")
        # print("Solving the 2N equations")
        for o, omega in enumerate(self.frequencies):
            G = [np.zeros_like(X, "complex") for s in range(self.N)]
            for i in range(self.n_pixels):
                for j in range(self.n_pixels):
                    x, y = (X[i, j], Y[i, j])
                    for s in range(self.N):
                        sx, sy = self.transducer_pos[s]
                        if dist((x, y), (sx, sy))<0.2:
                            G[s][i, j] = 0
                        G[s][i, j] = G0_hat(omega, (sx, sy), (x, y))

            # print("Creating us_tilda_hat")
            us_tilda_hat = [np.zeros_like(X, "complex") for s in range(self.N)]
            for s in range(self.N):
                for r in range(self.N):
                    us_tilda_hat[s] = us_tilda_hat[s] + G[r]*np.ma.conjugate(self.dataset[r, s, o])

            # print("Computing the result")
            for s in range(self.N):
                background = background + us_tilda_hat[s] * G[s]
        background = self.filter_imaging(background, X, Y)
        im = np.abs(background)
        im = (im-im.min())/(im.max()-im.min()+0.0000001)
        im = (255*im).astype("uint8")
        message = "Imagerie par retournement temporel"
        if show:
            plot_config(transducer_pos=self.transducer_pos, reflector_pos=[self.reflector_pos], pressure=im, n_pixels=self.n_pixels, limits=self.representation_size, message=message, save=save)
        return background, X, Y


    def KM_Imaging(self, show=True, save=None):
        X, Y = create_mesh(self.representation_size, self.precision_step)
        self.n_pixels = X.shape[0]
        background = np.zeros_like(X, "complex")
        # print("Solving the 2N equations")
        for o, omega in enumerate(self.frequencies):
            G = [np.zeros_like(X, "complex") for s in range(self.N)]
            for i in range(self.n_pixels):
                for j in range(self.n_pixels):
                    x, y = (X[i, j], Y[i, j])
                    for s in range(self.N):
                        sx, sy = self.transducer_pos[s]
                        G[s][i, j] = np.exp( (omega*dist((x,y), (sx,sy))/self.c0)*1j)

            # print("Creating us_tilda_hat")
            us_tilda_hat = [np.zeros_like(X, "complex") for s in range(self.N)]
            for s in range(self.N):
                for r in range(self.N):
                    us_tilda_hat[s] = us_tilda_hat[s] + G[r]*np.ma.conjugate(self.dataset[r, s, 0])

            # print("Computing the result")
            for s in range(self.N):
                background = background +us_tilda_hat[s] * G[s]
        background = self.filter_imaging(background, X, Y)
        im = np.abs(background)
        im = (im-im.min())/(im.max()-im.min()+0.0000001)
        im = (255*im).astype("uint8")
        message = "Imagerie KM"
        if show:
            plot_config(transducer_pos=self.transducer_pos, reflector_pos=[self.reflector_pos], pressure=im, n_pixels=self.n_pixels, limits=self.representation_size, message=message, save=save)
        return background, X, Y


    def MUSIC_Imaging(self, show=True, save=None):
        X, Y = create_mesh(self.representation_size, self.precision_step)
        self.n_pixels = X.shape[0]
        background = np.zeros_like(X, "complex")

        for o, omega in enumerate(self.frequencies):
            eigenvalues, eigenvectors = np.linalg.eig(self.dataset[:,:,o])
            v1 = np.ma.conjugate(eigenvectors[:,0])

            for i in range(self.n_pixels):
                for j in range(self.n_pixels):
                    x, y = (X[i, j], Y[i, j])
                    g_hat_x = np.zeros(self.N, "complex")
                    for s in range(self.N):
                        sx, sy = self.transducer_pos[s]
                        g_hat_x[s] = G0_hat(omega, (sx, sy), (x, y))

                    background[i, j] += np.abs(np.dot(g_hat_x, v1))**2

        background = self.filter_imaging(background, X, Y)
        im = np.abs(background)
        im = (im-im.min())/(im.max()-im.min()+0.0000001)
        im = (255*im).astype("uint8")
        message = "Imagerie MUSIC"
        if show:
            plot_config(transducer_pos=self.transducer_pos, reflector_pos=[self.reflector_pos], pressure=im, n_pixels=self.n_pixels, limits=self.representation_size, message=message, save=save)
        return background, X, Y


    def theoretical_Imaging(self, omega, show=True, save=None):
        X, Y = create_mesh(self.representation_size, self.precision_step)
        im = np.sqrt((X - self.reflector_pos[0])**2 + (Y - self.reflector_pos[1])**2)
        im = J0(omega*im)**2
        im = (im-im.min())/(im.max()-im.min()+0.0000001)
        if show:
            message = "Theoretical imaging"
            im = (255*im).astype("uint8")
            plot_config(transducer_pos=self.transducer_pos, reflector_pos=[self.reflector_pos], pressure=im, n_pixels=self.n_pixels, limits=self.representation_size, message=message, save=save)
        return im


    def get_estimated_reflector(self, background, X, Y):
        x, y = np.unravel_index(background.argmax(), background.shape)
        x, y = (X[x, y], Y[x, y])
        return x, y


    def get_estimation_error(self, background, X, Y):
        x, y = self.get_estimated_reflector(background, X, Y)
        return dist((x, y), (self.reflector_pos))





if __name__=="__main__":
    omega = 0.2*2*np.pi
    B = 0.*omega
    conf = Configuration(N=30, R0=100., reflector_pos=(0, 50), omega=omega, B=B, n_freq=1, config="linear", representation_size=110., precision_step=2, noise_level=0.00000005)
    # conf.theoretical_Imaging(omega, save="data/theoretical_base.png")
    conf.generate_dataset()
    bg, X, Y = conf.RT_Imaging(show=True, save="data\RT_linear_y100.png")
    bg, X, Y = conf.KM_Imaging(show=True, save="data\KM_linear_y100.png")
    bg, X, Y = conf.MUSIC_Imaging(show=True, save="data\MUSIC_linear_y100.png")
    # print(conf.get_estimation_error(bg, X, Y))
