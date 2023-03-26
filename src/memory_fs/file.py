from memory_fs.directory import Directory
from memory_fs.exceptions import FileSystemError
from memory_fs.file_contents import FileContents
from memory_fs.fs_object import FileSystemObject

class File(FileSystemObject):
    def __init__(self, name: str, parent: "Directory"):
        self.name = name
        self.parent = parent
        self.contents = FileContents(None)
    
    def get_contents(self) -> str:
        return self.contents.contents
    
    def remove(self, recursive: bool=False):
        self.parent.remove_child(self)
    
    def get_object(self, path_list: list[str]) -> "FileSystemObject":
        raise FileSystemError(f"Invalid path. {self.name} is a file, not a directory.")
    
    def write(self, contents: str):
        self.contents.contents = contents
    
    def find(self, name: str) -> list[str]:
        return []
    
    def move(self, dst: "File"):
        self.parent.remove_child(self)
        self.parent = dst.parent
        self.name = dst.name
        dst.remove()
        self.parent.add_child(self)
    
    def assert_directory(self):
        raise FileSystemError(f"{self.name} is a file, not a directory.")