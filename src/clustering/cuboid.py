class Cuboid:
    def __init__(self,points):
        self.__dimensions = self.__calculate_dimensions(points)
        
    def __calculate_dimensions(self, points):
        print("original")
        print(points)
        for i in range(0,len(points[0])):
            gathered = []
            for characteristics in points:
                gathered.append(characteristics[i])
            print("gathered")
            print(gathered)
        