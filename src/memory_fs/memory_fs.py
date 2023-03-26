from typing import cast

from memory_fs.directory import Directory
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
        fs_obj = self._pwd.get_object(path_list[:-1])
        fs_obj.assert_directory()
        working_directory = cast(Directory, fs_obj)
        working_directory.make_directory(path_list[-1])
    
    def rm(self, path: str, recursive=False):
        self._get_object_at_path(path).remove(recursive)

    def find(self, name: str):
        return self._pwd.find(name)
    
    def mv(self, src_path: str, dst_path: str):
        src_obj = self._get_object_at_path(src_path)
        dst_obj = self._get_object_at_path(dst_path)
        src_obj.move(dst_obj)

    def _get_object_at_path(self, path: str, create_file: bool = False, create_directory: bool = False) -> FileSystemObject:
        if path == '/':
            return self.root
        working_directory = self.root if path[0] == '/' else self._pwd
        path_list = self._to_path_list(path)
        if create_directory:
            fs_obj = working_directory.get_object(path_list[:-1])

        return working_directory.get_object(path_list)
    
    @staticmethod
    def _to_path_list(path: str) -> list[str]:
        return path.strip('/').split('/')