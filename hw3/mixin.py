import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin

class FileMixin:
    def save(self, filename: str):
        with open(filename, "w") as file:
            file.write(str(self))

class PrettifierMixin:
    def __str__(self):
        return np.array2string(self._data)

class DataMixin:
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        arr = np.array(value)
        if arr.ndim != 2:
            raise ValueError("matrix must have two dimensiones")
        self._data = arr

class Matrix(NDArrayOperatorsMixin, FileMixin, PrettifierMixin, DataMixin):
    __array_priority__ = 1

    def __init__(self, data):
        self.data = np.array(data)

    def __array__(self, dtype=None):
        return np.asarray(self._data, dtype=dtype)

    def __array_wrap__(self, arr, context=None):
        return Matrix(arr)

if __name__ == "__main__":
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))

    with open("artifacts/task2/matrix+.txt", "w") as file:
        file.write(str(a + b))

    with open("artifacts/task2/matrix*.txt", "w") as file:
        file.write(str(a * b))

    with open("artifacts/task2/matrix@.txt", "w") as file:
        file.write(str(a @ b))
