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


if __name__=="__main__":
    print("Launching Part2")
    part2()

    print("Launching Part3")
    part3()
