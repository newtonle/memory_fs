from abc import ABC
from typing import Optional

from memory_fs.exceptions import FileSystemError
from memory_fs.memory_space import MemorySpace

class FileSystemObject(ABC):
    pass


class File(FileSystemObject):
    def __init__(self, name: str, parent: "Directory", contents: str, memory_space: "MemorySpace"):
        self.name = name
        self.parent = parent
        self.memory_space = memory_space
        self.address = memory_space.write_new(contents)
    
    def get_contents(self):
        return self.memory_space.get(self.address)


class Directory(FileSystemObject):
    def __init__(self, name: str, parent: Optional["Directory"]):
        self.contents: dict[str, FileSystemObject] = {'.': self, '..': parent}
        self.name = name
        self.parent = parent
    
    def get_directory(self, path_list: list[str]):
        if not path_list:
            return self
        try:
            return self.contents[path_list[0]].get_directory(path_list[1:])
        except KeyError:
            raise FileSystemError(f"No such directory {path_list[0]}.")
    
    def get_path(self) -> str:
        if not self.parent:
            return ''
        return f"{self.parent.get_path()}/{self.name}"

    def get_contents(self) -> str:
        return list(set(self.contents.keys()) - {'..', '.'})
    
    def make_directory(self, name):
        if name in self.contents:
            raise FileSystemError(f"Can't create directory {name}. It already exists.")
        self.contents[name] = Directory(name=name, parent=self)