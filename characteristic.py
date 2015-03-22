import random
from interval import Interval

class Characteristic:
    def __init__(self):
        self.interval = self.randomizeInterval(0,20)

    def randomizeInterval(self, lowerBound, upperBound):
        a = random.uniform(lowerBound,upperBound)
        b = random.uniform(lowerBound,upperBound)

        if(a < b):
            return Interval(a,b)
        else:
            return Interval(b,a)

