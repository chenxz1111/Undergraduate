### <center>实验一：傅里叶级数的可视化</center>

<center>陈炫中 &nbsp; 2019011236</center>

#### 1. 实验目的

- 对信号的傅里叶级数做可视化，理解傅里叶级数是如何近似周期函数的。

#### 2. 实验原理

​	对于周期为 $T_1$的函数$f(t)$，它的三角形式的傅里叶级数展开可以写为
$$
f(t) = a_0 +\sum_{n = 1}^{\infin}(a_ncosn\omega_1t+b_nsinn\omega_1t)
$$
​	其中，通过信号的正交变换（Karhunen-Loeve），可以得到
$$
a_0 = \frac{1}{T_1}\int_{t0}^{t_0+T_1}f(t)dt\\
a_n = \frac{2}{T_2}\int^{t_0+T}_{t_0}f(t)cos(n\omega_1t)dt,n\in N^+\\
b_n = \frac{2}{T_2}\int^{t_0+T}_{t_0}f(t)sin(n\omega_1t)dt,n\in N^+\\
$$

#### 3.实验过程

​	在本次实验中，对于周期为$2\pi$的方波信号和半圆波信号，根据上述公式计算可得三角形式的傅里叶级数的系数为
$$
a_0 = \frac{1}{2\pi}\int_{0}^{2\pi}f(t)dt\\
a_n = \frac{1}{\pi}\int^{2\pi}_{0}f(t)cos(nt)dt,n\in N^+\\
b_n = \frac{1}{\pi}\int^{2\pi}_{0}f(t)sin(nt)dt,n\in N^+\\
$$
​	在计算积分的过程中，我调用了`scipy`模块下的子模块`integrate`里的`quad`函数来计算求值，傅里叶级数的系数计算的具体代码如下：

```python
def fourier_coefficient(n):
    if n == 0:
        def f(t) :
            return function(t)
        a0 = integrate.quad(f, 0, 2 * np.pi, limit=100)[0] / (2 * np.pi)
        #print("a0", a0)
        return a0
    elif n % 2:
        m = (n + 1) / 2
        def f(t) :
            return function(t) * np.sin(m * t)
        bm =  integrate.quad(f, 0, 2 * np.pi, limit=100)[0] / np.pi
        #print("b"+str(m), bm)
        return bm
    else:
        m = n / 2
        def f(t):
            return function(t) * np.cos(m * t)
        am = integrate.quad(f, 0, 2 * np.pi,limit=100)[0] / np.pi
        #print("a"+str(m), am)
        return am
```

​	之后运行`exp.py`后在同目录下得到`square_n=[2, 4, 8, 16, 32, 64, 128].mp4`文件，完成对傅里叶级数的可视化。

​	修改`signal_name = "semicircle"`后得到`semicircle_n=[2, 4, 8, 16, 32, 64, 128].mp4`文件。

#### 4.心得

​	在本次实验中，随着傅里叶级数展开的项数的增加，圆上的点的纵坐标的叠加值与方波（半圆波）函数的函数值越来越接近（实验中得到的红线也越来越与 x 轴平行），这也让我更直观地理解了通过傅里叶级数的逼近来近似周期函数的过程。

