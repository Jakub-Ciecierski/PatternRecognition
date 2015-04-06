from data_calculations.matrices_batch import MatricesBatch

class ResultsData:
    def __init__(self, radiuses):
        self.__radiusesData = self.__produce_matrices_batches(radiuses)
        
    def __produce_matrices_batches(self, radiuses):
        result = []
        for radius in radiuses:
            matrices_batch = MatricesBatch(radius)
            result.append(matrices_batch)
        return result
    
    def batch(self, radius):
        return self.__radiusesData[radius]