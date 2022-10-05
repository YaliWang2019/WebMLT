import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

def simple_chart(x):
    x2 = np.square(x)
    y = pow(x, 3)
    return x2, y