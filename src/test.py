import bioumlsim

sim = bioumlsim.BioUMLSim('C:/BioUML_2023.1')
model3 = sim.load("C:/Users/Damag/BioUML_Scripts/models_selected/BIOMD0000000003.xml")
model4 = sim.load("C:/Users/Damag/BioUML_Scripts/models_selected/BIOMD0000000010.xml")
result3 = model3.simulate(100, 10)
result4 = model4.simulate(100, 10)
print(result3.getValues('C'))
print(result4.getValues('MKK'))