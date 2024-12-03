from typing import Iterable

from Classes.AtomicSystem import AtomicSystem
from Classes.Chemistry.Atom import Atom


class FactoryAtomicSystem():
    def __init__(self, inputChunk: Iterable[str], systemSize: float = None):
        return AtomicSystem(self._fromIterable(inputChunk), size=systemSize)

    def _fromStr(cls, atomLine:str) -> "Atom":
        chemSymbol, x, y, z = atomLine.split()
        return chemSymbol, float(x), float(y), float(z)
    
    def _fromIterable(self, atomlist: Iterable[str]) -> list[Atom]:
        return [self._fromStr(atomLine) for atomLine in atomlist]