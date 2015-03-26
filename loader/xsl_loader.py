from xlrd import open_workbook
from symbol_class import SymbolClass
from util.color_chooser import ColorChooser

'''
    Class used to load symbols and their characteristics
'''
class XslLoader:
    '''
        filepath - path to the xsl file
        maxColumns - how many characteristics we want to read at most
    '''
    def __init__(self, filepath, maxColumns):
        self.filepath = filepath
        self.maxColumns = maxColumns

    '''
        Reads all the sheets and every row attached to it
        For every row, up to maxColulmns columns is read.
        
        Returns as many SymbolClasses as there are different Symbol
        names provided in first column in each row
        For each SymbolClass, DistortedClasses are stored,
        corresponding to that class.
    '''
    def read_symbols(self):
        symbolClasses = []
        print("Opening file:", self.filepath)
        wb = open_workbook(self.filepath)
        for s in wb.sheets():
            for row in range(s.nrows):
                characteristics = []
                for col in range(s.ncols):
                    if col == self.maxColumns + 1:
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
                symbolClass.distortedClasses.append(distortedClass)

                #symbolClasses.append(symbolClass)
        return symbolClasses