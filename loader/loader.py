from xlrd import open_workbook
from symbol_class import SymbolClass
from util.color_chooser import ColorChooser
from test.test_importlib.extension.util import FILEPATH

'''
    Reads all the sheets and every row attached to it
    For every row, up to maxColulmns columns is read.
    
    Returns as many SymbolClasses as there are different Symbol
    names provided in first column in each row
    For each SymbolClass, DistortedClasses are stored,
    corresponding to that class.
    
    filepath - path to the xsl file
    startRow - which row to start reading from
    maxColumns - how many characteristics we want to read at most
'''
def load_xsl(filepath, startRow, maxColumns):
    symbolClasses = []
    print("Opening file:", filepath)
    wb = open_workbook(filepath)
    for s in wb.sheets():
        for row in range(startRow, s.nrows):
            characteristics = []
            for col in range(s.ncols):
                if col == maxColumns + 1:
                    break

                currentValue = s.cell(row,col).value
                # create new symbol class
                if  (
                        (row != 0 and col == 0 and 
                            currentValue != symbolClasses[len(symbolClasses)-1].name) or
                        (row == 0 and col == 0)
                    ):
                    symbolClass = SymbolClass(currentValue, ColorChooser().get_color())
                    symbolClasses.append(symbolClass)
                if col == 0:
                    continue
                characteristics.append(currentValue)
            distortedClass = SymbolClass(symbolClass.name, symbolClass.color)
            distortedClass.characteristicsValues = characteristics
            symbolClass.learning_set.append(distortedClass)

            #symbolClasses.append(symbolClass)
    return symbolClasses

'''
    TODO have to change global variables
'''
def load_txt(filepath):
    symbolClasses = []

    filepath = 'native1.txt'
    f = open(filepath)
    lines = f.readlines()
    class_num = lines[0].split()[1]
    n_learning = lines[1].split()[1]
    n_test = lines[2].split()[1]
    prev_name = 0

    for i in range(3, len(lines)):
        line = lines[i].split()
        name = line[0]
        if prev_name != name or i == 3: 
            symbolClass = SymbolClass(name, ColorChooser().get_color())
            for c in range(1,len(line)):
                symbolClass.characteristicsValues.append(float(line[c]))
            symbolClasses.append(symbolClass)
        else:
            symbol = SymbolClass(symbolClasses[int(name)].name, symbolClasses[int(name)].color)
            for c in range(1,len(line)):
                symbol.characteristicsValues.append(float(line[c]))
            if((i - 3)%(int(n_learning) +int(n_test) + 1)  < int(n_learning) ):
                symbolClasses[int(name)].learning_set.append(symbol)
            else:
                symbolClasses[int(name)].test_set.append(symbol)
        prev_name = name
    return symbolClasses