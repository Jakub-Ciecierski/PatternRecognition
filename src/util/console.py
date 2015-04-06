import sys
import getopt
import util.global_variables 
import os
import datetime
#from main import symbolClasses

header_length = 94
header_frame_symbol = '%'
point_indent ="    "
subpoint_indent = "        "

def parse_argv(argv):
    # Gather up flags
    try:                                
        opts, args = getopt.getopt(argv, "12c:h:f:t:l:m:", ["test-type-1","test-type-2","classes=","characteristics=","log=","test=","learn=","mvee="])
        print(args)
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)              
    # Perform proper actions           
    for opt, arg in opts:               
        if opt in ("-c", "--classes"):      
            util.global_variables.CLASS_NUM = int(arg)   
        elif opt in ("-h", "--characteristics"):
            util.global_variables.CHAR_NUM = int(arg)
        elif opt in ("-f", "--log"): 
            print(arg, file=sys.stderr)
            util.global_variables.LOG_FILE_PREFIX_NAME = arg
        elif opt in ("-1", "--test-type-1"):
            util.global_variables.TEST_TYPE = util.global_variables.TestType.SYNTHETIC_HOMO_NATIVE
        elif opt in ("-2", "--test-type-2"):
            util.global_variables.TEST_TYPE = util.global_variables.TestType.GROUPING_ASSESSMENT
        elif opt in ("-t", "--test"):
            util.global_variables.N_TEST = int(arg)
        elif opt in ("-l", "--learn"):
            util.global_variables.N_LEARNING = int(arg)
        elif opt in ("-m", "--mvee"):
            util.global_variables.MVEE_ERR = float(arg)
            
    # Prepare global filename for further references
    util.global_variables.DIR_NAME = util.global_variables.TEST_TYPE.name + "_" + datetime.datetime.now().strftime('%Y-%m-%d_%H;%M;%S')
    # Create directory to save information
    os.makedirs(os.path.join("..","log",util.global_variables.DIR_NAME), exist_ok=True)
    
def usage():
    print("to be created", file=sys.stderr)

def write_header(text):
    print()
    print(header_frame_symbol * header_length )
    print(header_frame_symbol,
        " " * int((header_length- len(text))/2-3),
          text,
        " " * int((header_length- len(text))/2-3),
          header_frame_symbol )
    print(header_frame_symbol * header_length, '\n')
    
def write_point_text_number(text, number):
    point_length = header_length - len(2 * point_indent)
    sys.stdout.write("{0}{1}{2}{3}\n".format(point_indent,text,"." * (point_length -  len(text) - len(str(number))),number))
    sys.stdout.flush()
    
def write_symbol_classes(f,name,list, text=""):
    line1 = "{0}{1} {2}\n".format("",text,name)
    sys.stdout.write(point_indent + line1)
    f.write(line1)
    write_point_list(f,list,text)
    
def write_point_list(f,list, text=""):
    line1 = "{0}{1} ".format(subpoint_indent, text)
    sys.stdout.write(line1)
    f.write(line1)
    per_line = 0
    for i in range(0, len(list)):
        per_line += 1
        line2 = "[{0}] ".format(str(list[i]))
        sys.stdout.write(line2)
        f.write(line2)
        if(per_line % 3 == 0 and i != 0):
            sys.stdout.write("\n")
            f.write("\n")
            if(per_line >= 3):
                line3 = "{0} ".format(" " * (len(subpoint_indent) + len(text)) )
                sys.stdout.write(line3)
                f.write(line3)
        
    sys.stdout.write("\n")
    f.write("\n")
    sys.stdout.flush()
    
def write_name_number(name,number,text=""):
    number_str = str(number) + "%"
    point_length = header_length - len(2 * point_indent)
    sys.stdout.write("{0}{1} {2}:{3}{4}\n".format(point_indent,text,name,"."*(point_length - 2- len(number_str)- len(text)-len(str(name))),number_str ))
    sys.stdout.flush()
    
