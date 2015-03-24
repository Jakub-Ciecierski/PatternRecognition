# Class in charge of creating cloud of N  random 
# points for each (supplied) class of symbols.   

from numpy import random, sqrt, log, sin, cos, pi
import random
from symbol_class import SymbolClass

class Distorter:
    
    def __init__(self, N):
        self.N = N
        self.divisor = 1
        if(N % self.divisor != 0):
            print("Value of 'N' is not a multiplicity of value of 'divisor'.", 
                    "It may cause some problems e.g\n",
                    "desired number of points may differ.")
             
        self.basePointsVariance = 0.5
        self.cloudPointsVariance = 0.3
        print("Number of distorted classes per symbol:", N)

    # For a given n-dimensional point, this method distort  
    # it coordinates according to normal distribution.     
    # In addition user can specify standard deviation of   
    # this process                                         
    def generate_distortion(self, cloudCenterCoordinates,sigmaSqrt):
        distortedCenter = []
        for i in range(len(cloudCenterCoordinates)):
            distortedCenter.append(cloudCenterCoordinates[i]+ random.gauss(0, sigmaSqrt))
        return distortedCenter
    

    # Heart of the class. For a given set of symbol classes, this            
    # method generates cloud of points, following given algorithm:           
    #                                                                         
    # 1) Take coordinates of a given class and create N/divisor              
    #    new points with coordinates based on the class but distorted       
    #    using normal distribution with sigma equal to 'basePointsVariance'  
    #    value                                                              
    # 2) For each point created in 1) create (divisor-1) point cloud         
    #    based on this point distorted coordinates (again using normal       
    #    distribution but with sigma equal to 'cloudPointsVariance'           
    # 3) Repeat 1) and 2) until all symbol classes are managed                
    def create_cloud(self, symbolClasses):
        distortedClasses = []
        for cl in symbolClasses:
            for i in range(0, int(self.N/self.divisor)):
                # instance of new symbol
                distortedClass = SymbolClass(cl.name, cl.color)
                # randomize position around a given class(based on position)
                distortedClass.characteristicsValues = self.generate_distortion(
                                                                cl.characteristicsValues[:],
                                                                self.basePointsVariance)
                # store result 
                cl.distortedClasses.append(distortedClass)
                # create cloud of points around newly created one - distortedClass
                for j in range(0,self.divisor-1):
                    cloudPoint = SymbolClass(cl.name, cl.color)
                    
                    cloudPoint.characteristicsValues = self.generate_distortion(
                                                                distortedClass.characteristicsValues[:], 
                                                                self.cloudPointsVariance)
                    cl.distortedClasses.append(cloudPoint)