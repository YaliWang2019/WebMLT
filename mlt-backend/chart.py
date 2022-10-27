import os
import requests
import zipfile
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
from flask import Flask, render_template
from io import BytesIO
import base64
from sklearn.model_selection import train_test_split
app = Flask(__name__)
app.debug = True

@app.route('/index')
def linearregression_chart():

    chart = BytesIO()
    plt.cla()
    plt.savefig(chart, format = 'png')
    chart.seek(0)
    chart_png = base64.b64encode(chart.getvalue())

    return str(chart_png, "utf-8")

DATASET_TYPE = "downloaded" # Options are "toy" or "downloaded"

def generate_dataset():
  X = np.linspace(0, 2, 100)
  Y = 1.5 * X + np.random.randn(*X.shape) * 0.2 + 0.5
  return X, Y

if DATASET_TYPE == "toy":
  X, Y = generate_dataset()

def download_dataset():
  if (not os.path.exists('Bike-Sharing-Dataset.zip')):
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip'
    r = requests.get(url)
    open('Bike-Sharing-Dataset.zip', 'wb').write(r.content)

  zf = zipfile.ZipFile('Bike-Sharing-Dataset.zip')
  # Load data from URL using pandas read_csv method
  bike_data_daily = pd.read_csv(zf.open('day.csv'))
  return bike_data_daily.atemp.to_numpy(), bike_data_daily.cnt.to_numpy()

if DATASET_TYPE == "downloaded":
  X, Y = download_dataset()

# Scale the Data
Y = (Y - np.mean(Y)) / np.std(Y)

# Visualize the full Dataset
# img_scatter
img_scatter = BytesIO()
plt.scatter(X, Y)
plt.savefig(img_scatter, format = 'png')

# Split the Dataset into Training and Test Set
from matplotlib.pyplot import figure
X_train_split, X_test_split, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

figure(figsize=(18, 6), dpi=80)
img_train = BytesIO()
plt.subplot(1, 2, 1) # row 1, col 2 index 1
plt.scatter(X_train_split, Y_train)
plt.title("Training Data")
plt.xlabel('X_train')
plt.ylabel('Y_train')
plt.savefig(img_train, format = 'png')

img_test = BytesIO()
plt.subplot(1, 2, 2) # index 2
plt.scatter(X_test_split, Y_test)
plt.title("Test Data")
plt.xlabel('X_test')
plt.ylabel('Y_test')

plt.tight_layout()
plt.savefig(img_test, format = 'png')
# Create a 2D array for training and test data to make it compatible with
# scikit-learn (This is specific to scikit-learn because of the way it accepts input data)
X_train = X_train_split.reshape(-1, 1)
X_test = X_test_split.reshape(-1, 1)
X_train.shape, X_test.shape

# Initialize Model
from sklearn.linear_model import SGDRegressor
regressor = SGDRegressor()

# Run Model Training
regressor.fit(X_train, Y_train)

# Predict on the Test Data
Y_pred = regressor.predict(X_test)

# Plot the predictions and the original test data
X_test_split.shape, Y_pred.shape, Y_test.shape

img_prediction = BytesIO()
plt.clf()
plt.plot(X_test_split, Y_test, 'go', label='True data', alpha=0.5)
plt.plot(X_test_split, Y_pred, '--', label='Predictions', alpha=0.5)
plt.legend(loc='best')
plt.savefig(img_prediction, format = 'png')

# Evaluate the quality of the training (Generate Evaluation Metrics)
from sklearn import metrics
print('Mean Absolute Error:', metrics.mean_absolute_error(Y_test, Y_pred))
print('Mean Squared Error:', metrics.mean_squared_error(Y_test, Y_pred))
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(Y_test, Y_pred)))