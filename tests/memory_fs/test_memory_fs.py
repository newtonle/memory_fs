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
        """ As in the assignment example"""
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

    def test_file_read_write_succeeds(self):
        fs = MemoryFileSystem()
        fs.mkdir('newton')
        fs.touch('newton/test_file.txt')
        fs.cd('newton')
        fs.write('test_file.txt', 'foobar')
        assert fs.read('test_file.txt') == 'foobar'

    def test_move_directory_succeeds(self):
        fs = MemoryFileSystem()

        fs.mkdir('destination')
        fs.mkdir('newton')
        fs.mkdir('newton/le')
        assert set(fs.ls()) == {'newton', 'destination'}

        fs.mv('newton', 'destination/newton')
        assert fs.ls() == ['destination']

        fs.cd('destination')
        assert fs.ls() == ['newton']

        fs.cd('newton')
        assert fs.ls() == ['le']

    def test_move_directory_handles_name_collisions(self):
        fs = MemoryFileSystem()

        fs.mkdir('destination')
        fs.mkdir('newton')
        fs.mkdir('newton/le')
        fs.mkdir('newton/tran')
        fs.touch('newton/le/test_file')
        fs.write('newton/le/test_file', 'hello')
        fs.mkdir('destination/le')
        fs.touch('destination/le/test_file')
        fs.write('destination/le/test_file', 'hello again')
        assert set(fs.ls()) == {'newton', 'destination'}

        fs.mv('newton', 'destination')
        assert fs.ls() == ['destination']

        fs.cd('destination')
        assert set(fs.ls()) == {'le', 'tran'}

        fs.cd('le')
        assert set(fs.ls()) == {'test_file', 'test_file (1)'}
        assert fs.read('test_file') == 'hello again'
        assert fs.read('test_file (1)') == 'hello'  # original contents in source file as expeted


    def test_copy_directory_handles_name_collisions(self):
        fs = MemoryFileSystem()

        fs.mkdir('destination')
        fs.mkdir('newton')
        fs.mkdir('newton/le')
        fs.mkdir('newton/tran')
        fs.touch('newton/le/test_file')
        fs.write('newton/le/test_file', 'hello')
        fs.mkdir('destination/le')
        fs.touch('destination/le/test_file')
        fs.write('destination/le/test_file', 'hello again')
        assert set(fs.ls()) == {'newton', 'destination'}

        fs.cp('newton', 'destination')
        assert set(fs.ls()) == {'newton', 'destination'}

        fs.cd('destination')
        assert set(fs.ls()) == {'le', 'tran'}

        fs.cd('le')
        assert set(fs.ls()) == {'test_file', 'test_file (1)'}
        assert fs.read('test_file') == 'hello again'
        assert fs.read('test_file (1)') == 'hello'

        fs.write('test_file (1)', 'something new')
        fs.cd('/newton/le')
        assert fs.read('test_file') == 'hello'  # original contents unaffected by change in destination
