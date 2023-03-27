from typing import TYPE_CHECKING

from memory_fs.exceptions import FileSystemError
from memory_fs.fs_object import FileSystemObject
from memory_fs.file_content import FileContent

if TYPE_CHECKING:
    from memory_fs.directory import Directory


class File(FileSystemObject):
    def __init__(self, name: str, parent: "Directory"):
        self.name = name
        self.parent = parent
        self.content = FileContent(None)
    
    def get_content(self) -> str:
        return self.content.content
    
    def remove(self, recursive: bool=False):
        self.parent.remove_child(self)
    
    def write(self, content: str):
        self.content.content = content
    
    def find(self, name: str) -> list[str]:
        return []
    
    def move(self, dst: "File"):
        self.parent.remove_child(self)
        self.parent = dst.parent
        self.name = dst.name
        dst.remove()
        self.parent.add_child(self)
    
    def walk(self, fn: callable):
        fn(self)

    def assert_directory(self):
        raise FileSystemError(f"{self.name} is a file, not a directory.")
