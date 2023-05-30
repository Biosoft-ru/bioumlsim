import jpype
import jpype.imports
import numpy as np
import pandas as pd
import os

class BioUMLSim:
    
    bioUMLPath = None
    atol = 1E-8
    rtol = 1E-8
    engine = None

    def __init__(self):
        path = os.path.dirname(__file__)+'/jars'
        self.bioUMLPath = path
        print("JVM is starting up")
        jpype.startJVM(classpath=[path+'/*'], convertStrings=True)
        
    def load(self, file):
        """
        Loads SBML file and transforms it into object which represents mathematical model.
        Args:
            file (str): path to file
        Returns:
            model
        """
        print(f"SBML file is loading: {file}")
        diagram = jpype.JClass("biouml.plugins.sbml.SbmlModelFactory").readDiagram(file, False)
        self.engine = jpype.JClass("biouml.plugins.simulation.java.JavaSimulationEngine")()
        self.engine.setDiagram(diagram)
        self.engine.setClassPath(self.bioUMLPath +'/src.jar')
        self.engine.disableLog()
        self.engine.setAbsTolerance(self.atol)
        self.engine.setRelTolerance(self.rtol)
        return Model(self.engine, self.engine.createModel())
    
    def plot(self, df):
        import matplotlib.pyplot as plt
        plt.plot(df)
        plt.show()
    
    def loadTest(self):
        path = os.path.dirname(__file__)+'/test.xml'
        return self.load(path)
         
class Model:
    
    def __init__(self, engine, model):
        self.engine = engine
        self.model = model
        
    def simulate(self, tend, numpoints):
        """
        Simulates SBML model and returns results.
        Args:
            tend: final time for simulation
            numpoints: number of time points
        Returns:
            simulation results
        """
        print(f"Simulating model: {self.engine.getDiagram().getName()}")
        self.engine.setCompletionTime(tend)
        self.engine.setTimeIncrement(tend / numpoints)
        result = self.engine.simulateSimple(self.model)
        species = self.engine.getFloatingSpecies()
        values = np.array(result.getValuesTransposed(species))
        names = np.array(species)
        times = np.array(result.getTimes());
        return pd.DataFrame(values, columns = names, index = pd.Index(times, name ="Time"))