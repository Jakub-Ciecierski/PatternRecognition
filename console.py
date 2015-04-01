import sys
import getopt
import util.global_variables as global_v
import datetime

header_length = 94
header_frame_symbol = '%'
point_indent ="    "
subpoint_indent = "        "

def parse_argv(argv):
    # Gather up flags
    try:                                
        opts, args = getopt.getopt(argv, "nc:h:", ["nonhomo","classes=","characteristics="])
        print(args)
    except getopt.GetoptError:          
        usage()                         
        sys.exit(2)              
    # Perform proper actions           
    for opt, arg in opts:               
        if opt in ("-n", "--nonhomo"):      
            global_v.NON_HOMO_CLASSES = True
        elif opt in ("-c", "--classes"):      
            global_v.CLASS_NUM = int(arg)   
        elif opt in ("-h", "--characteristics"):
            global_v.CHAR_NUM = int(arg)

def usage():
    print("to be created")

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
    
def write_point_name(name,text=""):
    sys.stdout.write("{0}{1} {2}\n".format(point_indent,text,name))
    sys.stdout.flush()
def write_point_list(list, text=""):
    sys.stdout.write("{0}{1} ".format(subpoint_indent, text))
    per_line = 0
    for i in range(0, len(list)):
        per_line += 1
        sys.stdout.write("[{0}] ".format(str(list[i])))
        if(per_line % 3 == 0 and i != 0):
            sys.stdout.write("\n")
            if(per_line >= 3):
                sys.stdout.write("{0} ".format(" " * (len(subpoint_indent) + len(text)) ))
        
    sys.stdout.write("\n")
    sys.stdout.flush()
    
def write_name_number(name,number,text=""):
    number_str = str(number) + "%"
    point_length = header_length - len(2 * point_indent)
    sys.stdout.write("{0}{1} {2}:{3}{4}\n".format(point_indent,text,name,"."*(point_length - 2- len(number_str)- len(text)-len(str(name))),number_str ))
    sys.stdout.flush()
    
def write_interval(name,lower_bound,upper_bound, text1="", text2="",text3="",text4=""):
    text_l = header_length - 2 * len(point_indent)
    sys.stdout.write("{0}{1} {2} {3} {4}{5}{6}\n".format(point_indent, 
                                                      text1,
                                                      name, 
                                                      text2, 
                                                      text3, 
                                                      "." * (text_l-
                    (len(text1) + len(str(name))+ len(text2)+len(text3)+len(str(lower_bound))+3)
                                                             ),
                                                      lower_bound))
    sys.stdout.write("{0}{1}{2}{3}\n\n".format(" " *(3+len(point_indent)+ len(text1) + len(str(name)) + len(text2)),
                                        text4,
                                        "." * (text_l-
                    (len(text1) + len(str(name))+ len(text2)+len(text4)+len(str(lower_bound))+3)
                                                             ),
                                        upper_bound))   
     
def write_non_homo(name, group, text1="", text2=""):
    sys.stdout.write("{0}{1}: [{2}] {3}: {4}\n".format(point_indent,text1,name,text2,group ))

'''
    Redirects stdout to a file with unique name
'''
def redirect_stdout():
    global_v.LOADING_BARS = False
    d = datetime.datetime.now().strftime('%Y-%m-%d_%H;%M;%S')
    file = "log/" + str(d) +".txt"
    print("Redirecting output to: " + file)
    for i in range(0, len(file)):
        if file[i] == ' ':
            file[i] = '_'
    f = open(file, 'w')
    sys.stdout = f