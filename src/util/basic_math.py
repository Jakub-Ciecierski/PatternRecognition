from numpy import sqrt

def euclidian_distance(point1, point2):
    if len(point1) != len(point2):
        print("ERROR: euclidian distance; different dimensions.")
    else:
        distance = 0
        for i in range(0, len(point1)):
            distance += (point2[i]-point1[i])**2
        return sqrt(distance)

def sort_by_distance(points, center):
    # Error check
    for point in points:
        if len(point) != len(center):
            print("ERROR: sort_by_distance; different dimensions.")
            return 0
        
    # Bubble sort    
    for i in range(0,len(points)):
        for j in range(0,len(points)-1):
            if euclidian_distance(points[j], center) < euclidian_distance(points[j+1], center):
                points[j], points[j+1] = points[j+1], points[j]
          
    return points        
        
    
            