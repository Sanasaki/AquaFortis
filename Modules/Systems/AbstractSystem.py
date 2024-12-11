from abc import ABC
from typing import Self


class Component(ABC):
    """
    An object inheriting from Component is allowed to be part of a System[Component] class. The object must have a label property in order to be packed with different components for accounting.
    """

    def __init__(self, label: str) -> None:
        self.label: str = ""

    # @property
    # @abstractmethod
    # def label(self) -> str: ...

    # def __hash__(self) -> int:
    #     return hash(self.label)

    # def __eq__(self: Self, other: Any) -> bool:
    #     if not isinstance(other, self.__class__):
    #         return False
    #     return self.label == other.label


class System[component: Component](ABC):
    """
    Be ready for an overglorified list. System class is made to group components sharing a common representation (their label attribute).
    For instance, a System of Molecule shares the same formula, a System of Atom share the same symbol, etc.
    """

    __slots__ = "components"

    def __init__(self, components: list[component] = None) -> None:
        if components is None:
            self.components: list[component] = []
        else:
            self.components: list[component] = components

    def __iter__(self) -> "SystemIteratorHelper[component]":
        return SystemIteratorHelper(self)

    def __repr__(self) -> str:
        return f"{self.components}"

    def toDict(self) -> dict[str, int]:
        """
        Returns a dictionary with the label of the components as keys and the number of components as values.
        """
        componentsDict: dict[str, int] = {}
        for component in self.components:
            componentsDict[component.label] = componentsDict.get(component.label, 0) + 1
        return componentsDict


class SystemIteratorHelper[component: Component]:
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
