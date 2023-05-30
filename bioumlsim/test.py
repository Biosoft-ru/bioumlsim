import bioumlsim

sim = bioumlsim.BioUMLSim()
model = sim.load("C:/Users/Damag/BioUML_Scripts/models_selected/BIOMD0000000003.xml")
result = model.simulate(100, 10)

result.to_csv("C:/Users/Damag/result2.txt")
print(result)
print()
print(result.head())
print()
print(result.values)
print()
print(result['X'])
