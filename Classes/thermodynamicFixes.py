class PhaseSpace:
    def __init__(self, constraints: str, firstStateVariable: float, secondStateVariable: float, thirdStateVariable: float):
        self.constraints = constraints
        self.firstStateVariable = firstStateVariable
        self.secondStateVariable = secondStateVariable
        self.thirdStateVariable = thirdStateVariable
    pass

class LammpsWriter:
    def __init__(self, atoms: str, groups: str):
        self.atoms = atoms
        self.groups = groups
    def equilibriate(self, ensemble: PhaseSpace):
        pass
    pass
class LammpsFix:
    def __init__(self, fixName: str, T: float, themoTimeStep: float, comment: str = None):
        if comment is None:
            comment = ""
        self.fixName = fixName
        self.temperature = T
        self.themoTimeStep = themoTimeStep
        self.comment = comment

    # def run(self, groups: str, fixTime: float):
    def _valueParser(self, **kwargs):
        for key, value in kwargs.items():
            if key == ("groups" or "atoms"):
                groups = value
            elif key == ("time" or "t" or "fixTime" or "ps"):
                fixTime = value
            elif key == ("T" or "Temperature" or "temperature"):
                initialTemperature = value
                finalTemperature = value
            elif key == ("T1" or "Temperature1" or "temperature1"):
                initialTemperature = value
            elif key == ("T2" or "Temperature2" or "temperature2"):
                finalTemperature = value
            elif key == ("P" or "p" or "Pressure" or "pressure"):
                initialPressure = value
                finalPressure = value
            elif key == ("P1" or "p1" or "Pressure1" or "pressure1"):
                initialPressure = value
            elif key == ("P2" or "p2" or "Pressure2" or "pressure2"):
                finalPressure = value
        return groups, fixTime, initialTemperature, finalTemperature, initialPressure, finalPressure
    
    def NVT(self, **kwargs):
        for key, value in kwargs.items():
            if key == ("groups" or "atoms"):
                groups = value
            elif key == ("time" or "t" or "fixTime" or "ps"):
                fixTime = value
            elif key == ("T" or "Temperature" or "temperature"):
                initialTemperature = value
                finalTemperature = value
            elif key == ("T1" or "Temperature1" or "temperature1"):
                initialTemperature = value
            elif key == ("T2" or "Temperature2" or "temperature2"):
                finalTemperature = value 
    
    def NPT(self, **kwargs):
        for key, value in kwargs.items():
            if key == ("groups" or "atoms"):
                groups = value
            elif key == ("time" or "t" or "fixTime" or "ps"):
                fixTime = value
            elif key == ("P" or "p" or "Pressure" or "pressure"):
                initialPressure = value
                finalPressure = value
            elif key == ("P1" or "p1" or "Pressure1" or "pressure1"):
                initialPressure = value
            elif key == ("P2" or "p2" or "Pressure2" or "pressure2"):
                finalPressure = value
            elif key == ("T" or "Temperature" or "temperature"):
                initialTemperature = value
                finalTemperature = value
            elif key == ("T1" or "Temperature1" or "temperature1"):
                initialTemperature = value
            elif key == ("T2" or "Temperature2" or "temperature2"):
                finalTemperature = value                          

        fixLine = f"\nfix {self.fixName} {groups} rigid/nvt/small molecule temp {self.fixTemperature} {self.fixTemperature} $({self.thermoTimeStep}*dt)"
        runLine = f"\nrun {1000*fixTime/self.dt}"
        unfixLine = f"\nunfix {self.fixName}"
        if self.comment == "":
            commentLine = f"\n# NVT fix"
        else:
            commentLine = f"\n# {self.comment}"

        return commentLine + fixLine + runLine + unfixLine
    
    def reach(self, finalState: StatisticalEnsemble, fixTime: float, ):
        
        return self

Initialisation = lammpsFix("NVT", 298, 0.5, "Test")

#Initialisation.NPT.equilibriate("all", 1bar, 298K, 100ps)
#Initialisation.NPT.transition("all", 1bar, 298K, 1bar, 350K, 100ps)
print(Initialisation.equilibriate("all", 100))
print("Taaaaa")



# Fix1 = LammpsFix.NPT
# Fix1