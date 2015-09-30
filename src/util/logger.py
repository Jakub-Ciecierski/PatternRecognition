import sys
import util.global_variables as global_v
import os
import datetime
from enum import Enum
import shutil

"""
    File names
"""
LOG_SYMBOLS_FILE_NAME = "symbols.txt"
LOG_DEFAULT_FILE_NAME = "log.txt"
LOG_CONFIG_FILE_NAME = "config.txt"
LOG_CLUSTER_FILE_NAME = "cluster_evaluation.txt"

LOG_RESULTS_ELLIPSOIDS_FILE_NAME = "results_ellipsoids.txt"
LOG_RESULTS_CUBOIDS_FILE_NAME = "results_cuboids.txt"

"""
    Message templates:

    SEPARATOR_END:      Adds a separation line (width of the console)
                        after the log

    SEPARATOR_START:    Adds a separation line (width of the console)
                        before the log

    TIME_STAMP:         Add a timestamp before the log

    FILE_ONLY:
                        Logs only to a file
"""
LogStyle = Enum('LogStyle', 'NONE SEPARATOR_END SEPARATOR_START TIME_STAMP FILE_ONLY')

"""
    Header styles:

    MAIN_HEADER:        Big header, representing a chapter entry

    SUB_HEADER:         Medium header, representing a sub chapter entry

"""
LogHeaderStyle = Enum('LogHeaderStyle', 'NONE MAIN_HEADER SUB_HEADER')

"""
    Logger styles
"""
TIME_INDENT = ""
TEXT_INDENT = "  >>  "

#-----------------------------------------------------------------------------------------

"""
    The name of the main log directory
    where all logs are stored.
"""
LOG_MAIN_DIR_NAME = "log"

"""
    Path to the main log directory
"""
LOG_MAIN_DIR_PATH = ".."

"""
    The full path to current log directory
"""
LOG_CURRENT_DIR_PATH = ""

"""
    Path to the sub dir inside LOG_MAIN_DIR_NAME directory
"""
LOG_SUB_DIR_NAME = ""

"""
    Adds a prefix to the current test log folder name
"""
LOG_DIR_PREFIX_NAME = ""

#-----------------------------------------------------------------------------------------

"""
    The format of the time to be joined in
    the current dir name
"""
TIME_FORMAT_DIR_NAME = '%Y-%m-%d_%H;%M;%S'

"""
    The time format to be appended
    to each log
"""
TIME_FORMAT_SHORT_LOGGER = '%H:%M:%S'

"""
    The time format to be appended
    to the beggining of each log file
"""
TIME_FORMAT_LONG_LOGGER = '%H:%M:%S %d-%m-%Y'


"""
    Creates an log directory.
"""
def init_log_dir():
    # Don't make logs if no test is running
    if global_v.TEST_TYPE != global_v.TestType.NONE:
        global LOG_DIR_PREFIX_NAME
        global LOG_CURRENT_DIR_PATH

        # Prepare global filename for further references
        global_v.DIR_NAME = global_v.TEST_TYPE.name + "_" + LOG_DIR_PREFIX_NAME + "_" + get_time(TIME_FORMAT_DIR_NAME)

        # Join the path to current directory
        LOG_CURRENT_DIR_PATH = os.path.join(LOG_MAIN_DIR_PATH,
                                            LOG_MAIN_DIR_NAME,
                                            LOG_SUB_DIR_NAME,
                                            global_v.DIR_NAME)

        # Create directory to save information
        os.makedirs(LOG_CURRENT_DIR_PATH, exist_ok=True)


"""
    Creates a log in the console and file.

    You can add styles using the 'styles' list.
    Currently it is very ugly.
    TODO: separate styling from creating log message.

    - spaces refer to extra amount of spaces between logs
    - text_indent refer to the indent at the beggining of each line
"""
def log(msg, filename="",
            styles=[LogStyle.TIME_STAMP],
            spaces=0,
            text_indent=TEXT_INDENT):
    msg = str(msg)

    if filename:
        filepath = os.path.join(LOG_CURRENT_DIR_PATH, filename)

        # Check if file exists
        file_exists = os.path.exists(filepath)

        f = open(filepath, 'a')

        # If it was openned for the first time, print a log
        if not file_exists:
            f.write("File created: " + get_time(TIME_FORMAT_LONG_LOGGER) + "\n\n")

#-----------------------------------------------------------------------------------------
    # Default log file
    filepath_default = os.path.join(LOG_CURRENT_DIR_PATH, LOG_DEFAULT_FILE_NAME)
    # Check if file exists
    file_exists = os.path.exists(filepath_default)

    f_default = open(filepath_default, 'a')

    # If it was openned for the first time, print a log
    if not file_exists:
        f_default.write("File created: " + get_time(TIME_FORMAT_LONG_LOGGER) + "\n\n")

