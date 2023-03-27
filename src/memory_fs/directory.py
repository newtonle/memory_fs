from typing import Optional

from memory_fs.exceptions import FileSystemError
from memory_fs.file import File
from memory_fs.fs_object import FileSystemObject


class Directory(FileSystemObject):
    def __init__(self, name: str, parent: Optional["Directory"]):
        self.children: dict[str, FileSystemObject] = {}
        self.name = name
        self.parent = parent or self  # root object's parent is itself

    def get_contents(self) -> list[str]:
        return list(self.children.keys())
    
    def make_directory(self, name):
        if name in self.children:
            raise FileSystemError(f"Can't create directory {name}. It already exists.")
        self.children[name] = Directory(name=name, parent=self)

    def find(self, name: str) -> list[str]:
        found_paths = []
        if name in self.children:
            found_paths.append(self.children[name].get_path())
        
        for fs_obj in self.children.values():
            found_paths.extend(fs_obj.find(name))
        return found_paths
    
    def remove(self, recursive: bool=False):
        if not recursive:
            raise FileSystemError(f"Attempting to remove a directory. Set recursive=True to remove this directory with all its contents.")
        
        if self.is_root():
            raise FileSystemError(f"Attempting to remove root directory.")
        
        for fs_obj in self.children.values():
            fs_obj.remove(recursive)
        
        self.parent.remove_child(self)
    
    def move(self, dst: "Directory"):
        for name, child in list(self.children.items()):
            if name in dst.children:
                if isinstance(child, File) and isinstance(dst.children[name], File):
                    new_name = self._resolve_file_name_collision(dst, name)
                    child.name = new_name
                    dst.add_child(child)
                elif isinstance(child, Directory) and isinstance(dst.children[name], Directory):
                    child.move(dst.children[name])
                else:
                    raise FileSystemError(f"Trying to merge file and directories of the same name: {name}")
            else:
                dst.add_child(child)
            print(f"added {child.name} to {dst.name}")
        self.parent.remove_child(self)
    
    @staticmethod
    def _resolve_file_name_collision(dst_dir: "Directory", name: str) -> str:
        count = 1
        new_name = name
        while new_name in dst_dir.children:
            new_name = f"{name} ({count})"
            count += 1
        return new_name

    def walk(self, fn: callable=lambda obj: print(obj.get_path())):
        fn(self)
        for child in self.children.values():
            child.walk(fn)


    def add_child(self, child: FileSystemObject):
        self.children[child.name] = child
        child.set_parent(self)

    def get_or_create_child(self, name: str, create_file: bool=False) -> FileSystemObject:
        if name not in self.children:
            if create_file:
                self.children[name] = File(name=name, parent=self)
            else:
                self.children[name] = Directory(name=name, parent=self)
        return self.children[name]
    
    def remove_child(self, child: FileSystemObject):
        """Used by the child to remove its own reference.

        Args:
            name: Name of the child object. Should correspond to the key in the self.children dict.

        Raises:
            FileSystemError: If the name doesn't exist in the self.children dict.
        """
        print(f"Removing {child.name} from {self.name}")
        try:
            del self.children[child.name]
        except KeyError:
            raise FileSystemError(f"Attempting to remove content that doesn't exist: {child.name}")
    
    def assert_directory(self):
        """This object is a directory, so calling this passes.
        """
        pass