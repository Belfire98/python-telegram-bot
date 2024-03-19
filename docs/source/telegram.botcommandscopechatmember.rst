import numpy as np

# Display version
print("NumPy version: ", np.__version__)

# Create a 1D array
arr1 = np.array([1, 2, 3, 4, 5])
print("1D Array:")
print(arr1)

# Create a 2D array
arr2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print("\n2D Array:")
print(arr2)

# Array operations
add_arr = np.add(arr1, arr2)
print("\nAddition of 1D and 2D arrays:")
print(add_arr)

sub_arr = np.subtract(arr1, arr2)
print("\nSubtraction of 1D and 2D arrays:")
print(sub_arr)

mul_arr = np.multiply(arr1, arr2)
print("\nMultiplication of 1D and 2D arrays:")
print(mul_arr)

div_arr = np.divide(arr1, arr2)
print("\nDivision of 1D and 2D arrays:")
print(div_arr)

# Matrix multiplication
matmul_arr = np.matmul(arr2, arr2)
print("\nMatrix multiplication of 2D array with itself:")
print(matmul_arr)
