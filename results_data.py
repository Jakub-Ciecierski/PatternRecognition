from matrices_batch import MatricesBatch
class ResultsData:
    def __init__(self, number_of_radiuses):
        self.__radiusesData = self.__produce_matrices_batches(number_of_radiuses)
        
    def __produce_matrices_batches(self, number_of_radiuses):
        result = []
        for i in range(0, number_of_radiuses):
            matrices_batch = MatricesBatch()
            result.append(matrices_batch)
        return result
    
    def batch(self, radius):
        return self.__radiusesData[radius]