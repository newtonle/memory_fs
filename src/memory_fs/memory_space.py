from memory_fs.exceptions import MemorySystemError

class MemorySpace:
    def __init__(self):
        self.space = {}
        self.free_address = 0
    
    def get(self, address: int):
        try:
            return self.space[address]
        except KeyError:
            raise MemorySystemError(f"Unable to get object at address {address}. It does not exist.")
    
    def remove(self, address: int):
        try:
            del self.space[address]
        except KeyError:
            raise MemorySystemError(f"Unable to remove object at address {address}. It does not exist.")
    
    def write(self, address: int, contents: str):
        self.space[address] = contents

    def write_new(self, contents: str) -> int:
        self.space[self.free_address] =  contents
        address = self.free_address
        self.free_address += 1
        return address