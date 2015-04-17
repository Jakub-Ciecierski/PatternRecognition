from clustering.elllipsoid import  Ellipsoid
from clustering.cuboid import Cuboid
from enum import Enum
import util.console as console
from clustering import cuboid

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
                print("           Points in cluster:                ", 100 * len(pointsInEllipsoid)/len(temp_points),"%")
                # Save an ellipsoid
                set_of_objects.append(ellipsoid)
                
            if(type == ObjectType.CUBOID):
                cuboid = Cuboid(temp_points)
                print("Creating cuboid")
            
        return set_of_objects

ObjectType = Enum('ObjectType','ELLIPSOID CUBOID') 
            