def write_characteristics(f,name,lower_bound,upper_bound, text1="", text2="",text3="",text4=""):
    text_l = header_length - 2 * len(point_indent)
    line1 = "{0}{1} {2} {3} {4}{5}{6}\n".format("", 
                                                      text1,
                                                      name, 
                                                      text2, 
                                                      text3, 
                                                      "." * (text_l-
                    (len(text1) + len(str(name))+ len(text2)+len(text3)+len(str(lower_bound))+3)
                                                             ),
                                                      lower_bound)
    line2 = "{0}{1}{2}{3}\n\n".format(" " *(3+len("")+ len(text1) + len(str(name)) + len(text2)),
                                        text4,
                                        "." * (text_l-
                    (len(text1) + len(str(name))+ len(text2)+len(text4)+len(str(lower_bound))+3)
                                                             ),
                                        upper_bound)   
    
    sys.stdout.write(point_indent+line1)
    f.write(line1)
    sys.stdout.write(point_indent+line2)
    f.write(line2)    
    
     
def write_non_homo(name, group, text1="", text2=""):
    sys.stdout.write("{0}{1}: [{2}] {3}: {4}\n".format(point_indent,text1,name,text2,group ))

'''
    Redirects stdout to a file with unique name
'''
def redirect_stdout():
    util.global_variables.LOADING_BARS = False
    d = datetime.datetime.now().strftime('%Y-%m-%d_%H;%M;%S')
    if util.global_variables.LOG_FILE_PREFIX_NAME:
        prefix = util.global_variables.LOG_FILE_PREFIX_NAME + "_"
    else:
        prefix = ""
    file = "../log/" + prefix +str(d) +".txt"
    print("Redirecting output to: " + file)
    for i in range(0, len(file)):
        if file[i] == ' ':
            file[i] = '_'
    f = open(file, 'w')
    sys.stdout = f

'''
    prints all the symbols of native set
    First prints a header e.g.:
    
    CLASS_NUM: 10
    N_LEARNING: 1000
    N_TEST: 500
    
    For each class, first line is the base native symbol
    around which distortion was computed
    Next N_LEARNING lines is learning set of that symbol,
    Next N_TEST lines is the testing set of that symbol
'''
def print_symbols(symbolClasses):
    print("CLASS_NUM:",util.global_variables.CLASS_NUM)
    print("N_LEARNING:",util.global_variables.N_LEARNING)
    print("N_TEST:",util.global_variables.N_TEST)
    for cl in symbolClasses:
        print(cl.name,end=" ",flush=True)
        for value in cl.characteristicsValues:
            print(value, end=" ",flush=True)
        print()

        for ls in cl.learning_set:
            print(cl.name,end=" ",flush=True)
            for value in ls.characteristicsValues:
                print(value, end=" ",flush=True)
            print()
        for ts in cl.test_set:
            print(cl.name,end=" ",flush=True)
            for value in ts.characteristicsValues:
                print(value, end=" ",flush=True)
            print()
            
def print_config():
    f = open(os.path.join("..","log",util.global_variables.DIR_NAME,"RUN_CONFIG.txt"), 'w')
    double_print(point_indent,"TEST_TYPE:        ", util.global_variables.TEST_TYPE.name, f) 
    double_print(point_indent,"DIR:              ", util.global_variables.DIR_NAME, f)
    double_print(point_indent,"CLASS_NUM:        ", util.global_variables.CLASS_NUM, f)
    double_print(point_indent,"CHAR_NUM:         ", util.global_variables.CHAR_NUM, f)
    double_print(point_indent,"N_LEARNING:       ", util.global_variables.N_LEARNING, f)
    double_print(point_indent,"N_TEST:           ", util.global_variables.N_TEST, f)
    double_print(point_indent, "K:                ", util.global_variables.K, f)
    double_print(point_indent,"ELLPSD_TRESH:     ", util.global_variables.ELLPSD_TRESH, f)
    double_print(point_indent,"MVEE_ERR:         ", util.global_variables.MVEE_ERR, f)
    double_print(point_indent,"HOMO_STD_DEV:     ", util.global_variables.HOMO_STD_DEV, f)
    double_print(point_indent,"NON_HOMO_STD_DEV: ", util.global_variables.NON_HOMO_STD_DEV, f)
    double_print(point_indent,"MAX_K_CLUS_EVALUATION:     ", util.global_variables.MAX_K_CLUS_EVALUATION, f)
    double_print(point_indent,"K_CLOUD_DISTORTION: ", util.global_variables.K_CLOUD_DISTORTION, f)

    f.close()

    
def double_print(indent, s, var, file):
    print(indent + s,var)
    file.write(s + str(var) + '\n')
  
    
    