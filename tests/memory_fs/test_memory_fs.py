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
        assert set(fs.ls()) == {'class1', 'class2'}

        fs.mkdir('class1/student1')
        fs.mkdir('class1/student2')
        fs.mkdir('class1/student3')

        fs.cd('class1')
        assert set(fs.ls()) == {'student1', 'student2', 'student3'}
    
    def test_mkdir_rm_succeeds(self):
        fs = MemoryFileSystem()

        fs.mkdir('school')
        assert fs.ls() == ['school']
        fs.rm('school', recursive=True)
        assert fs.ls() == []