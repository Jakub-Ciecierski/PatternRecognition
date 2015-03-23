from numpy import random, sqrt, log, sin, cos, pi
import random


class Distorter:
    def __init__(self):
        pass

    def generateDistortion(self, cloudCenterCoordinates,sigmaSqrt):
        distortedCenter = []
        for i in range(len(cloudCenterCoordinates)):
            distortedCenter.append(cloudCenterCoordinates[i]+ random.gauss(0, sigmaSqrt))
#         print(distortedCenter)
        return distortedCenter