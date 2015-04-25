from clustering.elllipsoid import  Ellipsoid
from clustering.cuboid import Cuboid
from enum import Enum
import util.console as console
from clustering import cuboid
from util.basic_math import sort_by_distance
from util.basic_math import euclidian_distance
import os
import util.global_variables as global_v

point_indent ="    "

class BasicMembership:
    '''
    TODO
    '''
    def __init__(self, symbolClasses, with_test=True):
        self.ellipsoids         = self.__generate_objects(symbolClasses, ObjectType.ELLIPSOID, with_test)
        self.cuboids            = self.__generate_objects(symbolClasses, ObjectType.CUBOID,with_test)
        self.percentage         = 0
        self.ellipsoids_folder  = "ellipsoids"
        self.cuboids_folder     = "cuboids"
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%"), exist_ok=True)

    
    def shrink_objects(self, percentage_of_points):
        self.percentage += percentage_of_points
        print("PERCENTAGE",self.percentage)
        self.shrink_ellipsoids(percentage_of_points)
        self.shrink_cuboids(percentage_of_points)
        if percentage_of_points != 0:
            self.recalculate_ellipsoids()
            self.recalculate_cuboids()
    '''
    '''
    def shrink_ellipsoids(self, percentage_of_points):
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder), exist_ok=True)
        how_many_to_remove = int((percentage_of_points/100) * len(self.ellipsoids[0].points))
        
        for ellipsoid in self.ellipsoids:
            for i in range(0,how_many_to_remove):
                ellipsoid.remove_longest_point()
            f = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder,"points_in_ellipsoid_"+str(ellipsoid.name)+".txt"), 'w')
            double_print(point_indent,"POINTS:        ", len(ellipsoid.points), f)
            f.close()
    '''
    '''
    def shrink_cuboids(self, percentage_of_points):
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder), exist_ok=True)
        how_many_to_remove = int((percentage_of_points/100) * len(self.cuboids[0].points))
        
        for cuboid in self.cuboids:
            for i in range(0,how_many_to_remove):
                cuboid.remove_longest_point()    
            f = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder,"points_in_cuboid_"+str(cuboid.name)+".txt"), 'w')
            double_print(point_indent,"POINTS:        ", len(cuboid.points), f)
            f.close()
            
        

    def check_natives_ellipsoid(self,symbolClasses, name_homo, name_non_homo):
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder), exist_ok=True)      
        rejected = []
        for cl in symbolClasses:
            for point in cl.test_set:
                in_how_many = []
                for ellipsoid in self.ellipsoids:
                    if ellipsoid.ellipsoid.is_point_in_ellipsoid([point.characteristicsValues[:]],True) == 0:
                        in_how_many.append(point)
                        break;
                    
                if len(in_how_many) == 0:
                    rejected.append(point)    
             
                    
        f1 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder,"m_"+name_homo+".txt"), 'a')   
        f2 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder,"m_"+name_non_homo+".txt"), 'a')         
        tp_string = "Native:   TP ="+ str(((len(cl.learning_set)*len(symbolClasses)-len(rejected))/(len(cl.learning_set)*len(symbolClasses))*100)) + "% (" + str(len(cl.learning_set)*len(symbolClasses)-len(rejected)) + "/" +str(len(cl.learning_set)*len(symbolClasses))+ ")  "
        fn_string = "|| FN ="+ str(((len(rejected))/(len(cl.learning_set)*len(symbolClasses)))*100) + "% (" + str(len(rejected)) + "/" +str(len(cl.learning_set)*len(symbolClasses)) + ")  \n"
        f1.write(tp_string + fn_string)
        f2.write(tp_string + fn_string)
        
        f1.close()
        f2.close()
 
    def check_natives_cuboid(self,symbolClasses, name_homo, name_non_homo):
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder), exist_ok=True)      
        rejected = []
        for cl in symbolClasses:
            for point in cl.test_set:
                in_how_many = []
                for cuboid in self.cuboids:
                    if cuboid.cuboid.is_point_in_cuboid(point.characteristicsValues[:]):
                        in_how_many.append(point)
                        break; 
                    
                if len(in_how_many) == 0:
                    rejected.append(point)    
             
                    
        f1 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder,"m_"+name_homo+".txt"), 'a')   
        f2 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder,"m_"+name_non_homo+".txt"), 'a')         
        tp_string = "Native:   TP ="+ str(((len(cl.learning_set)*len(symbolClasses)-len(rejected))/(len(cl.learning_set)*len(symbolClasses))*100)) + "% (" + str(len(cl.learning_set)*len(symbolClasses)-len(rejected)) + "/" +str(len(cl.learning_set)*len(symbolClasses))+ ")  "
        fn_string = "|| FN ="+ str(((len(rejected))/(len(cl.learning_set)*len(symbolClasses)))*100) + "% (" + str(len(rejected)) + "/" +str(len(cl.learning_set)*len(symbolClasses)) + ")  \n"
        f1.write(tp_string + fn_string)
        f2.write(tp_string + fn_string)
        
        f1.close()
        f2.close()
        
    def check_natives_ellipsoid_proper(self,symbolClasses, name_homo, name_non_homo):
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder), exist_ok=True)      
        rejected = []
        
        total_count = 0
        belongs_count = 0
        
        for cl in symbolClasses:
            for point in cl.test_set:
                total_count += 1
                for ellipsoid in self.ellipsoids:
                    if ellipsoid.ellipsoid.is_point_in_ellipsoid([point.characteristicsValues[:]],True) == 0:
                        belongs_count += 1
                        break;

        TP = (belongs_count/total_count)*100
        FN = 100 - TP
        
        f1 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder,"m_"+name_homo+".txt"), 'a')   
        f2 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder,"m_"+name_non_homo+".txt"), 'a')         
        tp_string = "Native:   TP ="+ str(TP) + "% (" + str(belongs_count) + "/" +str(total_count)+ ")  "
        fn_string = "|| FN ="+ str(FN) + "% (" + str(total_count - belongs_count) + "/" +str(total_count) + ")  \n"
        f1.write(tp_string + fn_string)
        f2.write(tp_string + fn_string)
        
        f1.close()
        f2.close()
 
    def check_natives_cuboid_proper(self,symbolClasses, name_homo, name_non_homo):
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder), exist_ok=True)      
        rejected = []
        
        total_count = 0
        belongs_count = 0
        
        for cl in symbolClasses:
            for point in cl.test_set:
                total_count += 1
                for cuboid in self.cuboids:
                    if cuboid.cuboid.is_point_in_cuboid(point.characteristicsValues[:]):
                        belongs_count += 1
                        break; 
        
        TP = (belongs_count/total_count)*100
        FN = 100 - TP

        f1 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder,"m_"+name_homo+".txt"), 'a')   
        f2 = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder,"m_"+name_non_homo+".txt"), 'a')         
        tp_string = "Native:   TP ="+ str(TP) + "% (" + str(belongs_count) + "/" +str(total_count)+ ")  "
        fn_string = "|| FN ="+ str(FN) + "% (" + str(total_count - belongs_count) + "/" +str(total_count) + ")  \n"
        f1.write(tp_string + fn_string)
        f2.write(tp_string + fn_string)
        
        f1.close()
        f2.close()

    '''
    '''
    def check_foreign_ellipsoid(self, foreigns,name):
        os.makedirs(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder), exist_ok=True)
        rejected = []
        for foreign in foreigns:
            in_how_many = []
            for ellipsoid in self.ellipsoids:
                if ellipsoid.ellipsoid.is_point_in_ellipsoid([foreign.characteristicsValues[:]],True) == 0:
                    in_how_many.append(foreign)
                    break;
                
            if len(in_how_many) == 0:
                rejected.append(foreign)
                
        f = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.ellipsoids_folder,"m_"+name+".txt"), 'a')
        print("[ELLIPSOIDS] HOW MANY REJECTED: ",len(rejected)/len(foreigns))
        f.write("Foreign:  FP ="+ str(((len(foreigns)-len(rejected))/len(foreigns)*100)) + "% (" + str(len(foreigns)-len(rejected)) + "/" +str(len(foreigns))+ ")  ")
        f.write("|| TN ="+ str(((len(rejected))/len(foreigns))*100) + "% (" + str(len(rejected)) + "/" +str(len(foreigns)) + ")  ")
        f.close()
    
    '''
    '''
    def check_foreign_cuboids(self, foreigns,name):
        rejected = []
        for foreign in foreigns:
            in_how_many = []
            for cuboid in self.cuboids:
                if cuboid.cuboid.is_point_in_cuboid(foreign.characteristicsValues[:]):
                    in_how_many.append(foreign)
                    break;                    
                    
            if len(in_how_many) == 0:
                rejected.append(foreign)           

        f = open(os.path.join("..","log",global_v.DIR_NAME,str(self.percentage) + "_%",self.cuboids_folder,"m_"+name+".txt"), 'a')
        print("[CUBOIDS] HOW MANY REJECTED: ",len(rejected)/len(foreigns))
        f.write("Foreign:  FP ="+ str(((len(foreigns)-len(rejected))/len(foreigns)*100)) + "% (" + str(len(foreigns)-len(rejected)) + "/" +str(len(foreigns))+")   ")
        f.write("|| TN ="+ str(((len(rejected))/len(foreigns))*100) + "% (" + str(len(rejected)) + "/" +str(len(foreigns))+ ")  ")
        f.close()
      
    '''
    TODO
    '''        
    def __generate_objects(self, symbolClasses, type, with_test):
        set_of_objects = []
        for cl in symbolClasses:
            # Gather up points from each distorted class
            temp_points = []
            test_tmp = []
            for el in cl.learning_set:
                temp_points.append(el.characteristicsValues[:])
            
            if with_test:
                for el in cl.test_set:
                    test_tmp.append(el.characteristicsValues[:])
                
            if(type == ObjectType.ELLIPSOID):
                ellipsoid = Ellipsoid(temp_points)
                # Check accuracy 
                pointsInEllipsoid = ellipsoid.is_point_in_ellipsoid(temp_points,False, True)
                print("           Points in Ellipsoid:                            ", 100 * len(pointsInEllipsoid)/len(temp_points),"%")
                # Test set
                if with_test:
                    testPoints = ellipsoid.is_point_in_ellipsoid(test_tmp,False, True)
                    f = open(os.path.join("..","log",global_v.DIR_NAME,"TEST_SET_ACCURACY.txt"), 'a')
                    f.write("class [" + str(cl.name)+ "] ")
                    f.write("ellipsoid " + str(100 * len(testPoints)/len(test_tmp))+"%\n")
                    f.close()
                    print("           Test set accuracy:                              ", 100 * len(testPoints)/len(test_tmp),"%")                
                # Save an ellipsoid
                set_of_objects.append(EllipsoidWrap(temp_points,ellipsoid,cl.name))
                
            if(type == ObjectType.CUBOID):
                cuboid = Cuboid(temp_points)
                # Check accuracy
                pointsInCuboid = cuboid.points_in_cuboid(temp_points)
                print("           Points in Cuboid:                               ", 100 * len(pointsInCuboid)/len(temp_points),"%")
                # Test set
                if with_test:
                    testPoints = cuboid.points_in_cuboid(test_tmp)
                    print("           Test set accuracy:                              ", 100 * len(testPoints)/len(test_tmp),"%")   
                    f = open(os.path.join("..","log",global_v.DIR_NAME,"TEST_SET_ACCURACY.txt"), 'a')
                    f.write("class [" + str(cl.name)+ "] ")
                    f.write("cuboid " + str(100 * len(testPoints)/len(test_tmp))+ "%\n")
                    f.close()
                # Save an ellipsoid
                set_of_objects.append(CuboidWrap(temp_points,cuboid, cl.name))
            
        return set_of_objects
    
    '''
    '''
    def recalculate_ellipsoids(self):
        print("           >> Recalculating ellipsoids")
        for ellipsoid in self.ellipsoids:
            ellipsoid.recalculate()
            
    '''
    '''
    def recalculate_cuboids(self):
        print("           >> Recalculating cuboids")
        for cuboid in self.cuboids:
            cuboid.recalculate()
    
ObjectType = Enum('ObjectType','ELLIPSOID CUBOID')

class EllipsoidWrap:
    def __init__(self,points,ellipsoid, name):
        self.ellipsoid = ellipsoid
        self.points = sort_by_distance(points, ellipsoid.center)
        self.name = name
        
    def recalculate(self):
        self.ellipsoid = Ellipsoid(self.points)
    
    def remove_longest_point(self):
        del self.points[0]   
        
class CuboidWrap:
    def __init__(self,points,cuboid, name):
        self.cuboid = cuboid
        self.points = sort_by_distance(points, cuboid.center)
        self.name = name
        
    def recalculate(self):
        self.cuboid = Cuboid(self.points)     
        
    def remove_longest_point(self):
        del self.points[0]         
        
def double_print(indent, s, var, file):
    print(indent + s,var)
    file.write(s + str(var) + '\n') 