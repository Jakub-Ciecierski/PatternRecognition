import random

# Generated random number from given interval from
# uniform distribution
class RandomGenerator:

    def generateRandom(self, lowerBound, upperBound):
        return random.uniform(lowerBound, upperBound)