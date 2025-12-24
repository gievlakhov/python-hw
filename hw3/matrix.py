import numpy as np

class Matrix:
    def __init__(self, data):
        self.data = np.array(data)
        if self.data.ndim != 2:
            raise ValueError("matrix must have two dimensiones")

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.data.shape != other.data.shape:
            raise ValueError("invalid shapes for matrix addition")

        return Matrix(self.data + other.data)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.data.shape != other.data.shape:
            raise ValueError("invalid shapes for matrix element-wise multiplication")

        return Matrix(self.data * other.data)

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.data.shape[1] != other.data.shape[0]:
            raise ValueError("invalid shapes for matrix multiplication")

        return Matrix(self.data @ other.data)

    def __str__(self):
        return np.array2string(self.data)


if __name__ == "__main__":
    np.random.seed(0)
    a = Matrix(np.random.randint(0, 10, (10, 10)))
    b = Matrix(np.random.randint(0, 10, (10, 10)))

    with open("artifacts/task1/matrix+.txt", "w") as file:
        file.write(str(a + b))

    with open("artifacts/task1/matrix*.txt", "w") as file:
        file.write(str(a * b))

    with open("artifacts/task1/matrix@.txt", "w") as file:
        file.write(str(a @ b))
