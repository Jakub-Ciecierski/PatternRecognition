from clustering.elllipsoid import  Ellipsoid
from clustering.cuboid import Cuboid
from enum import Enum
import util.console as console
from clustering import cuboid
from util.basic_math import sort_by_distance
from util.basic_math import euclidian_distance

class BasicMembership:
    '''
    TODO
    '''
    def __init__(self, symbolClasses):
        self.ellipsoids = self.__generate_objects(symbolClasses, ObjectType.ELLIPSOID)
        self.cuboids    = self.__generate_objects(symbolClasses, ObjectType.CUBOID)
    '''
    TODO
    '''        
    def __generate_objects(self, symbolClasses, type):
        set_of_objects = []
        for cl in symbolClasses:
            # Gather up points from each distorted class
            temp_points = []
            for el in cl.learning_set:
                temp_points.append(el.characteristicsValues[:])
                
            if(type == ObjectType.ELLIPSOID):
                ellipsoid = Ellipsoid(temp_points)
                # Check accuracy 
                pointsInEllipsoid = ellipsoid.is_point_in_ellipsoid(temp_points,False, True)
                print("           Points in Ellipsoid:                ", 100 * len(pointsInEllipsoid)/len(temp_points),"%")
                # Save an ellipsoid
                set_of_objects.append(EllipsoidWrap(temp_points,ellipsoid))
                
            if(type == ObjectType.CUBOID):
                cuboid = Cuboid(temp_points)
                # Check accuracy
                pointsInCuboid = cuboid.points_in_cuboid(temp_points)
                print("           Points in Cuboid:                ", 100 * len(pointsInCuboid)/len(temp_points),"%")
                set_of_objects.append(CuboidWrap(temp_points,cuboid))
            
        return set_of_objects

    
ObjectType = Enum('ObjectType','ELLIPSOID CUBOID')

class EllipsoidWrap:
    def __init__(self,points,ellipsoid):
        self.ellipsoid = ellipsoid
        self.points = sort_by_distance(points, ellipsoid.center)
        
    def recalculate_ellipsoid(self):
        print("Recalculating ellipsoid")
        self.ellipsoid = Ellipsoid(self.points)
    
    def remove_longest_point(self):
        print("ELLIPSOID: Removing point")
        del self.points[0]   
        
class CuboidWrap:
    def __init__(self,points,cuboid):
        self.cuboid = cuboid
        self.points = sort_by_distance(points, cuboid.center)

    def recalculate_cuboid(self):
        self.cuboid = Cuboid(self.points)     
        
    def remove_longest_point(self):
        print("CUBOID: Removing point")
        del self.points[0]          