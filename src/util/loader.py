from xlrd import open_workbook
from symbols.symbol_class import SymbolClass
from util.color_chooser import ColorChooser
import util.global_variables as global_v
#from test.test_importlib.extension.util import FILEPATH
import random
import util.logger as logger

'''
    Reads all the sheets and every row attached to it
    For every row, up to maxColulmns columns is read.

    Returns as many SymbolClasses as there are different Symbol
    names provided in first column in each row
    For each SymbolClass, DistortedClasses are stored,
    corresponding to that class.

    Native set is split into Training and Testing set
    randomly.

    filepath - path to the xsl file
    startRow - which row to start reading from
    maxColumns - how many characteristics we want to read at most
'''
def load_native_xls():
    startRow = global_v.XLS_START_ROW
    maxColumns = global_v.XLS_MAX_COL

    symbolClasses = []

    logger.log("Opening file: " + str(global_v.NATIVE_FILE_PATH))

    wb = open_workbook(global_v.NATIVE_FILE_PATH)
    for s in wb.sheets():
        for row in range(startRow, s.nrows):
            characteristics = []
            for col in range(s.ncols):
                if maxColumns > 0 and col == maxColumns + 1:
                    break

                currentValue = float(str(s.cell(row,col).value).replace(',','.'))
                # create new symbol class
                if  (
                        (row != startRow and col == 0 and
                            currentValue != symbolClasses[len(symbolClasses)-1].name) or
                        (row == startRow and col == 0)
                    ):
                    symbolClass = SymbolClass(int(currentValue), ColorChooser().get_color())
                    symbolClasses.append(symbolClass)
                if col == 0:
                    continue
                characteristics.append(currentValue)
            distortedClass = SymbolClass(symbolClass.name, symbolClass.color)
            distortedClass.characteristicsValues = characteristics
            random.choice((symbolClass.learning_set,symbolClass.test_set)).append(distortedClass)
    return symbolClasses

#-----------------------------------------------------------------------------------------

def load_foreign_xls():
    startRow = global_v.XLS_START_ROW
    maxColumns = global_v.XLS_MAX_COL

    foreignClasses = []

    logger.log("Opening file: " + str(global_v.FOREIGN_FILE_PATH))

    path = ""
    wb = open_workbook(global_v.FOREIGN_FILE_PATH)
    for s in wb.sheets():
        for row in range(startRow, s.nrows):
            characteristics = []
            for col in range(s.ncols):
                if maxColumns > 0 and col == maxColumns + 1:
                    break

                currentValue = float(str(s.cell(row,col).value).replace(',','.'))
                if col == 0:
                    continue
                characteristics.append(currentValue)

            foreignClass = SymbolClass('foreign', ColorChooser().getForeignColor)
            foreignClass.characteristicsValues = characteristics
            foreignClasses.append(foreignClass)

    return foreignClasses

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

def serialize_choosen_elements(nativeElements):
    logger.log_header("Choosing Native elements")
    chosenNativeElements = SymbolClass("Chosen of Classes: ",
                                        ColorChooser().get_color())

    m_filename = "["

    # Go through all symbols classes and choose the classes we want
    for i in range(0, len(nativeElements)):
        if (nativeElements[i].name in global_v.NATIVE_CLASSES or
                len(global_v.NATIVE_CLASSES) == 0):
            chosenNativeElements.learning_set += nativeElements[i].learning_set
            chosenNativeElements.test_set += nativeElements[i].test_set

            chosenNativeElements.name += str(nativeElements[i].name) + ", "
            m_filename += str(nativeElements[i].name) + ", "

    chosenNativeElements.name = chosenNativeElements.name.rstrip(", ")
    m_filename = m_filename.rstrip(", ")
    m_filename += "]"

    for learning_element in chosenNativeElements.learning_set:
        element_str = str(learning_element.characteristicsValues)
        element_str = element_str.strip("[]")
        element_str = element_str.rstrip("]")

        logger.log(element_str,
                    filename="training" + "_" + m_filename + ".txt",
                    styles=[logger.LogStyle.NONE, logger.LogStyle.FILE_ONLY],
                    text_indent="")

    for test_element in chosenNativeElements.test_set:
        element_str = str(test_element.characteristicsValues)
        element_str = element_str.strip("[]")
        element_str = element_str.rstrip("]")

        logger.log(element_str,
                filename="test" + "_" + m_filename + ".txt",
                styles=[logger.LogStyle.NONE, logger.LogStyle.FILE_ONLY],
                text_indent="")

    # Log
    logger.log(str(chosenNativeElements))

    return chosenNativeElements

#-----------------------------------------------------------------------------------------

def deserialize_native():
    f = open(global_v.NATIVE_TRAINING_FILE)
    lines = f.readlines()

    line = lines[2].split(", ")

    wat = float(line[0])

    logger.log(line)

    logger.log(wat)

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------

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
