import numpy as np
# import cv2

# File created for all utility functions or classes


def create_circular_transducers(N, R0):
    """ Returns a Nx2 matrix with position of N transducers positioned on a centered circle of radius R0"""
    pos = np.zeros((N, 2))
    idx = np.arange(N)
    pos[:,0] = R0*np.cos(2*np.pi*idx/N)
    pos[:,1] = R0*np.sin(2*np.pi*idx/N)
    return pos


def plot_config(transducer_pos=None, reflecter_pos=None, pressure=None, size=524, limits=10):
    #TODO Test this function
    # Creating background
    if pressure is None:
        # Background is dark grey
        background = (15*np.ones((size, size, 3))).astype("uint8")
    else:
        # TODO Background should be of the color of the pressure field
        pass

    # Creating tranducers
    if transducer_pos is not None:
        for i in range(transducer_pos.shape[0]):
            pt = (size/limits*transducer_pos[i, 0], size/limits*transducer_pos[i, 1])
            cv2.circle(background, pt, 3, (15,15,255), 3)

    if reflecter_pos is not None:
        #TODO add reflecter
        pass

    cv2.imshow("configuration", background)
    cv2.waitKey(0)


if __name__=="__main__":
    ## This part i for testing only
    transducer_pos = create_circular_transducers(N=20, R0=2)
    import matplotlib.pyplot as plt
    plt.scatter(transducer_pos[:, 0], transducer_pos[:, 1])
    plt.show()
