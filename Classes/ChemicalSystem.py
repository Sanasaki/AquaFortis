import chemistry.Molecule as Molecule

class ChemicalSystem:

    def phaseRecognition(self):
        foundPhases = {x.phase for x in self.molecules}
        return foundPhases
    
    def compoundsRecognition(self):
        foundCompounds = {x.chemicalFormula for x in self.molecules}
        return foundCompounds
        
    def __init__(self, autoRefresh: bool=True):
        self.autoRefresh = autoRefresh

    def addMolecules(self, newMolecules: Molecule):
        self.molecules.append(newMolecules)
        self.phases = self.phaseRecognition() if self.autoRefresh else self.phases
    

    def regroup(self):
        # Main matrix, {phase => {compound}}
        #Look through all phases
        matrix = {}
        # Dictionary of compounds presence (regardless of multiple phase appearance)
        compounds = self.compoundsRecognition()
        for phase in self.phases:
            # Submatrix, {compound => [count]}
            subMatrix = {}
            for compound in compounds:
                subMatrix[compound] = []
            matrix[phase] = subMatrix

        for m in self.molecules:
            (matrix[m.phase])[m.chemicalFormula].append(m.count)
        
        newMolecules = []
        for phase in matrix.keys():
            for compound in (matrix[phase]).keys():
                count = sum((matrix[phase])[compound])
                (matrix[phase])[compound] = count
                newMolecules.append(Molecule(chemicalFormula=compound, atomicComposition=None, phase=phase, count=count))
        
        return newMolecules
    
    # def __init__(self, *molecules):
    #     self.molecules = [x for x in molecules if isinstance(x, Molecule)]
    #     self.phases = self.phaseRecognition()
    #     self.molecules = self.regroup()
    
    # def __hash__(self):
    #     return hash((self.molecule, self.phase))
    
    # def __eq__(self, other):
    #     return (
    #         isinstance(other, EquivalentMolecules) and
    #         self.molecule.chemicalFormula == other.molecule.chemicalFormula and
    #         self.phase == other.phase
    #     )
    
    # def add(self, addedQuantity: float):
    #     self.count += addedQuantity

    def __repr__(self):
        return f"{self.molecules}"