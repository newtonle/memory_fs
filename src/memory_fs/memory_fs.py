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
        working_directory = self.root if path[0] == '/' else self._pwd
        self._pwd = working_directory.get_object(path.split('/'))

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
        working_directory.get_object(path.split('/')).remove(recursive)
