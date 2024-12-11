from Chemistry.Atom import Atom
from Systems.AbstractSystem import System


class AtomicSystem(System[Atom]):
    @property
    def atoms(self) -> list[Atom]:
        return self.components

    def __init__(
        self,
        atoms: list[Atom],
    ):
        super().__init__(components=atoms)

    def __repr__(self) -> str:
        return f"Frame with {len(self.atoms)} atoms"
