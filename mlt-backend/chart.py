import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
from flask import Flask, render_template
from io import BytesIO
import base64
app = Flask(__name__)

@app.route('/plot')
def simple_chart(x1, x2):
    img = BytesIO()
    x1_sq = np.square(x1)
    x2_cu = pow(x2, 3)
    plt.plot(x1_sq, x2_cu)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')

    return img.png