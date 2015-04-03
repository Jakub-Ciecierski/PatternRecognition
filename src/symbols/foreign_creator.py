from src.symbols.symbol_class import SymbolClass
from src.util.color_chooser import ColorChooser
from src.util.random_generator import RandomGenerator
from numpy import sqrt
import src.util.global_variables as global_v
from src.symbols.symbol_types import SymbolType
import random
from src.util import global_variables

'''
    For a given n-dimensional point, this method distort  
    it coordinates according to normal distribution.     
    In addition user can specify standard deviation of   
    this process
'''
def __generate_distortion(cloudCenterCoordinates,sigmaSqrt):
    distortedCenter = []
    for i in range(len(cloudCenterCoordinates)):
        distortedCenter.append(cloudCenterCoordinates[i]+ random.gauss(0, sigmaSqrt))
    return distortedCenter

"""
    Creates Homogeneous Foreign classes using, uniform distribution, compares the distance
    between newly generated characteristics values to the ones of
    Native classes to make sure that these values do not overlap
"""
def create_homogeneous_foreign(nativeClasses, characteristics):
    # create n Foreign classes
    foreignClasses = []
    for i in range(0,global_v.CLASS_NUM * (global_v.N_LEARNING)):
        name  = "Foreign" + str(i)
        foreignClass = SymbolClass(name, ColorChooser().getForeignColor(), 
                                   type = SymbolType.FOREIGN)
        # Keep generating characteristics for given Foreign class 
        # while the values are not valid
        while True:
            foreignCharacteristics = []
            # Generate characteristics
            for j in range(0,len(characteristics)):
                foreignCharacteristic = RandomGenerator().generateRandom(
                                                    characteristics[j].interval.lowerBound,
                                                    characteristics[j].interval.upperBound)
                #foreignCharacteristic += random.gauss(0, global_v.HOMO_STD_DEV)
                foreignCharacteristics.append(foreignCharacteristic)
            # Check if it is foreign 'enough'
            if __isForeign(foreignCharacteristics, nativeClasses):
                foreignClass.characteristicsValues = foreignCharacteristics
                break
        # Add to all classes
        foreignClasses.append(foreignClass)
    print("        >> Generated:",global_v.CLASS_NUM * (global_v.N_LEARNING)," Homogeneous Foreign classes")
    return foreignClasses

'''
    Creates non Homogeneous foreign classes.
        Choose one pair of two native classes 
        (e.g.: (0-1), (2-3), (4-5), (6-7), (8-9))
        Selected a point between them (a middle).
        Create a distortion (cloud) around this point.
'''
def create_non_homogeneous_foreign(nativeClasses):
    foreignClasses = []
    for i in range(0, len(nativeClasses)):
        # take two centers
        i_c1 = i
        i_c2 = i + 1
        if(i_c2 == len(nativeClasses)):
            i_c2 = 0

        center1 = nativeClasses[i_c1].characteristicsValues
        center2 = nativeClasses[i_c2].characteristicsValues
        
        # find the midpoint between two centers
        midpoint = []
        for p in range(0,len(center1)):
            midpoint.append((center1[p] + center2[p]) / 2)
        # create a cloud around midpoint
        for j in range(0,global_v.N_LEARNING):
            foreignClass = SymbolClass("foreign", ColorChooser().getForeignColor(), SymbolType.FOREIGN)
            foreignClass.characteristicsValues = __generate_distortion(midpoint[:] ,global_v.NON_HOMO_STD_DEV)
            foreignClasses.append(foreignClass)
    print("        >> Generated:", len(foreignClasses) ,"Non Homogeneous Foreign classes")
    return foreignClasses

'''
    Creates foreign classes with duplicated characteristics from native classes
'''
def create_clone_foreign(nativeClasses):
    foreignClasses = []
    for nc in nativeClasses:
        for dc in nc.learning_set:
            name  = "Foreign"
            foreignClass = SymbolClass(name, ColorChooser().getForeignColor(), 
                               type = SymbolType.FOREIGN)
            
            foreignClass.characteristicsValues = dc.characteristicsValues
            foreignClasses.append(foreignClass)
    return foreignClasses

'''
    Checks if given vector of foreignCharacteristics 
    does not overlap with any of the native ones.
    Based on Euclidean distance.
'''
def __isForeign(foreignCharacteristics, nativeClasses):
    # go through every characteristic in Native classes
    for cl in nativeClasses:
        for dcl in cl.learning_set:
            distance = 0
            for i in range(0,len(foreignCharacteristics)):
                distance += (foreignCharacteristics[i] - dcl.characteristicsValues[i])**2
            distance = sqrt(distance)
            if distance > global_v.FOREIGN_CHAR_DIST_THRESH:
                return True
            else:
                return False
            
