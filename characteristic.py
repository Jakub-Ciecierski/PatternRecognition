import random
from interval import Interval
import util.global_variables as global_v

class Characteristic:
    def __init__(self):
        self.interval = self.randomizeInterval(global_v.CHAR_INTERVAL[0],global_v.CHAR_INTERVAL[1])

    def randomizeInterval(self, lowerBound, upperBound):
        a = random.uniform(lowerBound,upperBound)
        b = random.uniform(lowerBound,upperBound)

        if(a < b):
            return Interval(a,b)
        else:
            return Interval(b,a)

