from memory_fs.fs_object import Directory, File
from memory_fs.memory_space import MemorySpace


class MemoryFileSystem:
    def __init__(self):
        self.memory_space = MemorySpace()
        self.root = Directory(name='root', parent=None)
        self._pwd = self.root
    
    def cd(self, path: str):
        if not path:
            return
        if path == '/':
            self._pwd = self.root
            return
       
        working_directory = self.root if path[0] == '/' else self._pwd
        self._pwd = working_directory.get_object(self._to_path_list(path))

    def pwd(self):
        pwd_ = self._pwd.get_path()
        return pwd_ if pwd_ else '/'
    
    def ls(self):
        return self._pwd.get_contents()
    
    def mkdir(self, name: str):
        name_list = name.split('/')
        working_directory = self._pwd.get_object(name_list[:-1])
        working_directory.make_directory(name_list[-1])
    
    def rm(self, path: str, recursive=False):
        working_directory = self.root if path[0] == '/' else self._pwd
        working_directory.get_object(self._to_path_list(path)).remove(recursive)

    def find(self, name: str):
        return self._pwd.find(name)
    
    @staticmethod
    def _to_path_list(path: str) -> list[str]:
        return path.strip('/').split('/')