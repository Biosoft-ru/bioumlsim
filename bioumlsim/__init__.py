import jpype
from os import path as ospath

from .jdkhandler import JDKHandler
from .model import Model

def installJDK():
    JDKHandler.installJDK()
        
class Bioumlsim:
    
    bioUMLPath = None
    atol = 1E-8
    rtol = 1E-8
    engine = None

    def log(self, message, verbose=True):
        if verbose:
            print(message)  
            
    def __init__(self, jdk = '', verbose = False):
        path = ospath.join(ospath.dirname(__file__), 'jars')
        self.log('Path to java classes: ' + path, verbose)
        self.bioUMLPath = path
        JDKHandler().startJVM(path, jdk=jdk, verbose=verbose)

    def load(self, file, verbose = False):
        """
        Loads SBML file and transforms it into object which represents mathematical model.
        Args:
            file (str): path to file
        Returns:
            model
        """
        self.log(f"SBML file is loading: {file}", verbose)
        diagram = jpype.JClass('biouml.plugins.sbml.SbmlModelFactory').readDiagram(file, False)
        self.engine = jpype.JClass('biouml.plugins.simulation.java.JavaSimulationEngine')()
        self.engine.setDiagram(diagram)
        self.engine.setClassPath(ospath.join(self.bioUMLPath,'src.jar'))
        if  not verbose:
            self.engine.disableLog()
        self.engine.setAbsTolerance(self.atol)
        self.engine.setRelTolerance(self.rtol)
        return Model(self.engine, self.engine.createModel())
    
    def plot(self, df):
        import matplotlib.pyplot as plt
        plt.plot(df)
        plt.show()
    
    def loadTest(self, verbose = False):
        path = ospath.join(ospath.dirname(__file__),'test.xml')
        return self.load(path, verbose=verbose)