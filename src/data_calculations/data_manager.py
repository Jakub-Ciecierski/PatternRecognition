from util.random_generator import RandomGenerator
import util.global_variables as global_v
from symbols.characteristic import Characteristic
from symbols.symbol_class import SymbolClass
from symbols.symbol_types import SymbolType
from util.color_chooser import ColorChooser
import numpy as np
import os
import util.console as console

'''
    To make main.py more transparent whole process of initialization
    starting data and performing tests on generated sets takes place here.
'''

'''
    Creation of CHAR_NUM characteristics, each with random subinterval 
    of [0,20]. Uniform distribution is used.
'''
def generate_characteristic(characteristics):
    f = open(os.path.join("..","log",global_v.DIR_NAME,"CHARACTERISTICS.txt"), 'w')
    for i in range(0,global_v.CHAR_NUM):
        characteristics.append(Characteristic())
        console.write_characteristics(f,i, characteristics[i].interval.lowerBound,
                                characteristics[i].interval.upperBound,
                                "Characterestic #", "Interval:", "From:", "To:")
    f.close()
        
'''
    Initialization of CLASS_NUM symbol classes, each with CHAR_NUM
    characteristics. Values of each characteristic is randomized.
    Uniform distribution is used.
'''        
def generate_symbol_classes(symbolClasses, characteristics):
    for i in range(0,global_v.CLASS_NUM):
        newSymbol =  SymbolClass(i, ColorChooser().get_color(), type = SymbolType.NATIVE_BASE)  

        while True:
            # Generate random characteristics for new symbol
            newCharacteristics =[]
            for j in range(0,len(characteristics)):
                newCharacteristics.append(
                                RandomGenerator().generateRandom(characteristics[j].interval.lowerBound, 
                                                                 characteristics[j].interval.upperBound))   

            # Check generated numbers
            found = False
            for c in range(0,i):
                eucl = euclidian_distance(symbolClasses[c].characteristicsValues[:], newCharacteristics[:])
                if  eucl < global_v.HOMO_STD_DEV:
                    found = True
            if(not found):
                break
            
        # Save symbol
        newSymbol.characteristicsValues = newCharacteristics
        symbolClasses.append(newSymbol)   
         
    # INFO
    f = open(os.path.join("..","log",global_v.DIR_NAME,"NATIVE_SYMBOLS.txt"), 'w')
    for symbolClass in symbolClasses:
        console.write_symbol_classes(f,symbolClass.name,symbolClass.characteristicsValues,text="Symbol Class:", )
    f.close()
#
'''
    Using provided subset of generated distorted classes function performs
    cluster-membership test, determining how many points from test set belongs
    to clusters.
    Appropriate info is displayed.
'''
def cluster_membership_test(symbolClasses):
    for symbol_class in symbolClasses:
        number_of_accepted = 0
        for distorted_class in symbol_class.test_set:
            for cluster in symbol_class.clusters:
                # Check if a given point is rejected
                result = cluster.ellipsoid.is_point_in_ellipsoid([distorted_class.characteristicsValues[:]], True)
                # If point was not rejected increment number of accepted ad stop checking
                if(result == 0):
                    number_of_accepted += 1
                    break
        console.write_name_number(symbol_class.name, 100*number_of_accepted/global_v.N_TEST, 
                                  text="% of test points accepted by symbol")
        

def euclidian_distance(point1, point2):
    result = 0
    for i in range(0, len(point1)):
        result += np.power((point1[i]-point2[i]), 2)
    return np.sqrt(result)