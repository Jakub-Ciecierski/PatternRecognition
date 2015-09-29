import shutil
import math
import sys
import datetime
import time
import os
import util.global_variables as global_v
import util.logger as logger

"""
    Time when progress bar was initiated
"""
init_time = 0

"""
    Size of the problem for progress bar
"""
problem_size = 0

current_size = 0

"""
    Current progress percent as calculated
    from current size and problem size
"""
current_progress_percent = 0

"""
    Current 'bar' status in the progress bar.
    Calculated from current_progress_percent
    and rounded up to the nearest 10
"""
current_progress_bar = 0

"""
    How many bars to display in progress bar
"""
bar_count = 0

"""
    The header to be displayed
"""
header = ""

###########################################################
#                       CONFIG                            #
###########################################################

SHOW_PROGRESS_BAR = True

MAX_BAR_COUNT = 35

BAR_SYMBOL = "#"
SPACE_SYMBOL = " "

"""
    Uses to initiate the progress bar
"""
def init(_problem_size, _header=""):
    global problem_size
    problem_size = _problem_size

    global current_size
    current_size = 0

    global init_time
    init_time = time.time()

    global header
    header = _header
    
    # Get the dimensions of the console
    columns, rows = shutil.get_terminal_size((80,20))
    column_count = int(columns)

    # Make sure that the progress bar is not leaning to new line
    global MAX_BAR_COUNT
    if column_count < MAX_BAR_COUNT - 10:
        MAX_BAR_COUNT = column_count - 10

    logger.log("PROGRESS BAR INIT: " + str([header]),
                styles=[logger.LogStyle.SEPARATOR_START],
                spaces=3)

"""
    Should be called every iteration of your algorithm
    to notify progress
"""
def update(update_size=1):
    global current_size
    current_size += update_size

    global current_progress_percent
    current_progress_percent = (current_size / problem_size) * 100

    global current_progress_bar
    current_progress_bar = int(math.ceil(current_progress_percent / (100 / MAX_BAR_COUNT)))

    bars = BAR_SYMBOL * current_progress_bar
    space = SPACE_SYMBOL * (MAX_BAR_COUNT - current_progress_bar)

    if SHOW_PROGRESS_BAR:
        sys.stdout.write("\r[{0}] {1:.2f}%".format(bars + space,
                            current_progress_percent))
        sys.stdout.flush()

"""
    Should be called after your algorithm is done
"""
def finish():
    delta_time = time.time() - init_time

    msg = str([header]) + "\n" + "Finished after: {0:.3f} sec".format(delta_time)

    print()
    logger.log("PROGRESS BAR FINISH: " + msg,
            styles=[logger.LogStyle.SEPARATOR_END])
