from symbol_class import SymbolClass
from util.color_chooser import ColorChooser
from util.random_generator import RandomGenerator
from numpy import sqrt
import util.global_variables as global_v
from symbol_types import SymbolType

class ForeignCreator:
    def __init__(self):
        pass
    
    # Creates Foreign classes, checks the difference
    # of generated characteristics values to the ones of
    # Native classes, to make sure that no Foreign class overlaps
    # with previously generated Native classes
    def createForeignClass(self, n, nativeClasses, characteristics):
        # create n Foreign classes
        foreignClasses = []
        for i in range(0,n):
            foreignClass = SymbolClass("foreign", ColorChooser().getForeignColor(), 
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
                    foreignCharacteristics.append(foreignCharacteristic)
                # Check if it is foreign 'enough'
                if self.__isForeign(foreignCharacteristics, nativeClasses):
                    foreignClass.characteristicsValues = foreignCharacteristics
                    break
            # Add to all classes
            foreignClasses.append(foreignClass)
                
    # Checks if given vector of foreignCharacteristics 
    # does not overlap with any of the native ones.
    # Based on Euclidean distance.
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