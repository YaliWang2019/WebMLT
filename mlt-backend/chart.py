import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
from flask import Flask, render_template
from io import BytesIO
import base64
app = Flask(__name__)
app.debug = True

@app.route('/index')
def simple_chart(x1, x2):
    chart = BytesIO()
    x1_sq = np.square(x1)
    x2_cu = pow(x2, 3)
    plt.plot(x1_sq, x2_cu)
    plt.savefig('chart.png')
    chart.seek(0)
    chart_png = base64.b64encode(plt.getvalue())

    return chart_png