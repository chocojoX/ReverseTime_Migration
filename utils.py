import numpy as np
import cv2
import scipy.special as sp

# File created for all utility functions or classes


def create_circular_transducers(N, R0):
    """ Returns a Nx2 matrix with position of N transducers positioned on a centered circle of radius R0"""
    pos = np.zeros((N, 2))
    idx = np.arange(N)
    pos[:,0] = R0*np.cos(2*np.pi*idx/N)
    pos[:,1] = R0*np.sin(2*np.pi*idx/N)
    return pos


def create_linear_transducers(N, R0):
    pos = np.zeros((N, N))
    pos[:, 0] = np.linspace(-R0, R0, N)
    return pos


def plot_config(transducer_pos=None, reflector_pos=None, pressure=None, size=524, limits=5):
    """
    Plots the configuration. All arguments are optional, the function will plot all given arguments on the same figure
    inputs :
    - size : size (in pixels) of the image to show
    - limits : coordinates limits of the domain to show
    """
    # Creating background
    if pressure is None:
        # Background is dark grey
        background = (15*np.ones((size, size, 3))).astype("uint8")
    else:
        # TODO Background should be of the color of the pressure field
        pass

    # Creating tranducers and plotting them as red circles
    if transducer_pos is not None:
        for i in range(transducer_pos.shape[0]):
            pt = (int(size/(2*limits)*transducer_pos[i, 0]+size/2), int(size/(2*limits)*transducer_pos[i, 1]+size/2))
            cv2.circle(background, pt, 3, (15,15,255), 3)

    # Adding Reflectors as blue circles
    if reflector_pos is not None:
        for pos in reflector_pos:
             pt = (int(size/(2*limits)*pos[0]+size/2), int(size/(2*limits)*pos[1]+size/2))
             cv2.circle(background, pt, 3, (255,15,15), 3)
        pass

    cv2.imshow("configuration", background)
    cv2.waitKey(0)


def dist(x, y):
    """ Returns the euclidean distance betwwen two tuples or lists of length 2"""
    return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)


def J0(s):
    """ Returns the value of Bessel function of the first kind """
    return sp.j0(s)


def Y0(s):
    """ Returns the value of the bessel funciton of the first kind in s """
    return sp.y0(s)


def H0(s):
    """ Computes and returns the value of the Hankel function in s """
    value = sp.hankel1(0, s)
    # theoretical_value = J0(s) + 1j*Y0(s)
    return value


def G0_hat(omega, x, y):
    """ Returns the (complex) value of G0_hat(omega, x, y) according to the following formula :
        G0_hat = i/4*H0(w*|x-y|)
        With H0 is the Hankel function (H0 = J0 + i * Y0 with J0 first Bessel function and Y0 second Bessel function)
    """
    # TODO To be tested
    G0 = 1j/4.*H0(omega*dist(x, y))
    return G0


def compute_born_approx(omega, x1, x2, reflector_pos, c0=1) :
    """ Computes and returns the Born approximation of G_hat at frequency omega between two transducers at
     positions x1 and x2 with a (unique for now) reflector at reflector_pos.
     The wave velocity is denoted c0
    """
    # TODO To be tested
    G_hat = G0_hat(omega, x1, x2) + (omega/c0)**2*G0_hat(omega, x1, reflector_pos)*G0_hat(omega, x1, reflector_pos)
    return G_hat



if __name__=="__main__":
    ## This part is for testing only
    H0(3)
    transducer_pos = create_circular_transducers(N=20, R0=2)
    plot_config(transducer_pos, reflector_pos = [(0.1,0.2)])
    # import matplotlib.pyplot as plt
    # plt.scatter(transducer_pos[:, 0], transducer_pos[:, 1])
    # plt.show()
