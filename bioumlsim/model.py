from numpy import array as nparray
from pandas import DataFrame
from pandas import Index

class Model:
    
    def __init__(self, engine, model):
        self.engine = engine
        self.model = model
    
    def log(self, message, verbose=True):
        if verbose:
            print(message)  
        
    def simulate(self, tend, numpoints, verbose = False):
        """
        Simulates SBML model and returns results.
        Args:
            tend: final time for simulation
            numpoints: number of time points
        Returns:
            simulation results
        """
        self.log(f"Simulating model: {self.engine.getDiagram().getName()}", verbose)
        self.engine.setCompletionTime(tend)
        self.engine.setTimeIncrement(tend / numpoints)
        result = self.engine.simulateSimple(self.model)
        species = self.engine.getFloatingSpecies()
        values = nparray(result.getValuesTransposed(species))
        names = nparray(species)
        times = nparray(result.getTimes());
        return DataFrame(values, columns = names, index = Index(times, name ='Time'))