from abc import ABC, abstractmethod
from typing import Optional

from memory_fs.exceptions import FileSystemError
from memory_fs.memory_space import MemorySpace


class FileSystemObject(ABC):
    @abstractmethod
    def remove(self, recursive: bool=False):
        pass

    @abstractmethod
    def get_contents(self):
        pass

    def get_path(self) -> str:
        if not self.parent:
            return ''
        return f"{self.parent.get_path()}/{self.name}"
    
    def find(self, name: str) -> list[str]:
        return []


class File(FileSystemObject):
    def __init__(self, name: str, parent: "Directory", memory_space: "MemorySpace"):
        self.name = name
        self.parent = parent
        self.memory_space = memory_space
        self.address = memory_space.reserve()
    
    def get_contents(self) -> str:
        return self.memory_space.get(self.address)
    
    def remove(self, recursive: bool=False):
        self.memory_space.remove(self.address)
        self.parent.remove_child(self.name)
    
    def write(self, contents: str):
        self.memory_space.write(self.address, contents)


class Directory(FileSystemObject):
    def __init__(self, name: str, parent: Optional["Directory"]):
        self.contents: dict[str, FileSystemObject] = {}
        self.name = name
        self.parent = parent
    
    def get_object(self, path_list: list[str]):
        if not path_list:
            return self
        try:
            if path_list[0] == '.':
                working_object = self
            elif path_list[0] == '..':
                working_object = self.parent
            else:
                working_object = self.contents[path_list[0]]
            return working_object.get_object(path_list[1:])
        except KeyError:
            raise FileSystemError(f"No such directory {path_list[0]}.")

    def get_contents(self) -> list[str]:
        return list(self.contents.keys())
    
    def make_directory(self, name):
        if name in self.contents:
            raise FileSystemError(f"Can't create directory {name}. It already exists.")
        self.contents[name] = Directory(name=name, parent=self)

    def find(self, name: str) -> list[str]:
        found_paths = []
        if name in self.contents:
            found_paths.append(self.contents[name].get_path())
        
        for fs_obj in self.contents.values():
            found_paths.extend(fs_obj.find(name))
        return found_paths
    
    def remove(self, recursive=False):
        if not recursive:
            raise FileSystemError(f"Attemping to remove a directory. Set recursive=True to remove all contents of this directory.")
        
        for fs_obj in self.contents.values():
            fs_obj.remove(recursive)
        self.parent.remove_child(self.name)
    
    def remove_child(self, name: str):
        """Should only used by the child to remove its own reference.

        Args:
            name: Name of the child object. Should correspond to the key in the self.contents dict.

        Raises:
            FileSystemError: If the name doesn't exist in the self.contents dict.
        """
        try:
            del self.contents[name]
        except KeyError:
            raise FileSystemError(f"Attempting to remove content that doesn't exist: {name}")