# Memory File System

## Usage

Memory File System is an in-memory file system that supports many of the standard UNIX commands. Instantiating a `MemoryFileSystem` object creates an empty file system starting at root:


```python
from memory_fs.memory_fs import MemoryFileSystem

fs = MemoryFileSystem()
fs.pwd()
```




    '/'



Typical file system commands like `mkdir`, `cd`, and `ls` are supported:


```python
fs.mkdir('company')
fs.mkdir('company/organization0')
fs.cd('company')
fs.pwd()
```




    '/company'




```python
fs.mkdir('organization1')
fs.ls()
```




    ['organization0', 'organization1']



A simplified `walk` command is available, which helps illustrate the files and directories created so far:


```python
fs.walk('/')
```

    
    /company
    /company/organization0
    /company/organization1


Files can be written and read with `touch`, `write`, and `read` commands:


```python
fs.cd('organization0')
fs.touch('employee0.txt')
fs.write('employee0.txt', 'Name: Newton Le')
fs.touch('employee1.txt')
fs.write('employee1.txt', 'Name: Tiffany Smith')
fs.read('employee0.txt')
```




    'Name: Newton Le'




```python
fs.walk('/')
```

    
    /company
    /company/organization0
    /company/organization0/employee0.txt
    /company/organization0/employee1.txt
    /company/organization1


`cp` and `mv` commands work, with recurisve folder merging and automatic file name collision handling:


```python
fs.cp('/company', '/company2')
fs.touch('/company/organization0/employee2.txt')
fs.walk('/')
```

    
    /company
    /company/organization0
    /company/organization0/employee0.txt
    /company/organization0/employee1.txt
    /company/organization0/employee2.txt
    /company/organization1
    /company2
    /company2/organization0
    /company2/organization0/employee0.txt
    /company2/organization0/employee1.txt
    /company2/organization1



```python
fs.mv('/company', '/company2')
fs.walk('/')
```

    
    /company2
    /company2/organization0
    /company2/organization0/employee0.txt
    /company2/organization0/employee1.txt
    /company2/organization0/employee0.txt (1)
    /company2/organization0/employee1.txt (1)
    /company2/organization0/employee2.txt
    /company2/organization1


of course files and directories can be removed with `rm`:


```python
fs.rm('/company2/organization0', recursive=True)
fs.walk('/')
```

    
    /company2
    /company2/organization1


absolute and relative paths with `.` and `..` are also supported:


```python
fs.cd('/company2/organization1')
fs.mkdir('/company3')
fs.mkdir('../organization2')
fs.mkdir('../../company3/organization0')
fs.walk('/')
```

    
    /company2
    /company2/organization1
    /company2/organization2
    /company3
    /company3/organization0

