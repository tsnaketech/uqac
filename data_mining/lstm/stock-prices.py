import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import SimpleRNN
from sklearn.preprocessing import MinMaxScaler


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

apple_training_complete = pd.read_csv(r'apple.csv')
apple_training_processed = apple_training_complete.iloc[:, 1:2].values
scaler = MinMaxScaler(feature_range = (0, 1))
apple_training_scaled = scaler.fit_transform(apple_training_processed)

features_set = []
temp_list=[]
labels = []
for i in range(60, 1698):
    features_set.append(apple_training_scaled[i-60:i, 0])
    labels.append(apple_training_scaled[i, 0])


features_set, labels = np.array(features_set), np.array(labels)

features_set = np.reshape(features_set, (features_set.shape[0], features_set.shape[1], 1))

model = Sequential()
model.add(SimpleRNN(units=50, return_sequences=True, input_shape=(features_set.shape[1], 1)))

model.add(Dropout(0.2))

model.add(SimpleRNN(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(SimpleRNN(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(SimpleRNN(units=50))
model.add(Dropout(0.2))

model.add(Dense(units = 1))

model.compile(optimizer = 'adam', loss = 'mean_squared_error')

model.fit(features_set, labels, epochs = 10, batch_size = 32, verbose=)

apple_testing_complete = pd.read_csv(r'apple2019j.csv')
apple_testing_processed = apple_testing_complete.iloc[:, 1:2].values

apple_total = pd.concat((apple_training_complete['Open'], apple_testing_complete['Open']), axis=0)

test_inputs = apple_total[len(apple_total) - len(apple_testing_complete) - 60:].values

test_inputs = test_inputs.reshape(-1,1)
test_inputs = scaler.transform(test_inputs)

test_features = []
for i in range(60, 84):
    test_features.append(test_inputs[i-60:i, 0])

test_features = np.array(test_features)
test_features = np.reshape(test_features, (test_features.shape[0], test_features.shape[1], 1))

predictions = model.predict(test_features)

predictions = scaler.inverse_transform(predictions)

plt.figure(figsize=(10,6))
plt.plot(apple_testing_processed, color='blue', label='Actual Apple Stock Price')
plt.plot(predictions , color='red', label='Predicted Apple Stock Price')
plt.title('Apple Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Apple Stock Price')
plt.legend()
plt.show()