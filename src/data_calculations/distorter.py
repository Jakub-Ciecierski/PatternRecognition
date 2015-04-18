from numpy import random, sqrt, log, sin, cos, pi
import random
import util.global_variables as global_v
from symbols.symbol_class import SymbolClass
from symbols.symbol_types import SymbolType
import util.console as console

'''
    Class in charge of creating cloud of N  random 
    points for each (supplied) class of symbols.   
'''
class Distorter:
        
    '''
        For a given n-dimensional point, this method distort  
        it coordinates according to normal distribution.     
        In addition user can specify standard deviation of   
        this process      
    '''                                   
    def __generate_distortion(self, cloudCenterCoordinates,sigmaSqrt):
        distortedCenter = []
        for i in range(len(cloudCenterCoordinates)):
            distortedCenter.append(cloudCenterCoordinates[i]+ random.gauss(0, sigmaSqrt))
        return distortedCenter
    
            
    def create_homogeneus_cloud(self, symbolClasses):
        for cl in symbolClasses:
            # Learning set
            for i in range(0, global_v.N_LEARNING + global_v.N_TEST):
                # instance of new symbol
                distortedClass = SymbolClass(cl.name, cl.color, type = SymbolType.NATIVE_LEARNING)
                # randomize position around a given class(based on position)
                distortedClass.characteristicsValues = self.__generate_distortion(
                                                                cl.characteristicsValues[:],
                                                                global_v.HOMO_STD_DEV)
                # store result 
                if(i < global_v.N_LEARNING):
                    cl.learning_set.append(distortedClass)
                else:
                    cl.test_set.append(distortedClass)
            print(cl.name)        
            console.write_point_text_number(">> Number of learning set points", 
                                len(cl.learning_set))
            console.write_point_text_number(">> Number of test set points", 
                                            len(cl.test_set))    
                           
    def create_non_homogeneus_cloud(self, symbolClasses):
        indicator = 1.0
        ratio = global_v.N_LEARNING/(global_v.N_LEARNING+global_v.N_TEST)
        for cl in symbolClasses:
            for i in range(0, int(indicator)):

                # instance of new symbol
                distortedClass = SymbolClass(cl.name, cl.color)
                # randomize position around a given class(based on position)
                distortedClass.characteristicsValues = self.__generate_distortion(
                                                                cl.characteristicsValues[:],
                                                                global_v.HOMO_STD_DEV)
                
                scope =  int((global_v.N_LEARNING + global_v.N_TEST)/int(indicator))   
                for j in range (0, scope):
                    cloud_point = SymbolClass(cl.name, cl.color)
                    cloud_point.characteristicsValues = self.__generate_distortion(
                                                                distortedClass.characteristicsValues[:], 
                                                                global_v.NON_HOMO_STD_DEV)
                    # store result
                    if(j < ratio * scope):
                        cl.learning_set.append(cloud_point)
                    else:
                        cl.test_set.append(cloud_point)
                    

            # Info about number of created points
            console.write_non_homo(cl.name, int(indicator), "Symbol Class", "Groups")
            console.write_point_text_number(">> Number of distorted classes per symbol", len(cl.learning_set) + len(cl.test_set))
            console.write_point_text_number(">> Number of learning set points", 
                                            len(cl.learning_set))
            console.write_point_text_number(">> Number of test set points", 
                                            len(cl.test_set))    
            indicator += 0.5
    
    '''
        Distributed the data into obvious k clouds
        Used to test evaluation of clustering methods
        and should not be used otherwise. 
    '''
    def create_k_clouds(self, k ,symbolClasses):
        count_in_cloud = int(global_v.N_LEARNING/k)
        for cl in symbolClasses:
            for i in range(0, k):
                for j in range(0, count_in_cloud):
                    # instance of new symbol
                    distortedClass = SymbolClass(cl.name, cl.color)
                    
                    values = []
                    for v in range(0,len(cl.characteristicsValues)):
                        values.append(cl.characteristicsValues[v] + (cl.characteristicsValues[v]*i*0.5) )
                    
                    # randomize position around a given class(based on position)
                    distortedClass.characteristicsValues = self.__generate_distortion(
                                                                    values,
                                                                    global_v.HOMO_STD_DEV)
                    cl.learning_set.append(distortedClass)
                for j in range(0, int(count_in_cloud/2)):
                    # instance of new symbol
                    distortedClass = SymbolClass(cl.name, cl.color)
                    
                    values = []
                    for v in range(0,len(cl.characteristicsValues)):
                        values.append(cl.characteristicsValues[v] + (cl.characteristicsValues[v]*i*5) )
                    
                    # randomize position around a given class(based on position)
                    distortedClass.characteristicsValues = self.__generate_distortion(
                                                                    values,
                                                                    global_v.HOMO_STD_DEV)
                    cl.test_set.append(distortedClass)

    def create_cluster_assessment_cloud(self, k, symbolClasses):
        ratio = global_v.N_LEARNING/(global_v.N_LEARNING+global_v.N_TEST)
        for cl in symbolClasses:
            for i in range(0, int(k)):
    
                # instance of new symbol
                distortedClass = SymbolClass(cl.name, cl.color)
                # randomize position around a given class(based on position)
                distortedClass.characteristicsValues = self.__generate_distortion(
                                                                cl.characteristicsValues[:],
                                                                5.5)
                
                scope =  int((global_v.N_LEARNING + global_v.N_TEST)/int(k))   
                for j in range (0, scope):
                    cloud_point = SymbolClass(cl.name, cl.color)
                    cloud_point.characteristicsValues = self.__generate_distortion(
                                                                distortedClass.characteristicsValues[:], 
                                                                global_v.NON_HOMO_STD_DEV)
                    # store result
                    if(j < ratio * scope):
                        cl.learning_set.append(cloud_point)
                    else:
                        cl.test_set.append(cloud_point)
                    
    
            # Info about number of created points
            console.write_non_homo(cl.name, int(k), "Symbol Class", "Groups")
            console.write_point_text_number(">> Number of distorted classes per symbol", len(cl.learning_set) + len(cl.test_set))
            console.write_point_text_number(">> Number of learning set points", 
                                            len(cl.learning_set))
            console.write_point_text_number(">> Number of test set points", 
                                            len(cl.test_set))    
