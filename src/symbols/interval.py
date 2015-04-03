""" 
    Simple structure which encapsulates interval info i.e 
    lowe and upper bound.
"""
class Interval:
    def __init__(self, lowerBound, upperBound):
        self.lowerBound = lowerBound
        self.upperBound = upperBound