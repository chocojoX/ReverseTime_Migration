import numpy as np
import matplotlib.pyplot as plt
import cv2
import scipy.special as sp
import scipy.integrate as integrate

# File created for all utility functions or classes


def create_circular_transducers(N, R0):
    """ Returns a Nx2 matrix with position of N transducers positioned on a centered circle of radius R0"""
    pos = np.zeros((N, 2))
    idx = np.arange(N)
    pos[:,0] = R0*np.cos(2*np.pi*idx/N)
    pos[:,1] = R0*np.sin(2*np.pi*idx/N)
    return pos


def create_linear_transducers(N, R0):
    pos = np.zeros((N, 2))
    pos[:, 0] = np.linspace(-R0, R0, N)
    return pos


def plot_config(transducer_pos=None, reflector_pos=None, pressure=None, n_pixels=524, limits=5, message = "configuration", save = None):
    """
    Plots the configuration. All arguments are optional, the function will plot all given arguments on the same figure
    inputs :
    - n_pixels : size (in pixels) of the image to show
    - limits : coordinates limits of the domain to show
    """
    # Creating background
    if pressure is None:
        # Background is dark grey
        background = (15*np.ones((n_pixels, n_pixels, 3))).astype("uint8")
    else:
        background = cv2.applyColorMap(pressure, cv2.COLORMAP_JET)

    precision_step = 2*limits/n_pixels
    # Creating tranducers and plotting them as red circles
    if transducer_pos is not None:
        for i in range(transducer_pos.shape[0]):
            pt = (int(n_pixels/(2*limits)*transducer_pos[i, 0]+n_pixels/2), int(n_pixels/(2*limits)*transducer_pos[i, 1]+n_pixels/2))
            # import pdb; pdb.set_trace()
            cv2.circle(background, pt, 1, (15,15,255), 1)

    # Adding Reflectors as blue circles
    if reflector_pos is not None:
        for pos in reflector_pos:
             pt = (int(n_pixels/(2*limits)*pos[0]+n_pixels/2), int(n_pixels/(2*limits)*pos[1]+n_pixels/2))
             cv2.circle(background, pt, 1, (15,255,15), 1)

    if background.shape[0]<500:
        background = cv2.resize(background, (500,500))
    if save is not None:
        cv2.imwrite(save, background)
    cv2.imshow(message, background)
    cv2.waitKey(0)


def create_mesh(size, precision):
    n = int(size/precision)
    x = np.arange(-n, n+1)
    X, Y = np.meshgrid(x, x)
    X = X * size/n
    Y = Y * size/n
    return X, Y


def dist(x, y):
    """ Returns the euclidean distance betwwen two tuples or lists of length 2"""
    return np.sqrt((x[0]-y[0])**2+(x[1]-y[1])**2)


def J0(s):
    """ Returns the value of Bessel function of the first kind """
    return sp.j0(s)


def Y0(s):
    """ Returns the value of the bessel funciton of the first kind in s """
    if s<0.001:
        s=0.001   # Y0(0)=-inf
    return sp.y0(s)


def H0(s):
    """ Computes and returns the value of the Hankel function in s """
    if s<0.01:
        s = 0.01   #H0(0) = -inf
    value = sp.hankel1(0, s)
    # theoretical_value = J0(s) + 1j*Y0(s)
    return value


def G0_hat(omega, x, y):
    """ Returns the (complex) value of G0_hat(omega, x, y) according to the following formula :
        G0_hat = i/4*H0(w*|x-y|)
        With H0 is the Hankel function (H0 = J0 + i * Y0 with J0 first Bessel function and Y0 second Bessel function)
    """
    # TODO To be tested
    G0 = 0.25j*H0(omega*dist(x, y))
    return G0


def compute_born_approx(omega, x1, x2, reflector_pos, c0=1, include_direct_path=True) :
    """ Computes and returns the Born approximation of G_hat at frequency omega between two transducers at
     positions x1 and x2 with a (unique for now) reflector at reflector_pos.
     The wave velocity is denoted c0
    """
    if include_direct_path:
        # Include G0(x1,x2) in the computation
        G_hat = G0_hat(omega, x1, x2) + (omega/c0)**2*G0_hat(omega, x1, reflector_pos)*G0_hat(omega, x1, reflector_pos)
    else:
        # Delete the direct signal (signal without bouncing on the reflector)
        G_hat = (omega/c0)**2 * G0_hat(omega, x1, reflector_pos)*G0_hat(omega, x2, reflector_pos)
    return G_hat

def theoretical_func_x_part3(x, omega, reflector_pos, R0):
    reflector_dist = dist(reflector_pos, (0,0))
    rc = (2*np.pi/omega) * (reflector_dist / (2*R0))
    result = np.sinc(np.pi*(x[0]-reflector_pos[0])/rc)**2
    return result

def theoretical_func_z_part3(x, omega, reflector_pos, R0):
    reflector_dist = dist(reflector_pos, (0,0))
    rl = 2*(2*np.pi/omega)*(reflector_dist/(2*R0))**2
    result = integrate.quad(lambda s: np.exp(-1j*(np.pi/2)*(s**2)*np.abs(x[1]-reflector_pos[1])/rl), 0, 1)
    result = result[0]+ 1j*result[1]
    return np.abs(result)**2

def theoretical_2D_func_part3(x, omega, reflector_pos, R0):
    result = theoretical_func_z_part3(x, omega, reflector_pos, R0) * theoretical_func_x_part3(x, omega, reflector_pos, R0)
    return result

def theoretical_func_x_part4(x, omega, reflector_pos, R0):
    return theoretical_func_x_part3(x, omega, reflector_pos, R0)



if __name__=="__main__":
    ## This part is for testing only
    H0(3)
    transducer_pos = create_circular_transducers(N=20, R0=2)
    plot_config(transducer_pos, reflector_pos = [(0.1,0.2)])
    # import matplotlib.pyplot as plt
    # plt.scatter(transducer_pos[:, 0], transducer_pos[:, 1])
    # plt.show()
