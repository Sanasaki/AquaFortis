from typing import Iterable

from Classes.Vector import Vector
from Functions.FxStaticFunctions import FxProcessTime


class Atom(Vector):
    __slots__ = ("chemSymbol", "atomicNumber", "atomicWeight", "x", "y", "z")

    def __init__(self, 
                chemSymbol: str,
                atomicNumber: int=None, 
                atomicWeight: float=None, 
                x: float=None,
                y: float=None,
                z: float=None,
                ):
        self.chemSymbol:    str     = chemSymbol
        self.atomicNumber:  int     = atomicNumber
        self.atomicWeight:  float   = atomicWeight
        super().__init__(x, y, z)
    
    def __repr__(self):
        return f"{self.chemSymbol}"
    
    def __hash__(self):
        return hash(self.chemSymbol) + hash(self.x) + hash(self.y) + hash(self.z)
    
    def __lt__(self, other):
        return self.chemSymbol < other.chemSymbol

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    
    @classmethod
    def fromStr(cls, atomLine:str) -> "Atom":
        chemSymbol, x, y, z = atomLine.split()
        return cls(chemSymbol, x=float(x), y=float(y), z=float(z))
    
    @classmethod
    def fromIterable(cls, atomlist: Iterable[str]) -> list["Atom"]:
        return [cls.fromStr(atomLine) for atomLine in atomlist]