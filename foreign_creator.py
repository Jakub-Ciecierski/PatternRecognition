from symbol_class import SymbolClass
from util.color_chooser import ColorChooser
from util.random_generator import RandomGenerator
from numpy import sqrt
import util.global_variables as global_v
from symbol_types import SymbolType
import random

class ForeignCreator:
    def __init__(self):
        pass
    
    """
        Creates Foreign classes, compares the distance
        between newly generated characteristics values to the ones of
        Native classes to make sure that these values do not overlap
    """
    def createForeignClass(self, n, nativeClasses, characteristics):
        print("Generating:",global_v.CLASS_NUM * (global_v.N_LEARNING + global_v.N_TEST),"Foreign classes" )

        # create n Foreign classes
        foreignClasses = []
        for i in range(0,n):
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
                    foreignCharacteristic += random.gauss(0, global_v.DIST_BASE_P_SD)
                    foreignCharacteristics.append(foreignCharacteristic)
                # Check if it is foreign 'enough'
                if self.__isForeign(foreignCharacteristics, nativeClasses):
                    foreignClass.characteristicsValues = foreignCharacteristics
                    break
            # Add to all classes
            foreignClasses.append(foreignClass)
        return foreignClasses

    '''
        Creates foreign classes with duplicated characteristics from native classes
    '''
    def createForeignClassDuplicateCharValues(self, n, nativeClasses, characteristics):
        foreignClasses = []
        for nc in nativeClasses:
            for dc in nc.distortedClasses:
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
    def __isForeign(self, foreignCharacteristics, nativeClasses):
        # go through every characteristic in Native classes
        for cl in nativeClasses:
            for dcl in cl.distortedClasses:
                distance = 0
                for i in range(0,len(foreignCharacteristics)):
                    distance += (foreignCharacteristics[i] - dcl.characteristicsValues[i])**2
                distance = sqrt(distance)
                if distance > global_v.FOREIGN_CHAR_DIST_THRESH:
                    return True
                else:
                    return False