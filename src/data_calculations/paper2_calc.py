import util.global_variables as global_v
import os

def compute(symbolClasses, foreignClasses):
    os.makedirs(os.path.join("..","log",global_v.DIR_NAME,"results"), exist_ok=True)
    
    native_ellipsoid(symbolClasses)
    native_cuboid(symbolClasses)
    
    foreign_ellipsoid(symbolClasses, foreignClasses)
    foreign_cuboid(symbolClasses, foreignClasses)


def native_ellipsoid(symbolClasses):
    total_count = 0
    belongs_count = 0

    # For every point in native test set,
    # check if it belongs to learning set
    for sym in symbolClasses:
        for point in sym.test_set:
            if belongs_to_native_ellipsoid(point, symbolClasses):
                belongs_count += 1
            total_count += 1
    
    # Confusion matrix parameters in percents
    TP = (belongs_count / total_count )* 100
    FN = 100-TP
    
    f1 = open(os.path.join("..","log",global_v.DIR_NAME,"results","ellipsoid.txt"), 'a')
    
    TPstr = "True Positive (TP) = " + str(TP) + "%" + "(" + str(belongs_count) +"/" +str(total_count) + ") \n"
    FNstr = "False Negative (FN) = " + str(FN) + "%" + "(" + str(total_count - belongs_count) +"/" + str(total_count) + ") \n\n"

    f1.write("Native \n" + TPstr + FNstr)
    f1.close()

def native_cuboid(symbolClasses):
    total_count = 0
    belongs_count = 0

    # For every point in native test set,
    # check if it belongs to learning set
    for sym in symbolClasses:
        for point in sym.test_set:
            if belongs_to_native_cuboid(point, symbolClasses):
                belongs_count += 1
            total_count += 1
    
    # Confusion matrix parameters in percents
    TP = (belongs_count / total_count )* 100
    FN = 100-TP
    f1 = open(os.path.join("..","log",global_v.DIR_NAME,"results","cuboid.txt"), 'a')
    
    TPstr = "True Positive (TP) = " + str(TP) + "%" + "(" + str(belongs_count)+"/"+str(total_count) + ") \n"
    FNstr = "False Negative (FN) = " + str(FN) + "%" + "(" + str(total_count - belongs_count) + "/" + str(total_count) + ") \n\n"

    f1.write("Native \n" + TPstr + FNstr)
    f1.close()


def foreign_ellipsoid(symbolClasses, foreignClasses):
    total_count = 0
    rejected_count = 0
    
    for f in foreignClasses:
        if belongs_to_native_ellipsoid(f, symbolClasses) == False:
            rejected_count += 1
        total_count += 1
        
    TN = (rejected_count / total_count) * 100
    FP = 100 - TN
    
    f1 = open(os.path.join("..","log",global_v.DIR_NAME,"results","ellipsoid.txt"), 'a')
    
    TNstr = "True Negatives (TN) = " + str(TN) + "%" + "(" + str(rejected_count) + "/" + str(total_count) + ") \n"
    FPstr = "False Positives (FP) = " + str(FP) + "%" + "(" + str(total_count - rejected_count) + "/" +str(total_count) + ") \n"

    f1.write("Foreign \n" + FPstr + TNstr)
    f1.close()

def foreign_cuboid(symbolClasses, foreignClasses):
    total_count = 0
    rejected_count = 0
    
    for f in foreignClasses:
        if belongs_to_native_cuboid(f, symbolClasses) == False:
            rejected_count += 1
        total_count += 1
        
    TN = (rejected_count / total_count) * 100
    FP = 100 - TN
    
    f1 = open(os.path.join("..","log",global_v.DIR_NAME,"results","cuboid.txt"), 'a')
    
    TNstr = "True Negatives (TN) = " + str(TN) + "%" + "(" + str(rejected_count )+"/"+ str(total_count) + ") \n"
    FPstr = "False Positives (FP) = " + str(FP) + "%" + "(" + str(total_count - rejected_count)+"/"+str(total_count) + ") \n"

    f1.write("Foreign \n" + FPstr + TNstr)
    f1.close()

def belongs_to_native_ellipsoid(point, symbolClasses):
    for sym in symbolClasses:
        for c in sym.clusters:
            if c.ellipsoid.is_point_in_ellipsoid([point.characteristicsValues[:]], True) == 0:
                return True
    return False

def belongs_to_native_cuboid(point, symbolClasses):
    for sym in symbolClasses:
        for c in sym.clusters:
            if c.cuboid.is_point_in_cuboid(point.characteristicsValues[:]):
                return True
    return False
