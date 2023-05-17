import jpype
import jpype.imports

class BioUMLSim:
    
    bioUMLPath = None
    atol = 1E-8
    rtol = 1E-8
    engine = None
    
    def __init__(self, path = 'C:/BioUML_2023.1'):
        """
        Code copied from runJVM method
        """
        self.bioUMLPath = path
        print("JVM is starting up")
        jpype.startJVM(classpath=[self.bioUMLPath+'/plugins/*',self.bioUMLPath+'/plugins/cern.jet.random_1.3.0/colt.jar'])
 
    def runJVM(path):
        """
        Starts up Java Virtual Machine and adds all BioUML jars to classpath 
        Args:
            path (str): path to BioUML installation
        """
        self.bioUMLPath = path
        print("JVM is starting up")
        jpype.startJVM(classpath=[self.bioUMLPath+'/plugins/*',self.bioUMLPath+'/plugins/cern.jet.random_1.3.0/colt.jar'])
       
    def load(self, file):
        """
        Loads SBML file and transforms it into object which represents mathematical model.
        Args:
            file (str): path to file
        Returns:
            model
        """
        print(f"SBML file is loading: {file}.")
        diagram = jpype.JClass("biouml.plugins.sbml.SbmlModelFactory").readDiagram(file)
        self.engine = jpype.JClass("biouml.plugins.simulation.java.JavaSimulationEngine")()
        self.engine.setDiagram(diagram)
        self.engine.setClassPath(self.bioUMLPath +'/plugins/biouml.plugins.simulation/src.jar')
        self.engine.setOutputDir(self.bioUMLPath+'/temp')
        self.engine.disableLog()
        self.engine.setAbsTolerance(self.atol)
        self.engine.setRelTolerance(self.rtol)
        return Model(self.engine, self.engine.createModel())
    
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
        print(f"Simulating model: {self.engine.getDiagram().getName()}.")
        self.engine.setCompletionTime(tend)
        self.engine.setTimeIncrement(tend / numpoints)
        return self.engine.simulateSimple(self.model) 