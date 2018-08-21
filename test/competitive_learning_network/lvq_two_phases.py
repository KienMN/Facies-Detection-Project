# LVQ with Neighborhood Model

# Adding path to libraries
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Importing the libraries
import numpy as np
import pandas as pd

# Importing the dataset
filepath = os.path.join(os.path.dirname(__file__), 'data/SD-3X_rocktype.csv')
dataset = pd.read_csv(filepath)
X = dataset.iloc[:, 0: -1].values
y = dataset.iloc[:, -1].values.astype(np.int8)

# Spliting the dataset into the Training set and the Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

# Feature scaling
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (-1, 1))
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Label encoder
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)

# Training the LVQ
from detection.competitive_learning_network import AdaptiveLVQ
lvq = AdaptiveLVQ(n_rows = 9, n_cols = 9,
                  learning_rate = 0.5, decay_rate = 1,
                  sigma = 1, sigma_decay_rate = 1,
                  # weights_normalization = "length",
                  bias = False, weights_init = 'pca',
                  neighborhood='gaussian', label_weight = 'exponential_distance')
lvq.fit(X_train, y_train, first_num_iteration = 4000, first_epoch_size = 400, second_num_iteration = 4000, second_epoch_size = 400)

# Predict the result
y_pred, confidence_score = lvq.predict(X_test, confidence = 1, crit='winner_neuron')
y_pred = encoder.inverse_transform(y_pred)

# Making confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

# Printing the confusion matrix
print(cm)
true_result = 0
for i in range (len(cm)):
  true_result += cm[i][i]
print(true_result / np.sum(cm))

print(lvq._winner_count)
# Visualization
# from detection.competitive_learning_network.visualization import network_mapping, feature_distribution

# feature_distribution(9, 9, lvq._competitive_layer_weights, figure_path = '/Users/kienmaingoc/Desktop/som_test4.png')

# network_mapping(9, 9, 4, lvq._competitive_layer_weights, lvq._linear_layer_weights, 
#                 encoder.inverse_transform(np.arange(0, 4, 1)),
#                 figure_path = '/Users/kienmaingoc/Desktop/som_test3.png')

# for i in range (len(y_pred)):
#   print(i, y_pred[i], y_test[i], confidence_score[i])