# Memory File System

## Usage

Memory File System is an in-memory file system that supports many of the standard UNIX commands. Instantiating a `MemoryFileSystem` object creates an empty file system starting at root:


```python
from memory_fs.memory_fs import MemoryFileSystem

fs = MemoryFileSystem()
fs.pwd()
```




    '/'




```python

```
