import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

# chart
def simple_chart(a):
    x = np.linspace(0,5,10)
    y = x**2
    plt.plot(x, y)
    int(a)
    result = np.interp(a, x,y)
    print(result)

# table
data = [[1, "apple"], 
        [2, "banana"], 
        [3, "orange"], 
        [4, "cherry"]]

col_names = ["ID", "Item"]
  
#display table
tabulate(data, headers=col_names, tablefmt="fancy_grid", showindex="always")