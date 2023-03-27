from typing import cast

from memory_fs.directory import Directory
from memory_fs.exceptions import FileSystemError
from memory_fs.file import File
from memory_fs.fs_object import FileSystemObject


class MemoryFileSystem:
    def __init__(self) -> None:
        self.root: Directory = Directory(name='root', parent=None)
        self._pwd: Directory = self.root
    
    def cd(self, path: str):
        if not path:
            return
        fs_obj = self._get_object_at_path(path)
        fs_obj.assert_directory()
        self._pwd = cast(Directory, fs_obj)

    def pwd(self):
        if self._pwd.is_root():
            return '/'
        return self._pwd.get_path()
    
    def ls(self):
        return self._pwd.get_contents()
    
    def mkdir(self, path: str):
        path_list = self._to_path_list(path)
        fs_obj = self._traverse_path(self._pwd, path_list[:-1])
        fs_obj.assert_directory()
        working_directory = cast(Directory, fs_obj)
        working_directory.make_directory(path_list[-1])
    
    def rm(self, path: str, recursive=False):
        self._get_object_at_path(path).remove(recursive)

    def touch(self, path: str):
        self._get_object_at_path(path=path, create=True, create_file=True)

    def write(self, path: str, content: str):
        file_obj = self._get_object_at_path(path)
        file_obj.write(content)

    def read(self, path: str) -> str:
        file_obj = self._get_object_at_path(path)
        return file_obj.read()

    def find(self, name: str):
        return self._pwd.find(name)
    
    def mv(self, src_path: str, dst_path: str):
        src_obj = self._get_object_at_path(src_path)
        dst_obj = self._get_object_at_path(path=dst_path, create=True, create_file=isinstance(src_obj, File))
        src_obj.move(dst_obj)
    
    def cp(self, src_path: str, dst_path: str):
        src_obj = self._get_object_at_path(src_path)
        dst_obj = self._get_object_at_path(path=dst_path, create=True, create_file=isinstance(src_obj, File))
        src_obj.copy(dst_obj)

    def walk(self, path: str, fn: callable=lambda obj: print(obj.get_path())):
        fs_obj = self._get_object_at_path(path)
        fs_obj.walk(fn)

    def _get_object_at_path(self, path: str, create: bool = False, create_file: bool = False) -> FileSystemObject:
        if path == '/':
            return self.root
        working_directory = self.root if path[0] == '/' else self._pwd
        path_list = self._to_path_list(path)
        
        if create:
            fs_obj = self._traverse_path(working_directory, path_list[:-1])
            fs_obj.assert_directory()
            working_directory = cast(Directory, fs_obj)
            return working_directory.get_or_create_child(name=path_list[-1], create_file=create_file)
        else:
            return self._traverse_path(working_directory, path_list)
    
    def _traverse_path(self, base_object: FileSystemObject, path_list: list[str]) -> FileSystemObject:
        if not path_list:
            return base_object
        else:
            base_object.assert_directory()
            base_directory = cast(Directory, base_object)
        try:
            working_object: FileSystemObject
            if path_list[0] == '.':
                working_object = base_directory
            elif path_list[0] == '..':
                working_object = base_directory.parent
            else:
                working_object = base_directory.children[path_list[0]]
            return self._traverse_path(working_object, path_list[1:])
        except KeyError:
            raise FileSystemError(f"No such directory {path_list[0]}.")
    
    @staticmethod
    def _to_path_list(path: str) -> list[str]:
        return path.strip('/').split('/')