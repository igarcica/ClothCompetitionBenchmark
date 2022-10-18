
#Dictionary with perimeters and areas for all cloths in cloth set
#Given a perimeter/area compute error

def unfolding(obj_size, perimeter):
    obj_per = (obj_size[0]+obj_size[1])*2
    obj_area = obj_size[0]*obj_size[1]
    print("Real cloth perimeter: ", obj_per)
    print("Real cloth area: ", obj_area)

    error_per = obj_per - perimeter
    print("Unfolding error: ", error_per)

    #If error < X then pts


def folding(obj_size, perimeter, area, fold):
    print("folding")
    obj_per = ((obj_size[0]+obj_size[1]/fold)*2) #Half of the total area
    obj_area = (obj_size[0]*obj_size[1])/fold
    print("Real folded cloth perimeter: ", obj_per)
    print("Real folded cloth area: ", obj_area)

    error_per = obj_per - perimeter
    error_area = obj_area - area
    print("Error: ", error_per)
    print("Area error: ", error_area)

    #If error < X then pts


## Test code
#size = (50,90)
#unfolding(size, 175)


