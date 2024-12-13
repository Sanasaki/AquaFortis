from typing import Any

from Classes.Vector import Vector


class Atom(Vector):
    __slots__ = ()

    # @property
    # def chemSymbol(self) -> str:
    #     return self.label

    def __init__(
        self,
        # atomicNumber: int=None,
        # atomicWeight: float=None,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        chemSymbol: str = "",
    ):
        super().__init__(x, y, z, label=chemSymbol)
        # self.label: str = chemSymbol
        # self.label = self.label
        # self.atomicNumber:  int     = atomicNumber
        # self.atomicWeight:  float   = atomicWeight

    def __repr__(self):
        return f"{self.label}"

    def __hash__(self):
        return hash(self.label) + hash(self.x) + hash(self.y) + hash(self.z)

    def __lt__(self, other: "Atom"):
        return self.label < other.label

    def __eq__(self, other: Any) -> bool:
        return self.__hash__() == other.__hash__()

    @classmethod
    def fromStr(cls, atomLine: str) -> "Atom":
        chemSymbol, x, y, z = atomLine.split()
        return cls(chemSymbol=chemSymbol, x=float(x), y=float(y), z=float(z))
