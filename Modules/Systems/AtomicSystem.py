from Chemistry.Atom import Atom
from Systems.AbstractSystem import System


class AtomicSystem(System[Atom]):
    # __slots__ = "atoms"

    def __init__(
        self,
        atoms: list[Atom],
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        label: str = "",
    ):
        super().__init__(components=atoms)
        self.atoms = self.components

    def __repr__(self) -> str:
        return f"Frame with {len(self.atoms)} atoms"
