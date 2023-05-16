
#Dictionary with perimeters and areas for all cloths in cloth set
#Given a perimeter/area compute error

def unfolding(real_obj_size, measured_perimeter_px, measured_perimeter_cm):
    real_perimeter_cm = (real_obj_size[0]+real_obj_size[1])*2
    real_area_cm = real_obj_size[0]*real_obj_size[1]
    print("Real cloth perimeter (cm): ", real_perimeter_cm)
    print("Real cloth area (cm): ", real_area_cm)

    # Error of the perimeter in centimeters
    error_perimeter_cm = real_perimeter_cm - measured_perimeter_cm
    print("Unfolding error (cm): ", error_perimeter_cm)

    # Percetange of error
    percentage_error_cm = 1-(measured_perimeter_cm/real_perimeter_cm)
    print("Unfolding % error: ", percentage_error_cm)

    #If error < X then pts

    return real_perimeter_cm, real_area_cm, error_perimeter_cm, percentage_error_cm


def folding(obj_size, init_area_px, perimeter_px, perimeter_cm, area_px, area_cm):
    #print("folding")
    obj_per = (obj_size[0]+obj_size[1]/2) #Half of the total area
    obj_area = (obj_size[0]*obj_size[1])/2
    print("Real folded cloth perimeter: ", obj_per, " cm")
    print("Real folded cloth area: ", obj_area, " cm")

    f2_init_area_px = init_area_px/2
    error_area_px = 1-(area_px/f2_init_area_px)
    print("Error with init image: ", error_area_px)

    error_per = obj_per - perimeter_cm
    error_area = obj_area - area_cm
    print("Error: ", error_per)
    print("Area error: ", error_area)

    #If error < X then pts

    return obj_per, obj_area, error_per, error_area

def folding2(obj_size, init_area_px, perimeter_px, perimeter_cm, area_px, area_cm):
    #print("folding")
    obj_per = (obj_size[0]+obj_size[1]) # (x/2+y/2)*2
    obj_area = (obj_size[0]*obj_size[1])/4
    print("Real folded cloth perimeter: ", obj_per, " cm")
    print("Real folded cloth area: ", obj_area, " cm")

    f2_init_area_px = init_area_px/4
    error_area_px = 1-(area_px/f2_init_area_px)
    print("Error with init image: ", error_area_px)

    error_per = obj_per - perimeter_cm
    error_area = obj_area - area_cm
    print("Error: ", error_per)
    print("Area error: ", error_area)

    #If error < X then pts

    return obj_per, obj_area, error_per, error_area

## Test code
#size = (50,90)
#unfolding(size, 175)


