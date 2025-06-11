# dummyfile.py — вспомогательный класс
from copy import deepcopy

class DummyFile:
    def __init__(self, base_data=None):
        if base_data is not None:
            self.commited_data = bytearray(deepcopy(base_data))
            self.virt_data = bytearray(deepcopy(base_data))
        else:
            self.commited_data = bytearray()
            self.virt_data = bytearray()
        self.current_position = 0

    def is_dirty(self):
        return self.commited_data != self.virt_data

    def revert(self):
        self.virt_data = bytearray(deepcopy(self.commited_data))
        self.current_position = 0
        return self

    def truncate(self, size=None):
        if size is None:
            raise ValueError("Size must be specified when truncating a DummyFile")
        self.virt_data = self.virt_data[:size]
        self.current_position = min(self.current_position, len(self.virt_data))
        return self

    def tell(self):
        return self.current_position

    def seek(self, offset, whence=0):
        if whence == 0:
            self.current_position = offset
        elif whence == 1:
            self.current_position += offset
        elif whence == 2:
            self.current_position = len(self.virt_data) + offset
        else:
            raise ValueError("Invalid whence value")
        self.current_position = max(0, min(self.current_position, len(self.virt_data)))
        return self.current_position

    def read(self, size=-1):
        if size == -1:
            size = len(self.virt_data) - self.current_position
        data = self.virt_data[self.current_position:self.current_position + size]
        self.current_position += len(data)
        return data

    def write(self, data):
        end_pos = self.current_position + len(data)
        if end_pos > len(self.virt_data):
            self.virt_data.extend(b'\x00' * (end_pos - len(self.virt_data)))
        self.virt_data[self.current_position:end_pos] = data
        self.current_position = end_pos
        return len(data)

    def getbuffer(self):
        return memoryview(self.virt_data)

    def save(self, file_name):
        with open(file_name, 'wb') as f:
            f.write(self.virt_data)

    def copy(self):
        new_dummy_file = DummyFile(deepcopy(self.commited_data))
        new_dummy_file.virt_data = bytearray(deepcopy(self.virt_data))
        new_dummy_file.current_position = self.current_position
        return new_dummy_file

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
