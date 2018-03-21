from configuration import *
import os


def part2():
    conf = Configuration(N=100, R0=110., reflector_pos=(10, 20), omega=0.05*2*np.pi, B=0, n_freq=1, config="circular", representation_size=110., precision_step=1)
    conf.theoretical_Imaging(0.05*2*np.pi)
    conf.generate_dataset()
    conf.RT_Imaging()
    conf.KM_Imaging()


def part3(spot_x_direction=True, vary_omega = True, vary_ratio_xref_R0 = False):
    '''conf = Configuration(N=100, R0=25., reflector_pos=(0,100), omega=0.90*2*np.pi, B=0, n_freq=1, config="linear", representation_size=110., precision_step=1)
    conf.generate_dataset()
    conf.RT_Imaging()
    conf.KM_Imaging()
    conf.MUSIC_Imaging()'''
    # TODO Add code for comparing with the theoretical focal spots
    # For this, we'll need to return the predicted field of values and plot 1D curves
    # x_direction
    if spot_x_direction :
        if vary_omega :
            L_theo = []
            L_exp = []
            OMEGA = [j/float(100) for j in range(5,105,5)]
            for o in OMEGA:
                conf = Configuration(N=100, R0=25., reflector_pos=(0,100), omega=o*2*np.pi, B=0, n_freq=1, config="linear", representation_size=110., precision_step=1)
                conf.generate_dataset()
                background, X, Y = conf.KM_Imaging(False)
                spot_width_theo = conf.theo_spot_part3_x(o*2*np.pi)
                spot_width_exp = conf.exp_spot_part3_x(o*2*np.pi, background, X, Y)
                L_theo.append(spot_width_theo)
                L_exp.append(spot_width_exp)
            error_w = []
            for it in range(len(L_theo)):
                error_w.append(abs(L_theo[it]-L_exp[it]) )
            plt.figure()
            plt.plot(OMEGA, error_w, 'ro')
            plt.xlabel('Omega (2*pi scale)')
            plt.ylabel('error on the width of the focal spot')
            plt.title('plot of the absolute error on the width of the spot when xref=(0,100) while varying omega')
            plt.show()
        if vary_ratio_xref_R0 :
            L_theo = []
            L_exp = []
            Z_REF = [j for j in range(20,110, 10)]
            r0 = 50
            for z_ref in Z_REF :
                conf = Configuration(N=100, R0=r0, reflector_pos=(0,z_ref), omega=2*np.pi, B=0, n_freq=1, config="linear", representation_size=110., precision_step=1)
                conf.generate_dataset()
                background, X, Y = conf.KM_Imaging(False)
                spot_width_theo = conf.theo_spot_part3_x(2*np.pi)
                print(spot_width_theo)
                spot_width_exp = conf.exp_spot_part3_x(2*np.pi, background, X, Y)
                print(spot_width_exp)
                L_theo.append(spot_width_theo)
                L_exp.append(spot_width_exp)
            difference_width = []
            for it in range(len(L_theo)):
                difference_width.append(abs(L_theo[it]-L_exp[it]))
            RATIOS = [z_ref /float(r0) for z_ref in Z_REF]
            plt.figure()
            plt.plot(RATIOS, difference_width, 'bo')
            plt.xlabel('ration |xref| / R0 ')
            plt.ylabel('error on the width of the focal spot')
            plt.title('plot of the absolute error on the width of the spot when w=2*pi while varying the ratio')
            plt.show()
    # TODO z_direction

def part4():
    conf = Configuration(N=25, R0=100., reflector_pos=(10, 100), omega=0.05*2*np.pi, B=0.05, n_freq=10, config="linear", representation_size=105., precision_step=1)
    conf.theoretical_Imaging(0.05*2*np.pi)
    conf.generate_dataset()
    conf.RT_Imaging()
    conf.KM_Imaging()
    conf.MUSIC_Imaging()
    # TODO x_direction
    # TODO z_direction


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
                noise_level=0.000
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



'''
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

    compute_stats(mode="circular", var="N")
