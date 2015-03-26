from numpy import random, sqrt, log, sin, cos, pi
import random
import util.global_variables as global_v
from symbol_class import SymbolClass
from symbol_types import SymbolType

'''
    Class in charge of creating cloud of N  random 
    points for each (supplied) class of symbols.   
'''
class Distorter:
    
    def __init__(self):
        if(global_v.N % global_v.DIST_DIV != 0):
            print("Value of 'N' is not a multiplicity of value of 'divisor'.", 
                    "It may cause some problems e.g\n",
                    "desired number of points may differ.")

        print("Number of distorted classes per symbol:", global_v.N)
        
    '''
        For a given n-dimensional point, this method distort  
        it coordinates according to normal distribution.     
        In addition user can specify standard deviation of   
        this process      
    '''                                   
    def __generate_distortion(self, cloudCenterCoordinates,sigmaSqrt):
        distortedCenter = []
        for i in range(len(cloudCenterCoordinates)):
            distortedCenter.append(cloudCenterCoordinates[i]+ random.gauss(0, sigmaSqrt))
        return distortedCenter
    
    '''
        Heart of the class. For a given set of symbol classes, this            
        method generates cloud of points, following given algorithm:           
                                                                                 
        1) Take coordinates of a given class and create N/divisor              
           new points with coordinates based on the class but distorted       
           using normal distribution with sigma equal to 'basePointsVariance'  
           value                                                              
        2) For each point created in 1) create (divisor-1) point cloud         
           based on this point distorted coordinates (again using normal       
           distribution but with sigma equal to 'cloudPointsVariance'           
        3) Repeat 1) and 2) until all symbol classes are managed   
    '''             
    def create_cloud(self, symbolClasses):
        for cl in symbolClasses:
            for i in range(0, int(global_v.N/global_v.DIST_DIV)):
                # instance of new symbol
                distortedClass = SymbolClass(cl.name, cl.color, type = SymbolType.NATIVE_LEARNING)
                # randomize position around a given class(based on position)
                distortedClass.characteristicsValues = self.__generate_distortion(
                                                                cl.characteristicsValues[:],
                                                                global_v.DIST_BASE_P_SD)
                # store result 
                cl.distortedClasses.append(distortedClass)
                # create cloud of points around newly created one - distortedClass
                for j in range(0,global_v.DIST_DIV-1):
                    cloudPoint = SymbolClass(cl.name, cl.color)
                    
                    cloudPoint.characteristicsValues = self.__generate_distortion(
                                                                distortedClass.characteristicsValues[:], 
                                                                global_v.DIST_CLOUD_P_SD)
                    cl.distortedClasses.append(cloudPoint)