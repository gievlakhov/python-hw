import numpy as np

cache = {}

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
        
        key = (hash(self), hash(other))
        if key in cache:
            return cache[key]

        res = Matrix(self.data @ other.data)
        cache[key] = res

        return res

    def __str__(self):
        return np.array2string(self.data)
    
    def __hash__(self):
        h = 0
        rows, cols = self.data.shape
        for i in range(rows):
            for j in range(cols):
                h += (i * 17 + j * 13 + 11 * self.data[i, j])

        return int(h % 997)

if __name__ == "__main__":
    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[1, 0], [0, 1]])
    C = Matrix([[2, 1], [4, 3]])
    D = Matrix([[1, 0], [0, 1]])

    AB = A @ B
    CD = C @ D

    with open("artifacts/task3/A.txt", "w") as file:
        file.write(str(A))
    
    with open("artifacts/task3/B.txt", "w") as file:
        file.write(str(B))

    with open("artifacts/task3/C.txt", "w") as file:
        file.write(str(C))

    with open("artifacts/task3/D.txt", "w") as file:
        file.write(str(D))

    with open("artifacts/task3/AB.txt", "w") as file:
        file.write(str(AB))

    with open("artifacts/task3/CD.txt", "w") as file:
        file.write(str(CD))

    with open("artifacts/task3/hash.txt", "w") as file:
        file.write(f"AB hash: {hash(AB)}\n")
        file.write(f"CD hash: {hash(CD)}\n")
