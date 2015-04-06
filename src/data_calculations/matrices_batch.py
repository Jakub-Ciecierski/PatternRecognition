import util.global_variables 
import os
from enum import Enum
'''
    To wrap all confusion matrices in one place,
    I present this class. 
'''
class MatricesBatch:
    def __init__(self, radius):
        self.__m_conf_learn             = self.__m_init(util.global_variables.CLASS_NUM, util.global_variables.CLASS_NUM+2)
        self.__m_conf_test              = self.__m_init(util.global_variables.CLASS_NUM, util.global_variables.CLASS_NUM+2)
        self.__m_eucl_conf_learn        = self.__m_init(util.global_variables.CLASS_NUM, util.global_variables.CLASS_NUM+2)
        self.__m_eucl_conf_test         = self.__m_init(util.global_variables.CLASS_NUM, util.global_variables.CLASS_NUM+2)
        self.__m_conf_homo_foreign      = self.__m_init(1, util.global_variables.CLASS_NUM+2)
        self.__m_conf_nonhomo_foreign   = self.__m_init(1, util.global_variables.CLASS_NUM+2)
        self.__radius_val = radius
    '''
        Initialize matrix with specified number of rows and columns.
        This method obviously can be used to specified vectors as well.
    '''
    def __m_init(self, rows, columns):
        matrix = []
        for r in range(0, rows):
            row = []
            matrix.append(row)
            for c in range(0,columns):
                matrix[r].append(0)
        return matrix
    
            
    def data(self,value,class_n, op_type, set_type , m_type, column, native_no = 0):
        if(set_type == DataInfo.LEARN):
            if(m_type == DataInfo.BASIC):
                if(column == DataInfo.AMB):
                    # LEARNING SET | BASIC CLASSIFICATION | AMBIGUOUS
                    if(op_type == DataInfo.SAVE):
                        self.__m_conf_learn[class_n][util.global_variables.CLASS_NUM] += value
                    elif(op_type == DataInfo.GET):
                        return 100 * self.__m_conf_learn[class_n][util.global_variables.CLASS_NUM] / util.global_variables .N_LEARNING
                    
                elif(column == DataInfo.NOT_CLASS):
                    # LEARNING SET | BASIC CLASSIFICATION | NOT CLASSIFIED
                    if(op_type == DataInfo.SAVE):
                        self.__m_conf_learn[class_n][util.global_variables.CLASS_NUM+1] += value
                    elif(op_type == DataInfo.GET):
                        return 100 * self.__m_conf_learn[class_n][util.global_variables.CLASS_NUM+1] / util.global_variables.N_LEARNING
                    
                elif(column == DataInfo.NATIVE_CLASS):
                    # LEARNING SET | BASIC CLASSIFICATION | NATIVE CLASS
                    if(op_type == DataInfo.SAVE):
                        self.__m_conf_learn[class_n][native_no] +=value
                    elif(op_type == DataInfo.GET):
                        return 100 * self.__m_conf_learn[class_n][native_no] / util.global_variables.N_LEARNING
                    
            elif(m_type == DataInfo.EUCL):
                if(column == DataInfo.AMB):
                    self.__m_eucl_conf_learn[class_n][util.global_variables.CLASS_NUM] += value
                elif(column == DataInfo.NOT_CLASS):
                    self.__m_eucl_conf_learn[class_n][util.global_variables.CLASS_NUM+1] += value
                elif(column == DataInfo.NATIVE_CLASS):  
                    self.__m_eucl_conf_learn[class_n][native_no] += value
                    
        elif(set_type == DataInfo.TEST):  
            if(m_type == DataInfo.BASIC):
                if(column == DataInfo.AMB):
                    # TEST SET | BASIC CLASSIFICATION | AMBIGUOUS
                    if(op_type == DataInfo.SAVE):
                        self.__m_conf_test[class_n][util.global_variables.CLASS_NUM] += value
                    elif(op_type == DataInfo.GET):
                        return 100 * self.__m_conf_test[class_n][util.global_variables.CLASS_NUM] / util.global_variables.N_TEST
                    
                elif(column == DataInfo.NOT_CLASS):
                    # TEST SET | BASIC CLASSIFICATION | NOT CLASSIFIED
                    if(op_type == DataInfo.SAVE):
                        self.__m_conf_test[class_n][util.global_variables.CLASS_NUM+1] += value
                    elif(op_type == DataInfo.GET):
                        return 100 * self.__m_conf_test[class_n][util.global_variables.CLASS_NUM+1] / util.global_variables.N_TEST
                    
                elif(column == DataInfo.NATIVE_CLASS):
                    # TEST SET | BASIC CLASSIFICATION | NATIVE CLASS
                    if(op_type == DataInfo.SAVE):
                        self.__m_conf_test[class_n][native_no] += value
                    elif(op_type == DataInfo.GET):
                        return 100 * self.__m_conf_test[class_n][native_no] / util.global_variables.N_TEST
 
            elif(m_type == DataInfo.EUCL):
                if(column == DataInfo.AMB):
                    self.__m_eucl_conf_test[class_n][util.global_variables.CLASS_NUM] += value
                elif(column == DataInfo.NOT_CLASS):
                    self.__m_eucl_conf_test[class_n][util.global_variables.CLASS_NUM+1] += value
                elif(column == DataInfo.NATIVE_CLASS):  
                    self.__m_eucl_conf_test[class_n][native_no] += value 
            
        elif(set_type == DataInfo.FOREIGN):
            if(m_type == DataInfo.HOMO):
                if(column == DataInfo.AMB):
                    # FOREIGN | HOMO | AMBIGUOUS
                    self.__m_conf_homo_foreign[0][util.global_variables.CLASS_NUM] += value
                elif(column == DataInfo.NOT_CLASS):
                    # FOREIGN | HOMO | REJECTED
                    self.__m_conf_homo_foreign[0][util.global_variables.CLASS_NUM + 1] += value
                elif(column == DataInfo.NATIVE_CLASS):
                    # FOREIGN | HOMO | NATIVE CLASS
                    self.__m_conf_homo_foreign[0][native_no] += value
            elif(m_type == DataInfo.NONHOMO):
                if(column == DataInfo.AMB):
                    # FOREIGN | NON HOMO | AMBIGUOUS
                    self.__m_conf_nonhomo_foreign[0][util.global_variables.CLASS_NUM] += value
                elif(column == DataInfo.NOT_CLASS):
                    # FOREIGN | NON HOMO | REJECTED
                    self.__m_conf_nonhomo_foreign[0][util.global_variables.CLASS_NUM + 1] += value
                elif(column == DataInfo.NATIVE_CLASS):
                    # FOREIGN | NON HOMO | NATIVE CLASS
                    self.__m_conf_nonhomo_foreign[0][native_no] += value
            
    def summarization(self, class_n, set_type, m_type):
        # Print out results  
        print("        >> Symbol:", [class_n])
        print("           Unambiguous points:                            ",
              self.data(-1, class_n, DataInfo.GET, set_type, m_type, DataInfo.NATIVE_CLASS, class_n),"%")
        print("           Ambiguous points:                              ",
              self.data(-1, class_n, DataInfo.GET, set_type, m_type, DataInfo.AMB),"%")
        print("           Not Classified points:                         ",
              self.data(-1, class_n, DataInfo.GET, set_type, m_type, DataInfo.NOT_CLASS),"%")

    def print_matrix(self, set_type, m_type):
        if(set_type == DataInfo.LEARN):
            if(m_type == DataInfo.BASIC):
                f = open(os.path.join("..","log",util.global_variables.DIR_NAME,"r"+str(self.__radius_val)+"__m_conf_learning_non_euclid.txt"), 'w')
                self.__print(f,self.__m_conf_learn)
                f.close()
            elif(m_type == DataInfo.EUCL):
                f = open(os.path.join("..","log",util.global_variables.DIR_NAME,"r"+str(self.__radius_val)+"__m_conf_learning_euclid.txt"), 'w')
                self.__print(f,self.__m_eucl_conf_learn)  
                f.close()
        if(set_type == DataInfo.TEST):
            if(m_type == DataInfo.BASIC):
                f = open(os.path.join("..","log",util.global_variables.DIR_NAME,"r"+str(self.__radius_val)+"__m_conf_test_non_euclid.txt"), 'w')
                self.__print(f,self.__m_conf_test)
                f.close()
            elif(m_type == DataInfo.EUCL):
                f = open(os.path.join("..","log",util.global_variables.DIR_NAME,"r"+str(self.__radius_val)+"__m_conf_test_euclid.txt"), 'w')
                self.__print(f,self.__m_eucl_conf_test)           
                f.close()    
                
        if(set_type == DataInfo.FOREIGN):
            if(m_type == DataInfo.HOMO):
                f = open(os.path.join("..","log",util.global_variables.DIR_NAME,"r"+str(self.__radius_val)+"__m_conf_foreign_homo.txt"), 'w')
                self.__print(f,self.__m_conf_homo_foreign, util.global_variables.CLASS_NUM*util.global_variables.N_LEARNING)
                f.close()
            if(m_type == DataInfo.NONHOMO):
                f = open(os.path.join("..","log",util.global_variables.DIR_NAME,"r"+str(self.__radius_val)+"__m_conf_foreign_non_homo.txt"), 'w')
                self.__print(f,self.__m_conf_nonhomo_foreign, util.global_variables.CLASS_NUM*util.global_variables.N_LEARNING)
                f.close()
    '''
        Saves matrix to a file
    '''
    def __print(self,f, matrix, divider = util.global_variables.N_LEARNING):
        for r in range(0, len(matrix)):
            for c in range(0, len(matrix[r])):
                f.write(str(round(100*matrix[r][c]/divider,2)) +' | ')
            f.write("\n")

DataInfo = Enum('DataInfo','TEST LEARN EUCL BASIC AMB NATIVE_CLASS NOT_CLASS SAVE GET FOREIGN HOMO NONHOMO')            