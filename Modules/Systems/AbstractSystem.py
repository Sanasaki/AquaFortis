from abc import ABC
from typing import Self

from Classes.Vector import Vector


class Component(ABC):
    """
    An object inheriting from Component is allowed to be part of a System[Component] class. The object must have a label property in order to be packed with different components for accounting.
    """

    __slots__ = "label"

    def __init__(self, label: str = "") -> None:
        self.label: str = label


class System[component: Vector](Vector):
    """
    tl;dr System is Vector space, and is itself a Vector.\n
    Otherwise, be ready for an overglorified list. System class is made to group components sharing a common representation (their label attribute).
    For instance, a System of Molecule shares the same formula, a System of Atom share the same symbol, etc.
    Builtin support is provided for interace with dictionary.
    """

    __slots__ = "components"

    def __init__(
        self,
        components: list[component] = None,
        x: float = 0.0,
        y: float = 0.0,
        z: float = 0.0,
        label: str = "",
    ) -> None:
        if components is None:
            self.components: list[component] = []
        else:
            self.components: list[component] = components

    def __iter__(self) -> "SystemIteratorHelper[component]":
        return SystemIteratorHelper(self)

    def __repr__(self) -> str:
        return f"{self.components}"

    @property
    def asDict(self) -> dict[str, int]:
        """
        Returns a dictionary with the label of the components as keys and the number of components as values.
        """
        componentsDict: dict[str, int] = {}
        for component in self:
            componentsDict[component.label] = componentsDict.get(component.label, 0) + 1
        return componentsDict

    def setCenterOfMass(self) -> None:
        self.x = sum([vector.x for vector in self.components]) / len(self.components)
        self.y = sum([vector.y for vector in self.components]) / len(self.components)
        self.z = sum([vector.z for vector in self.components]) / len(self.components)
        # return Vector(x, y, z)


class SystemIteratorHelper[component: Vector]:
    def __init__(self, system: System[component]):
        self.components = system.components
        self.index = 0

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> component:
        self.index += 1
        try:
            return self.components[self.index - 1]
        except IndexError:
            self.index = 0
            raise StopIteration
