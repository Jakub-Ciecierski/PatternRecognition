from symbols.interval import Interval
import util.global_variables as global_v
import sys

class Cuboid:
    '''
    '''
    def __init__(self,points):
        self.__dimensions = self.__calculate_dimensions(points)
        self.center       = self.__calculate_center()
        
    def __calculate_center(self):
        center =[] 
        for dim in self.__dimensions:
            dim_center = (dim.upperBound + dim.lowerBound)/2
            center.append(dim_center)
        return center
        
    '''
    '''        
    def is_point_in_cuboid(self, point):
        if(len(point) != len(self.__dimensions)):
            print("ERROR:is_point_in_cuboid; Point dimension is different than cuboid's one.")
        else:
            for i in range(0,len(point)):
                if (point[i] < self.__dimensions[i].lowerBound) or (point[i] > self.__dimensions[i].upperBound):
                    return False
            return True    
    
    '''
    '''
    def points_in_cuboid(self,points):
        points_in = []
        for point in points:
            if self.is_point_in_cuboid(point):
                points_in.append(point)
        return points_in
        
    '''
    '''        
    def __calculate_dimensions(self, points):
        if(global_v.LOADING_BARS):
            percentage = 0
            increment = 100/len(points[0])
            
        dimensions = []
        for i in range(0,len(points[0])):
            gathered = []
            for characteristics in points:
                gathered.append(characteristics[i])
            dimensions.append(self.__get_interval(gathered))
            
            if(global_v.LOADING_BARS):
                percentage += increment
                hashes = '#' * int(round(percentage/5))
                spaces = ' ' * (20 -len(hashes))
                sys.stdout.write("\r        >> enclosing cuboid calculation:                   [{0}] {1}%".format(hashes + spaces, int(round(percentage))))
                sys.stdout.flush()
                
        if(global_v.LOADING_BARS): 
            print()    
        return dimensions
        
    '''
    '''            
    def __get_interval(self, list):
        min = list[0]
        max = list[0]
        
        for i in range(1,len(list)):
            if list[i] < min:
                min = list[i]
            if list[i] > max:
                max = list[i]
                
        return Interval(min,max)
        