import random
import global_variables as global_v
from characteristic import Characteristic
from symbol_class import SymbolClass
from color_chooser import ColorChooser

'''
    To make main.py more transparent wholl process of initialization
    starting data takes place here.
'''
class InitDataRandomizer:
    '''
        Creation of CHAR_NUM characteristics, each with random subinterval 
        of [0,20]. Uniform distribution is used.
    '''
    def generate_characteristic(self, characteristics):
        for i in range(0,global_v.CHAR_NUM):
            characteristics.append(Characteristic())
            print("Characterestic #",i,"Interval: From:",characteristics[i].interval.lowerBound,
                        "To:",characteristics[i].interval.upperBound)
    '''
        Initialization of CLASS_NUM symbol classes, each with CHAR_NUM
        characteristics. Values of each characteristic is randomized.
        Uniform distribution is used.
    '''        
    def generate_symbol_classes(self, symbolClasses, characteristics):
        for i in range(0,global_v.CLASS_NUM):
            # Store newly created symbol class in the list
            symbolClasses.append(SymbolClass(i, ColorChooser().get_color()))
            # Randomize value for each characteristic of the symbol
            for j in range(0,len(characteristics)):
                symbolClasses[i].characteristicsValues.append(
                    random.uniform(characteristics[j].interval.lowerBound, 
                                   characteristics[j].interval.upperBound))
        # INFO
        for symbolClass in symbolClasses:
            print("Symbol Class:",symbolClass.name, "\n",
                  "Characteristics: ", symbolClass.characteristicsValues, "\n")