#-----------------------------------------------------------------------------------------

    msg_to_log = ""

    msg_to_log += "\n" * spaces

    # Add style
    if LogStyle.SEPARATOR_START in styles:
        msg_to_log += __get_separator()

    # Print the time of log
    if LogStyle.TIME_STAMP in styles:
        msg_to_log += "".join([TIME_INDENT, "[", get_time(), "]:", "\n"]);

    # Insert indent before each line
    msg_list = msg.split("\n")
    for m in msg_list:
        msg_to_log += "".join([text_indent, m, "\n"]);

    # Add style
    if LogStyle.SEPARATOR_END in styles:
        msg_to_log += __get_separator()

    #msg_to_log += "\n"

    # Log
    if LogStyle.FILE_ONLY not in styles:
        print()
        print(msg_to_log)

    if filename:
        f.write(msg_to_log)
    f_default.write(msg_to_log)

    # Flush buffer
    sys.stdout.flush()

    # Clean up
    if filename:
        f.close()
    f_default.close()

"""
    Prints header, console and file
"""
def log_header(text, filename="",
                styles=[LogHeaderStyle.MAIN_HEADER]):

    if filename:
        filepath = os.path.join(LOG_CURRENT_DIR_PATH, filename)

        # Check if file exists
        file_exists = os.path.exists(filepath)

        f = open(filepath, 'a')

        # If it was openned for the first time, print a log
        if not file_exists:
            f.write("File created: " + get_time(TIME_FORMAT_LONG_LOGGER) + "\n\n")

#-----------------------------------------------------------------------------------------
    # Default log file
    filepath_default = os.path.join(LOG_CURRENT_DIR_PATH, LOG_DEFAULT_FILE_NAME)
    # Check if file exists
    file_exists = os.path.exists(filepath_default)

    f_default = open(filepath_default, 'a')

    # If it was openned for the first time, print a log
    if not file_exists:
        f_default.write("File created: " + get_time(TIME_FORMAT_LONG_LOGGER) + "\n\n")

#-----------------------------------------------------------------------------------------

    # Get the dimensions of the console
    #rows, columns = os.popen('stty size', 'r').read().split()
    columns, rows = shutil.get_terminal_size((80,20))

    row_count = int(rows)
    column_count = int(columns)

    time = get_time()

    # Dividing odd integer by 2 might cause of information
    # i.e. int(len(text) / 2)
    # Thus the need of fixing the end position of the header
    # Brace yourself. Magic Numbers are comming.
    if int(len(text)) % 2 == 0:
        text_beggining_indent = 2
        text_ending_indent = 5
    else:
        text_beggining_indent = 1
        text_ending_indent = 4

    if int(len(time)) % 2 == 0:
        time_ending_indent = 3
    else:
        time_ending_indent = 4

    text_ending_indent -= column_count%2 - 1
    time_ending_indent -= column_count%2 - 1

    # Length of header border, not counting the two left and right corners
    border_length = (column_count - 2)
    # Position of text
    text_pos = int(((column_count - 2) / 2)) - int(len(text) / 2) + text_beggining_indent
    # Position of time stamp
    time_pos = int(((column_count - 2) / 2)) - int(len(time) / 2)

    # Print the header
    msg_to_print = ""

    msg_to_print += "\n"
    msg_to_print += __get_separator()

    if LogHeaderStyle.MAIN_HEADER in styles:
        msg_to_print += __get_separator(filler=" ")

    msg_to_print += "".join(["#",
                " " * time_pos,
                "[" + time + "]",
                " " * (column_count - border_length + time_pos - time_ending_indent),
                "#",
                "\n"])

    if LogHeaderStyle.MAIN_HEADER in styles:
        msg_to_print += __get_separator(filler=" ")

    msg_to_print += "".join(["#",
                    " " * text_pos + text,
                    " " * (column_count - border_length + text_pos - text_ending_indent),
                    "#",
                    "\n"])

    if LogHeaderStyle.MAIN_HEADER in styles:
        msg_to_print += __get_separator(filler=" ")

    msg_to_print += __get_separator()
    msg_to_print += "\n"

    print(msg_to_print)
    if filename:
        f.write(msg_to_print)
    f_default.write(msg_to_print)

    # Flush buffer
    sys.stdout.flush()

    # Clean up
    if filename:
        f.close()
    f_default.close()

"""
    Returns a nice, stylish log separator as string
"""
def __get_separator(corner="#", filler="-"):
    columns, rows = shutil.get_terminal_size((80,20))
    #rows, columns = os.popen('stty size', 'r').read().split()
    column_count = int(columns)
    border_length = (column_count - 2)

    msg_to_print = corner + filler * border_length + corner + "\n"

    return msg_to_print

"""
    Returns current time as string.

    @format
        The format of the date to be printed
"""
def get_time(format=TIME_FORMAT_SHORT_LOGGER):
    return datetime.datetime.now().strftime(format)

"""
    Print current global configuration
"""
def log_config():
    # Get all items from global_variables
    items = dir(global_v)

    value_pos = 1

    # Find the variable name with logest name
    # Make that length the position of printing values
    for item in items:
        if not item.startswith("__"):
            if len(item) > value_pos:
                value_pos = len(item)

    # Add 5 more units for cosmetics
    value_pos += 5

    config_str = ""
    for item in items:
        if not item.startswith("__"):
            config_str += item
            config_str += " " + "." * (value_pos - len(item)) + " "
            config_str += str(getattr(global_v, item))
            config_str += "\n"

    log_header("Config", LOG_CONFIG_FILE_NAME)
    log(config_str, LOG_CONFIG_FILE_NAME)
