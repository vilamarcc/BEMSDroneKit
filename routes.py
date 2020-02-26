import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


def getHelix(hmax, sep, wall1, wall2, bufferD):
    a = max(wall1,wall2) * 2
    b = min(wall2,wall1) * 2
    C = np.sqrt(a**2 - b**2)
    e = C / a
    n = (hmax / sep)
    c = hmax / (2 * np.pi * n)
    theta = np.linspace(0, np.pi * n * 2 , 300)
    z = c * theta
    r = (b / np.sqrt(1 - (e**2)*(np.cos(theta)))) + bufferD 
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x,y,z