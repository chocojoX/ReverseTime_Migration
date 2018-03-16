from configuration import *
import os


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


def compute_stats(mode = "circular", var="distance"):
    directory = "data"
    file_name = directory+"/stats_"+var+".txt"
    N=20
    R0 = 100
    reflector_pos = (20,20)
    omega = 0.05*2*np.pi
    B = 0.
    n_freq=1
    noise_level = 0.

    if not os.path.exists(directory):
        os.makedirs(directory)
    if mode=="circular":
        if var=="distance":
            for dist in range(95):
                reflector_pos = (0, dist)
                conf = Configuration(N=N, R0=R0, reflector_pos=reflector_pos, omega=omega, B=B, n_freq=n_freq, config="circular", representation_size=110., precision_step=1, noise_level=noise_level)
                conf.generate_dataset()
                bg, X, Y = conf.RT_Imaging(show=False)
                err_RT = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.KM_Imaging(show=False)
                err_KM = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.MUSIC_Imaging(show=False)
                err_MUSIC = conf.get_estimation_error(bg, X, Y)
                with open(file_name, "a") as f:
                    f.write("%i, %i, %.1f, %.1f, %.1f\n"%(N, dist, err_RT, err_KM, err_MUSIC))
        elif var=="noise_level":
            for noise_level in [1.5**i * 0.00001 for i in range(30)]:
                conf = Configuration(N=N, R0=R0, reflector_pos=reflector_pos, omega=omega, B=B, n_freq=n_freq, config="circular", representation_size=110., precision_step=1, noise_level=noise_level)
                conf.generate_dataset()
                bg, X, Y = conf.RT_Imaging(show=False)
                err_RT = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.KM_Imaging(show=False)
                err_KM = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.MUSIC_Imaging(show=False)
                err_MUSIC = conf.get_estimation_error(bg, X, Y)
                with open(file_name, "a") as f:
                    f.write("%i, %.6f, %.1f, %.1f, %.1f\n"%(N, noise_level, err_RT, err_KM, err_MUSIC))
        elif var=="N":
            for N in range(5, 100):
                conf = Configuration(N=N, R0=R0, reflector_pos=reflector_pos, omega=omega, B=B, n_freq=n_freq, config="circular", representation_size=110., precision_step=1, noise_level=noise_level)
                conf.generate_dataset()
                bg, X, Y = conf.RT_Imaging(show=False)
                err_RT = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.KM_Imaging(show=False)
                err_KM = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.MUSIC_Imaging(show=False)
                err_MUSIC = conf.get_estimation_error(bg, X, Y)
                with open(file_name, "a") as f:
                    f.write("%i, %.6f, %.1f, %.1f, %.1f\n"%(N, err_RT, err_KM, err_MUSIC))
        elif var=="n_freq":
            B = 0.1*omega
            noise_level=0.001
            for n_freq in range(20):
                conf = Configuration(N=N, R0=R0, reflector_pos=reflector_pos, omega=omega, B=B, n_freq=n_freq, config="circular", representation_size=110., precision_step=1, noise_level=noise_level)
                conf.generate_dataset()
                bg, X, Y = conf.RT_Imaging(show=False)
                err_RT = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.KM_Imaging(show=False)
                err_KM = conf.get_estimation_error(bg, X, Y)
                bg, X, Y = conf.MUSIC_Imaging(show=False)
                err_MUSIC = conf.get_estimation_error(bg, X, Y)
                with open(file_name, "a") as f:
                    f.write("%i, %.6f, %.1f, %.1f, %.1f\n"%(N, noise_level, n_freq, err_RT, err_KM, err_MUSIC))

    else:
        print("Mode %s not implemented yet for statistics computation. Nothing will be done." %mode)




if __name__=="__main__":
    # print("Launching Part2")
    # part2()
    #
    # print("Launching Part3")
    # part3()
    #
    # print("Launching Part4")
    # part4()
    #
    # print("Launching Part5")
    # part5()

    compute_stats(mode="circular", var="distance")
