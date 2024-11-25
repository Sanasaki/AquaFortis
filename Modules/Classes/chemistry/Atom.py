

# from chemistry.Molecule import Molecule

periodicTable: dict = {
    "H" :   {"atomicWeight": 1.0080,    "atomicNumber": 1 },
    "He":   {"atomicWeight": 4.00260,   "atomicNumber": 2 },
    "Li":   {"atomicWeight": 7.0,       "atomicNumber": 3 },
    "Be":   {"atomicWeight": 9.012183,  "atomicNumber": 4 },
    "B" :   {"atomicWeight": 10.81,     "atomicNumber": 5 },
    "C" :   {"atomicWeight": 12.011,    "atomicNumber": 6 },
    "N" :   {"atomicWeight": 14.007,    "atomicNumber": 7 },
    "O" :   {"atomicWeight": 15.999,    "atomicNumber": 8 }
}

# @dataclass(frozen= True, order=True, slots=True)
class Atom():
    # symbol:             str     = field(compare=True)
    # __slots__ = ['symbol', 'atomicNumber', 'atomicWeight', 'coordinates']
    # __atomicNumber:     int     = field(default=(periodicTable[symbol])[atomicNumber], repr=False)
    # __atomicWeight:     float   = field(default=periodicTable[symbol].atomicWeight, compare=False, repr=False)
    # coordinates:        float  = field(default_factory= list, hash=True, compare=False, repr=False)


    def __init__(self, 
                chemSymbol: str,
                atomicNumber: int=None, 
                atomicWeight: float=None, 
                coordinates: list=None,
                x: float=None,
                y: float=None,
                z: float=None,
                # molecule=None,
                ):
        self.chemSymbol:    str     = chemSymbol
        self.atomicNumber:  int     = atomicNumber
        self.atomicWeight:  float   = atomicWeight
        self.x:   float = x
        self.y:   float = y
        self.z:   float = z
        # self._molecule: Molecule    = molecule

    def __repr__(self):
        return f"{self.chemSymbol}"
    
    def __hash__(self):
        return hash(self.chemSymbol) + hash(self.x) + hash(self.y) + hash(self.z)
    
    def __lt__(self, other):
        return self.chemSymbol < other.chemSymbol

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    
    # m'y prends-je de la bonne manière pour définir des propriétés privées ? devraient-elles être privées ?même remarque pour self.atoms de la classe molécule
    # @property
    # def molecule(self):
    #     return self._molecule

    # @molecule.setter
    # def molecule(self, aaa):
    #     self._molecule = aaa 
    

    
# class MolecularDynamicFrame(Component, File):


#     # To begin with, a frame will be a leaf
#     # Later, it could be made a composition of atoms and their coordinates
#     def isComposite(self) -> bool:
#         return False



# class MolecularDynamicTrajectory(Component, File):
#     def __init__(self) -> None:
#         self._children: List[Component] = []

#     def add(self, component: Component) -> None:
#         self._children.append(component)
#         component.parent = self
    
#     def remove(self, component: Component) -> None:
#         self._children.remove(component)
#         component.parent = None
