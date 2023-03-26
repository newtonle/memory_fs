import pytest

from memory_fs.memory_fs import MemoryFileSystem

class TestMemoryFileSystem:
    def test_mkdir_cd_pwd_succeeds(self):
        fs = MemoryFileSystem()
        assert fs.pwd() == '/'
        
        fs.mkdir('school')
        fs.cd('school')
        assert fs.pwd() == '/school'

        fs.cd('..')
        assert fs.pwd() == '/'

        fs.mkdir('school/classes')
        fs.cd('school/classes')
        assert fs.pwd() == '/school/classes'

    def test_mkdir_ls_succeeds(self):
        fs = MemoryFileSystem()

        fs.mkdir('class1')
        fs.mkdir('class2')
        fs.mkdir('class1/student1')
        fs.mkdir('class1/student2')
        fs.mkdir('class1/student3')
        assert set(fs.ls()) == {'class1', 'class2'}

        fs.cd('class1')
        assert set(fs.ls()) == {'student1', 'student2', 'student3'}
    
    def test_mkdir_rm_succeeds(self):
        fs = MemoryFileSystem()

        fs.mkdir('school')
        assert fs.ls() == ['school']
        fs.rm('school', recursive=True)
        assert fs.ls() == []
    
    def test_example_commands_succeed(self):
        """ make "school" directory
            change directory to "school"
            get working directory => "/school"
            make "homework" directory
            change directory to "homework"
            make "math" directory
            make "lunch" directory
            make "history" directory
            make "spanish" directory
            delete "lunch" directory
            get working directory contents => ["math", "history", "spanish"]
            get working directory => "/school/homework"
            change directory to parent
            make "cheatsheet" directory
            get working directory contents => ["homework", "cheatsheet"]
            delete "cheatsheet" directory
            change directory to parent
            get working directory => "/"
        """
        fs = MemoryFileSystem()
        fs.mkdir('school')
        fs.cd('school')
        assert fs.pwd() == '/school'

        fs.mkdir('homework')
        fs.cd('homework')
        fs.mkdir('math')
        fs.mkdir('lunch')
        fs.mkdir('history')
        fs.mkdir('spanish')
        fs.rm('lunch', recursive=True)
        assert set(fs.ls()) == {'math', 'history', 'spanish'}
        assert fs.pwd() == '/school/homework'

        fs.cd('..')
        fs.mkdir('cheatsheet')
        assert set(fs.ls()) == {'homework', 'cheatsheet'}

        fs.rm('cheatsheet', recursive=True)
        fs.cd('..')
        assert fs.pwd() == '/'
    
    def test_find_succeeds(self):
        fs = MemoryFileSystem()

        fs.mkdir('newton')
        assert fs.find('newton') == ['/newton']
        assert fs.find('le') == []

        fs.mkdir('newton/le')
        assert fs.find('le') == ['/newton/le']

        fs.cd('newton/le')
        fs.mkdir('material')
        fs.cd('/')
        fs.mkdir('material')
        assert set(fs.find('material')) == {'/newton/le/material', '/material'}

    def test_root_properties(self):
        fs = MemoryFileSystem()
        assert fs.pwd() == '/'

        fs.cd('..')
        assert fs.pwd() == '/'

    def test_move_directory_succeeds(self):
        fs = MemoryFileSystem()

        fs.mkdir('destination')
        fs.mkdir('newton')
        fs.mv('newton', 'destination')
        