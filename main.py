from configuration import *

def part2():
    conf = Configuration(N=100, R0=110., reflector_pos=(10, 20), omega=0.05*2*np.pi, B=0, n_freq=1, config="circular", representation_size=110., precision_step=1)
    conf.theoretical_Imaging(0.05*2*np.pi)
    conf.generate_dataset()
    conf.RT_Imaging()
    conf.KM_Imaging()


def part3():
    conf = Configuration(N=100, R0=50., reflector_pos=(0,100), omega=0.05*2*np.pi, B=0, n_freq=1, config="linear", representation_size=110., precision_step=1)
    conf.generate_dataset()
    conf.RT_Imaging()
    conf.KM_Imaging()
    conf.NUSIC_Imaging()
    # TODO Add code for comparing with the theoretical focal spots
    # For this, we'll need to return the predicted field of values and plot 1D curves


def part4():
    conf = Configuration(N=25, R0=100., reflector_pos=(10, 100), omega=0.05*2*np.pi, B=0.05, n_freq=10, config="linear", representation_size=105., precision_step=1)
    conf.theoretical_Imaging(0.05*2*np.pi)
    conf.generate_dataset()
    conf.RT_Imaging()
    conf.KM_Imaging()
    conf.MUSIC_Imaging()


def part5():
    omega = 0.05*2*np.pi
    B = 0.*omega
    conf = Configuration(N=20, R0=100., reflector_pos=(20, 20), omega=omega, B=B, n_freq=1, config="circular", representation_size=110., precision_step=1, noise_level=0.0001)
    # conf.theoretical_Imaging(omega)
    conf.generate_dataset()
    bg, X, Y = conf.RT_Imaging(show=True)
    print("Localisation error : %.1f" %conf.get_estimation_error(bg, X, Y))




if __name__=="__main__":
    print("Launching Part2")
    part2()

    print("Launching Part3")
    part3()

    print("Launching Part4")
    part4()

    print("Launching Part5")
    part5()
