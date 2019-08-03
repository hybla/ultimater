import numpy

# find the angle between two points
# from: https://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points
def angle_between(p1, p2):
    ang1 = numpy.arctan2(*p1[::-1])
    ang2 = numpy.arctan2(*p2[::-1])
    return numpy.rad2deg((ang1 - ang2) % (2 * numpy.pi))

# this uses angle_between() to find the direction to a single point
# from another point. 
def angle_to(A, B):
    offset = (B[0] - A[0], B[1] - A[1])
    return angle_between((0,1), offset)

# returns the direction that an angle (in degrees) points in
# uses our N, NE, E, SE etc. convention
def direction(angle):
    if (angle >  337.5) or (angle   <= 22.5):
        return 'N'
    elif(angle >  22.5) and (angle  <= 67.5): 
        return 'NE'
    elif(angle >  67.5) and (angle <= 112.5): 
        return 'E'
    elif(angle > 112.5) and (angle <= 157.5): 
        return 'SE'
    elif(angle > 157.5) and (angle <= 202.5): 
        return 'S'
    elif(angle > 202.5) and (angle <= 247.5): 
        return 'SW'
    elif(angle > 247.5) and (angle <= 292.5): 
        return 'W'
    elif(angle > 292.5) and (angle <= 337.5): 
        return 'W'

# done.
