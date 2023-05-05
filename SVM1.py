from SVM import LinearSVM
import numpy as np
from matplotlib import pyplot as plt

dataset = [
    [[2, 0], 1],
    [[1, -1], 1],
    [[1, -2], 1],
    [[3, -1], 1],
    [[0, 0], -1],
    [[1.5, 1.5], -1],
    [[0, 1], -1],
    [[1, 2], -1]
]

linearSVM = LinearSVM.LinearSVM(dataset.__len__(), dataset[0][0].__len__())
linearSVM.train(dataset, 100)
print(linearSVM)

for record in dataset:
    vector = record[0]
    label = record[-1]
    if label == 1:
        plt.plot(vector[0], vector[1], 'r-o')
    else:
        plt.plot(vector[0], vector[1], 'g-o')

    predict = linearSVM.predict(vector)
    print(record.__str__() + predict.__str__() + '\n')

x1 = np.linspace(0, 1, 50)
x2 = (-linearSVM.bias - linearSVM.weight_vec[0] * x1) / linearSVM.weight_vec[1]
plt.plot(x1, x2)
plt.show()