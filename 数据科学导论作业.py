import numpy as np
from matplotlib import pyplot as plt


def selectJrand(i, m):
    j = i
    while (j == i):
        j = int(np.random.uniform(0, m))
    return j


def clipAlpha(aj, H, L):
    if aj > H:
        aj = H
    if aj < L:
        aj = L
    return aj


def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
    dataMatrix = np.mat(dataMatIn)
    labelMat = np.mat(classLabels).transpose()
    b = 0
    m, n = np.shape(dataMatrix)
    alphas = np.mat(np.zeros((m, 1)))
    iters = 0
    while (iters < maxIter):
        alphaPairsChanged = 0
        for i in range(m):
            fxi = float(np.multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
            Ei = fxi - float(labelMat[i])
            if (((labelMat[i] * Ei) < -toler) and (alphas[i] < C)) or ((labelMat[i] * Ei > toler) and (alphas[i] > 0)):
                j = selectJrand(i, m)
                fxj = float(np.multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[j, :].T)) + b
                Ej = fxj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if (labelMat[i] != labelMat[j]):
                    L = max(0, alphas[j] - alphas[i])
                    H = min(C, C + alphas[j] - alphas[i])
                else:
                    L = max(0, alphas[j] + alphas[i] - C)
                    H = min(C, alphas[j] + alphas[i])
                if L == H:
                    print('L=H')
                    continue
                eta = 2.0 * dataMatrix[i, :] * dataMatrix[j, :].T - dataMatrix[i, :] * dataMatrix[i, :].T - dataMatrix[
                                                                                                            j,
                                                                                                            :] * dataMatrix[
                                                                                                                 j, :].T
                if eta >= 0:
                    print('eta>=0')
                    continue
                alphas[j] -= labelMat[j] * (Ei - Ej) / eta
                alphas[j] = clipAlpha(alphas[j], H, L)
                if (abs(alphas[j] - alphaJold) < 0.00001):
                    print('J is not move')
                    continue
                alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])
                b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[i, :].T - labelMat[
                    j] * (alphas[j] - alphaJold) * dataMatrix[i, :] * dataMatrix[j, :].T
                b2 = b - Ej - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T - labelMat[
                    j] * (alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T
                if (0 < alphas[i]) and (C > alphas[i]):
                    b = b1
                elif (0 < alphas[j]) and (C > alphas[j]):
                    b = b2
                else:
                    b = (b1 + b2) / 2.0
                alphaPairsChanged += 1
                print('iter:%d   i:%d   pairs:%d' % (iters, i, alphaPairsChanged))
        if (alphaPairsChanged == 0):
            iters += 1
        else:
            iters = 0
        print('iteration number :%d' % iters)
    return b, alphas


if __name__ == '__main__':
    data = np.array([[2, 0], [1, -1], [1, -2], [3, -1], [0, 0], [1.5, 1.5], [0, 1], [1, 2]])
    label = np.array([1, 1, 1, 1, -1, -1, -1, -1])

    b, alpha = smoSimple(data, label, 0.6, 0.001, 100)
    w = 0
    alpha_new = alpha.tolist()
    for i in range(8):
        w += alpha[i] * label[i] * data[i]
    print("b是{}".format(b))
    print("lambda是{}".format(alpha))
    print("w是{}".format(w))
    w_new = w.tolist()
    print(w_new[0][1])
    plt.scatter(data[:, 0], data[:, 1], c=label)
    k = -w_new[0][0] / w_new[0][1]  # 斜率,即w
    xx = np.linspace(-5, 5)  # 用于画超平面
    yy = k * xx - b / w_new[0][1]  # 带入 x 的值，获得直线方程
    plt.plot(xx, yy.tolist()[0], 'k-')
    plt.show()
