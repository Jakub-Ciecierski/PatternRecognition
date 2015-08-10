import sys
import util.global_variables as global_v
import os
import datetime

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
    Logger styles
"""
TIME_INDENT ="  "
TEXT_INDENT = "     "

"""
    Creates an log directory.
"""
def init_log_dir():
    # Don't make logs if no test is running
    if global_v.TEST_TYPE != global_v.TestType.NONE:

        # Prepare global filename for further references
        global_v.DIR_NAME = global_v.TEST_TYPE.name + "_" + get_time(TIME_FORMAT_DIR_NAME)

        # Join the path to current directory
        global LOG_CURRENT_DIR_PATH
        LOG_CURRENT_DIR_PATH = os.path.join(LOG_MAIN_DIR_PATH,
                                            LOG_MAIN_DIR_NAME,
                                            global_v.DIR_NAME)

        # Create directory to save information
        os.makedirs(LOG_CURRENT_DIR_PATH, exist_ok=True)


"""
    Creates a log in the console and file
"""
def log(msg, filename="log.txt"):
    filepath = os.path.join(LOG_CURRENT_DIR_PATH, filename)

    # Check if file exists
    file_exists = os.path.exists(filepath)

    f = open(filepath, 'a')

    # If it was openned for the first time, print a log
    if not file_exists:
        f.write("File created: " + get_time(TIME_FORMAT_LONG_LOGGER) + "\n\n")

    # Print the time of log
    msg_to_log = "".join([TIME_INDENT, "[", get_time(), "]:", "\n"]);

    # Insert indent before each line
    msg_list = msg.split("\n")
    for m in msg_list:
        msg_to_log += "".join([TEXT_INDENT, m, "\n"]);
    msg_to_log += "\n\n"

    # Log
    print(msg_to_log)
    f.write(msg_to_log)

    # Flush buffer
    sys.stdout.flush()

    # Clean up
    f.close()

"""
    Legacy function, print header
"""
def log_header(text):
    # Get the dimensions of the console
    rows, columns = os.popen('stty size', 'r').read().split()

    row_count = int(rows)
    column_count = int(columns)

    time = get_time()

    # Dividing odd integer by 2 might cause of information
    # i.e. int(len(text) / 2)
    # Thus the need of fixing the end position of the header
    # Brace yourself. Magic Numbers are comming.
    if int(len(text)) % 2 == 0:
        text_beggining_indent = 1
        text_ending_indent = 3
    else:
        text_beggining_indent = 0
        text_ending_indent = 2

    if int(len(time)) % 2 == 0:
        time_ending_indent = 3
    else:
        time_ending_indent = 4

    # Length of header border, not counting the two left and right corners
    border_length = (column_count - 2)
    # Position of text
    text_pos = int(((column_count - 2) / 2)) - int(len(text) / 2) + text_beggining_indent
    # Position of time stamp
    time_pos = int(((column_count - 2) / 2)) - int(len(time) / 2)

    # Print the header
    print()
    print("#" + "-" * border_length + "#")
    print(  "#"
            + " " * time_pos
            + "[" + time + "]"
            + " " * (column_count - border_length + time_pos - time_ending_indent)
            + "#")

    print(  "#"
            + " " * text_pos + text
            + " " * (column_count - border_length + text_pos - text_ending_indent)
            + "#")

    print("#" + " " * border_length + "#")
    print("#" + "-" * border_length + "#")
    print()

"""
    Returns current time as string.

    @format
        The format of the date to be printed
"""
def get_time(format=TIME_FORMAT_SHORT_LOGGER):
    return datetime.datetime.now().strftime(format)

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

    log_header("Config")
    log(config_str, "config.txt")
