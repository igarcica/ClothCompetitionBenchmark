
#Dictionary with perimeters and areas for all cloths in cloth set
#Given a perimeter/area compute error

activate_print = False

def print_info(activate, arg1, arg2="", arg3="", arg4="", arg5="", arg6=""):
    if(activate):
        print(str(arg1) + str(arg2) + str(arg3) + str(arg4) + str(arg5) + str(arg6))

def unfolding(real_obj_size, measured_perimeter_px, measured_perimeter_cm, measured_area_px, measured_area_cm):
    real_perimeter_cm = (real_obj_size[0]+real_obj_size[1])*2
    real_area_cm = real_obj_size[0]*real_obj_size[1]
    print("Real cloth perimeter (cm): ", real_perimeter_cm)
    print("Real cloth area (cm): ", real_area_cm)

    print_info(activate_print, "UNFOLDED Measured cloth perimeter (px): ", measured_perimeter_px)
    print_info(activate_print, "UNFOLDED Measured cloth area (px): ", measured_area_px)
    print("UNFOLDED Measured cloth perimeter (cm): ", measured_perimeter_cm)
    print("UNFOLDED Measured cloth area (cm): ", measured_area_cm)

    # ERROR with REAL OBJECT SIZE - PERIMETER
    error_perimeter_cm = real_perimeter_cm - measured_perimeter_cm          # Error of the perimeter in centimeters
    percentage_perimeter_error_cm = (1-(measured_perimeter_cm/real_perimeter_cm))*100 # Percetange of perimeter error
    print_info(activate_print, "Unfolding perimeter error (cm): ", error_perimeter_cm)
    print_info(activate_print, "Unfolding perimeter error (%): ", percentage_perimeter_error_cm, " %")

    # ERROR with REAL OBJECT SIZE - AREA
    error_area_cm = real_area_cm - measured_area_cm          # Error of the perimeter in centimeters
    percentage_area_error_cm = (1-(measured_area_cm/real_area_cm))*100 # Percetange of perimeter error
    print(" Unfolding area error (cm): ", error_area_cm)
    print("\033[33m Unfolding area error (%): ", percentage_area_error_cm, " % \033[0m")

    #If error < X then pts

    return percentage_area_error_cm #, percentage_perimeter_error_cm, real_perimeter_cm, real_area_cm, error_perimeter_cm


def folding(real_obj_size, perimeter_px, perimeter_cm, area_px, area_cm):
    #print("folding")
    real_perimeter_cm = (real_obj_size[0]+real_obj_size[1]/2)*2 #Half of the total area
    real_area_cm = (real_obj_size[0]*real_obj_size[1])/2
    print("Real folded cloth perimeter (cm): ", real_perimeter_cm, " cm")
    print("Real folded cloth area (cm): ", real_area_cm, " cm")

    # # ERROR with INITIAL DEFINED AREA
    # f2_init_area_px = init_area_px/2
    # error_area_px = 1-(area_px/f2_init_area_px)
    # print("Error with init image: ", error_area_px)

    # ERROR with REAL OBJECT SIZE - PERIMETER
    error_perimeter_cm = real_perimeter_cm - perimeter_cm
    percentage_perimeter_error_cm = (1-(perimeter_cm/real_perimeter_cm))*100     # Percetange of error
    print("First fold error perimeter (cm): ", error_perimeter_cm)
    print("First fold perimeter error: ", percentage_perimeter_error_cm, "%")

    # ERROR with REAL OBJECT SIZE - AREA
    error_area_cm = real_area_cm - area_cm
    percentage_area_error_cm = (1-(area_cm/real_area_cm))*100
    print(" First fold area error (cm): ", error_area_cm)
    print("\033[33m First fold area error: ", percentage_area_error_cm, "% \033[0m")

    #If error < X then pts

    return percentage_area_error_cm #, percentage_perimeter_error_cm, real_perimeter_cm, real_area_cm, error_perimeter_cm #, error_area_cm

def folding2(real_obj_size, perimeter_px, perimeter_cm, area_px, area_cm):
    #print("folding")
    real_perimeter_cm = (real_obj_size[0]+real_obj_size[1]) # (x/2+y/2)*2
    real_area_cm = (real_obj_size[0]*real_obj_size[1])/4
    print("Real folded cloth perimeter: ", real_perimeter_cm, " cm")
    print("Real folded cloth area: ", real_area_cm, " cm")

    # # ERROR with INITIAL DEFINED AREA
    # f2_init_area_px = init_area_px/4
    # error_area_px = 1-(area_px/f2_init_area_px)
    # print("Error with init image: ", error_area_px)

    # ERROR with REAL OBJECT SIZE - PERIMETER
    error_perimeter_cm = real_perimeter_cm - perimeter_cm
    percentage_perimeter_error_cm = (1-(perimeter_cm/real_perimeter_cm))*100     # Percetange of error
    print("First fold error perimeter (cm): ", error_perimeter_cm)
    print("First fold perimeter error: ", percentage_perimeter_error_cm, "%")

    # ERROR with REAL OBJECT SIZE - AREA
    error_area_cm = real_area_cm - area_cm
    percentage_area_error_cm = (1-(area_cm/real_area_cm))*100
    print(" First fold area error (cm): ", error_area_cm)
    print("\033[33m First fold area error: ", percentage_area_error_cm, "% \033[0m")


    # if abs(percentage_area_error_cm) < 20.0:
    #     print("\033[92m Successful fold! \033[0m")
    #     # Sum points! Save points in CSV
    # else:
    #     print("\033[33m UNSUCCESSFUL fold! \033[0m")

    return percentage_area_error_cm #, percentage_perimeter_error_cm, real_perimeter_cm, real_area_cm, error_perimeter_cm

## Test code
#size = (50,90)
#unfolding(size, 175)


### TODO
# Join functions folding and folding2 into one with a parameter that defines the number of folds -> will be used to evaluate different number of folds


