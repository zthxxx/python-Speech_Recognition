# -*- coding: utf-8 -*-
import numpy
import numpy as np

def zx_lms(xn, dn, M=50, W=np.ones(50), u=0.1, max_iter=150, min_err=0.3):
    """
    :param xn:输入信号 行向量或行矩阵
    :param dn:期望输出 行向量或行矩阵
    :param W:初始化权值
    :param u:学习率
    :param M:滤波器阶数
    :param max_iter:最大迭代次数
    :param min_err:迭代最小误差
    :return: (yn, err)   (自适应滤波输出, 误差值)
    """
    if len(W) != M:
        raise Exception('param.w的长度必须与滤波器阶数相同.')
    if max_iter > len(xn) or max_iter < M:
        raise Exception('迭代次数太大或太小，M<=max_iter<=length(xn)')

    iter = 0
    for k in range(M, max_iter + 1):
        x = xn[k - M:k] # 滤波器M个抽头的倒序输入
        x = x[::-1]     # 滤波器M个抽头的倒序输入
        y = W * x       #此处为点乘
        err = dn[k-M] - y
        #更新滤波器权值系数
        W = W + 2 * u * x

        iter += 1
        if False not in (numpy.abs(err) < min_err):
            break

    # 求最优时滤波器的输出序列
    yn = numpy.zeros(len(xn))
    w_t = W
    w_t.shape = (1, -1)
    w_t = w_t.T
    for k in range(0, M):
        x = xn[0:k + 1]
        w = w_t[-1:-(k + 2):-1]
        yn[k] = numpy.dot(x, w)
    for k in range(M, len(xn)):
        x = xn[k - M:k]
        x = x[::-1]
        yn[k] = numpy.dot(x, w_t)

    return yn



if __name__ == "__main__":
    import pylab as pl
    t = np.arange(-5 * np.pi, 5* np.pi, np.pi/102.4)
    x = np.sin(t)
    # pl.ion()
    pl.figure()
    pl.subplot(221)
    pl.plot(x)
    xf = np.fft.fft(x)
    pl.subplot(223)
    pl.plot(np.abs(xf))

    noise = 0.7 * np.random.randn(len(x))
    xs = x + noise
    pl.subplot(222)
    pl.plot(xs)
    xsf = np.fft.fft(xs,1024)
    pl.subplot(224)
    pl.plot(np.abs(xsf))
    # pl.show()

    t = np.arange(0, 1, 1/100)
    dn = np.sin(10 * np.pi * t)

    M = 50
    W = np.ones(M)
    u = 0.1
    max_iter = 100
    min_err = 0.5

    yn = zx_lms(xs, dn, M, W, u, max_iter, min_err)
    pl.figure()
    pl.plot(yn)
    pl.figure()
    ynf = np.fft.fft(yn,1024)
    pl.plot(np.abs(ynf))
    pl.show()




















