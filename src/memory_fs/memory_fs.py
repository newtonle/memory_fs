from typing import cast, Callable

from memory_fs.directory import Directory
from memory_fs.exceptions import FileSystemError
from memory_fs.file import File
from memory_fs.fs_object import FileSystemObject


class MemoryFileSystem:
    def __init__(self) -> None:
        self.root: Directory = Directory(name='root', parent=None)
        self._pwd: Directory = self.root
    
    def cd(self, path: str):
        """Change directory. Similar to UNIX's cd command.

        Args:
            path (str): relative or absolute path
        """
        if not path:
            return
        fs_obj = self._get_object_at_path(path)
        fs_obj.assert_directory()
        self._pwd = cast(Directory, fs_obj)

    def pwd(self) -> str:
        """Present working directory. Similar to UNIX's pwd command.

        Returns:
            path of the present working directory
        """
        if self._pwd.is_root():
            return '/'
        return self._pwd.get_path()
    
    def ls(self) -> list[str]:
        """List directory. Similar to UNIX's ls command.

        Returns:
            list of directories and files in this directory
        """
        return self._pwd.get_children()
    
    def mkdir(self, path: str):
        """Make directory. Similar to UNIX's mkdir command.

        Args:
            path: relative or absolute path to create
        """
        path_list = self._to_path_list(path)
        fs_obj = self._traverse_path(self._pwd, path_list[:-1])
        fs_obj.assert_directory()
        working_directory = cast(Directory, fs_obj)
        working_directory.make_directory(path_list[-1])
    
    def rm(self, path: str, recursive: bool=False):
        """Remove a file or directory. Similar to UNIX's rm command.

        Args:
            path: path to file or directory to remove
            recursive: Flag to recursively delete the contents of a directory. Defaults to False.
        """
        self._get_object_at_path(path).remove(recursive)

    def touch(self, path: str):
        """Creates an empty file at the path. Similar to UNIX's touch command.

        Args:
            path: Path to empty file to create. If file exists, this is a no-op.
        """
        self._get_object_at_path(path=path, create=True, create_file=True)

    def write(self, path: str, content: str):
        """Write content to the file path.

        Args:
            path: path to the file. The file must exist.
            content: string to write to this file.
        """
        file_obj = self._get_object_at_path(path)
        if isinstance(file_obj, File):
            file_obj.write(content)
        else:
            raise FileExistsError(f"Can't write to {path}. It is a directory.")

    def read(self, path: str) -> str:
        """Read content from the file path.

        Args:
            path: path to the file

        Returns:
            content of the file
        """
        file_obj = self._get_object_at_path(path)
        if isinstance(file_obj, File):
            return file_obj.read()
        else:
            raise FileExistsError(f"Can't read from {path}. It is a directory.")

    def find(self, name: str):
        """Find files or directory with an exact match to the name in the pwd

        Args:
            name: name of the file or directory

        Returns:
            list of absolute paths of files and directories found in the pwd
        """
        return self._pwd.find(name)
    
    def mv(self, src_path: str, dst_path: str):
        """Move file or directory at src_path to dst_path. This doesn't yet handle all the edge cases
        of the UNIX mv command (directory or file at dst doesn't exist and isn't specified in the dst_path)
        
        Args:
            src_path: path to source file or directory
            dst_path: path to destination file or directory
        """
        src_obj = self._get_object_at_path(src_path)
        dst_obj = self._get_object_at_path(path=dst_path, create=True, create_file=isinstance(src_obj, File))
        src_obj.move(dst_obj)
    
    def cp(self, src_path: str, dst_path: str):
        """Copy file or directory at src_path to dst_path. This doesn't yet handle all the edge cases
        of the UNIX mv command (directory or file at dst doesn't exist and isn't specified in the dst_path)

        Args:
            src_path: path to source file or directory
            dst_path: path to destination file or directory
        """
        src_obj = self._get_object_at_path(src_path)
        dst_obj = self._get_object_at_path(path=dst_path, create=True, create_file=isinstance(src_obj, File))
        src_obj.copy(dst_obj)

    def walk(self, path: str, fn: Callable=lambda obj: print(obj.get_path())):
        """Walk the path and run fn on each file or directory

        Args:
            path: path to walk
            fn: callable to use during walk. Defaults to printing out the paths of the directories and files
        """
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