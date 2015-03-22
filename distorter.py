from numpy import random, sqrt, log, sin, cos, pi

class Distorter:
    def __init__(self):
        pass
    def boxMuller(self, uniform1, uniform2):
        z1 = sqrt(-2*log(uniform1))*cos(2*pi*uniform2)
        z2 = sqrt(-2*log(uniform1))*sin(2*pi*uniform2)
        return z1,z2
    def generateDistortion(self, cloudCenterCoordinates):
        distortedCenter = []
        rangeS = len(cloudCenterCoordinates);
        for i in range(0, rangeS):
            if(range % 2 == 0):
                print("hello")
            distortion = random.normal(0, 0.2, 1)
            distortedCenter.append(cloudCenterCoordinates[i]+distortion) 
        return distortedCenter