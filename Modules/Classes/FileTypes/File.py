from __future__ import annotations

from abc import ABC


class File(ABC):
    __slots__ = [
        "filePath",
        "currentDirPath",
        "name",
        "fileName",
        "fileType",
        "fileLength",
    ]

    def __init__(self, filePath: str, fileType: str = None) -> None:
        self.filePath: str = filePath
        self.currentDirPath: str = "/".join(filePath.split("/")[:-1]) + "/"
        self.name: str = filePath.split("/")[-1].split(".")[0]
        self.fileName: str = filePath.split("/")[-1]
        self.fileType: str = (
            self.fileName.split(".")[-1] if fileType is None else fileType
        )
        self.fileLength: int = self._getFileLength()

    def __repr__(self) -> str:
        return self.filePath

    def _getFileLength(self):
        with open(self.filePath, "rb") as f:
            return sum(1 for line in f)


# class Vector(ABC):
#     def __init__(self, **kwargs) -> None:
#         for key, value in kwargs.items():
#             setattr(self, key, float(value))
#         self.dimension = len(kwargs)

#     def __hash__(self) -> int:
#         return hash(self.dimension)

#     def __eq__(self, other):
#         return self.dimension == other.dimension

# class Component(ABC):

#     @property
#     def parent(self) -> Component:
#         return self._parent

#     @parent.setter
#     def parent(self, parent: Component) -> None:
#         self._parent = parent

#     @abstractmethod
#     def isComposite(self) -> bool:
#         pass

# class Set(ABC):
#     def __init__(self, count:float) -> None:
#         self.count = count

#     @abstractmethod
#     def merge(self, other) -> None:
#         pass

# class EquivalentSet(Set):
#     def __init__(self) -> None:
#         super().__init__()

#     def merge(self, other) -> None:
#         self.count += other.count


# class NonEquivalentSet(Set):
#     def __init__(self, setList:list) -> None:
#         self.setList = setList
#         self.count = len(setList)

#     def __hash__(self) -> int:
#         return hash(tuple(self.setList))

#     def __eq__(self, other) -> bool:
#         return self == other

#     def merge(self, other) -> None:
#         self.setList += other.setList
#         self.count += other.count
