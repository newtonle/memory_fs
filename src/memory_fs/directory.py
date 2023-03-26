from typing import Optional

from memory_fs.exceptions import FileSystemError
from memory_fs.fs_object import FileSystemObject


class Directory(FileSystemObject):
    def __init__(self, name: str, parent: Optional["Directory"]):
        self.contents: dict[str, FileSystemObject] = {}
        self.name = name
        self.parent = parent or self  # root object's parent is itself
    
    def get_object(self, path_list: list[str]) -> FileSystemObject:
        if not path_list:
            return self
        try:
            working_object: FileSystemObject
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
            raise FileSystemError(f"Attempting to remove a directory. Set recursive=True to remove all contents of this directory.")
        
        if self.is_root():
            raise FileSystemError(f"Attempting to remove root directory.")
        
        for fs_obj in self.contents.values():
            fs_obj.remove(recursive)
        
        self.parent.remove_child(self)
    
    def move(self, dst: "Directory"):
        self.parent.remove_child(self)
        for child in self.contents.values():
            dst.add_child(child)

    def add_child(self, child: FileSystemObject):
        name = child.name
        count = 1
        while name in self.contents:
            name = f"{child.name} ({count})"
            count += 1
        child.name = name
        self.contents[name] = child
        child.set_parent(self)

    def create_or_get_child_directory(self, name: str):
        if name not in self.contents:
            self.contents[name] = Directory(name=name, parent=self)
        return self.contents[name]
    
    def remove_child(self, child: FileSystemObject):
        """Used by the child to remove its own reference.

        Args:
            name: Name of the child object. Should correspond to the key in the self.contents dict.

        Raises:
            FileSystemError: If the name doesn't exist in the self.contents dict.
        """
        try:
            del self.contents[child.name]
        except KeyError:
            raise FileSystemError(f"Attempting to remove content that doesn't exist: {child.name}")
    
    def assert_directory(self):
        """This object is a directory, so calling this passes.
        """
        pass