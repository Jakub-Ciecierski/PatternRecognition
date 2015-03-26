from symbol_class import SymbolClass
from util.color_chooser import ColorChooser
from util.random_generator import RandomGenerator
from numpy import sqrt

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
            foreignClass = SymbolClass("foreign", ColorChooser().getForeignColor())
            # create characteristics for given foreign class
            foreignCharacteristics = []

            for j in range(0,len(characteristics)):
                foreignCharacteristic = RandomGenerator().generateRandom(
                                                                         characteristics[j].interval.lowerBound,
                                                                         characteristics[j].interval.upperBound)
                foreignCharacteristics.append(foreignCharacteristic)

            isForeign = self.__isForeign(foreignCharacteristics, nativeClasses)
            foreignClass.characteristicsValues = foreignCharacteristics
    
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
                print("The distance between two vectors: ")
                print(dcl.characteristicsValues)
                print(foreignCharacteristics)
                print("is:",distance)