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