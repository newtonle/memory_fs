from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from memory_fs.directory import Directory

class FileSystemObject(ABC):
    name: str
    parent: "Directory"

    @abstractmethod
    def remove(self, recursive: bool=False):
        pass

    @abstractmethod
    def find(self, name: str) -> list[str]:
        pass

    @abstractmethod
    def assert_directory(self):
        pass

    @abstractmethod
    def move(self, dst):
        pass

    def is_root(self) -> bool:
        return self == self.parent

    def get_path(self) -> str:
        if self.is_root():
            return ''
        return f"{self.parent.get_path()}/{self.name}"
    
    def set_parent(self, parent: "Directory"):
        self.parent = parent
