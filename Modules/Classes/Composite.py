from abc import ABC


class Composite(ABC):
    canHaveChildren = True

    def __init__(self):
        self._parent: "Composite" = None
        # if self.canHaveChildren:
        self._children: list["Composite"] = []

    @property
    def parent(self) -> "Composite":
        return self._parent

    @parent.setter
    def parent(self, newParent: "Composite") -> None:
        self._parent = newParent

    def attach(self, component: "Composite") -> None:
        self._children.append(component)
        component.parent = self

    def detach(self, component: "Composite") -> None:
        del component.parent
