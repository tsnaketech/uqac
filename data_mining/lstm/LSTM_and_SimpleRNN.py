#!/usr/bin/python3
# -*- coding: utf-8 -*-

###### Import ########

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import time

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import SimpleRNN
from sklearn.preprocessing import MinMaxScaler

###### Variable ######

file = "apple.csv"
file = "AAPL_pres.csv"
file_test = "apple2019j.csv"
file_test = "AAPL_pres_test.csv"

###### Function ######

class Timer(object):  
    def start(self):  
        if hasattr(self, 'interval'):  
            del self.interval  
        self.start_time = time.time()  
  
    def stop(self):  
        if hasattr(self, 'start_time'):  
            self.interval = time.time() - self.start_time  
            del self.start_time

def model_SimpleRNN(features_set, labels, e = 100, u = 50):
    print("############# With SimpleRNN #############")
    timer = Timer()

    model = Sequential()

    model.add(SimpleRNN(units=u, return_sequences=True, input_shape=(features_set.shape[1], 1)))
    model.add(Dropout(0.2))

    model.add(SimpleRNN(units=u, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(SimpleRNN(units=u, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(SimpleRNN(units=u))
    model.add(Dropout(0.2))

    model.add(Dense(units = 1))

    model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    
    timer.start()
    model.fit(features_set, labels, epochs = e, batch_size = 32, verbose=2)
    timer.stop()
    print(f"[+] Timer : {timer.interval} secondes")

    return model

def model_LSTM(features_set, labels, e = 100, u = 50):
    print("############# With LSTM #############")
    timer = Timer()

    model = Sequential()

    model.add(LSTM(units=u, return_sequences=True, input_shape=(features_set.shape[1], 1)))
    model.add(Dropout(0.2))

    model.add(LSTM(units=u, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=u, return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(units=u))
    model.add(Dropout(0.2))

    model.add(Dense(units = 1))

    model.compile(optimizer = 'adam', loss = 'mean_squared_error')

    timer.start()
    model.fit(features_set, labels, epochs = e, batch_size = 32, verbose=2)
    timer.stop()
    print(f"[+] Timer : {timer.interval} secondes")

    return model

def protot(file):
    features_set = []
    labels = []
    apple_training_complete = pd.read_csv(file)
    apple_training_processed = apple_training_complete.iloc[:, 1:2].values
    scaler = MinMaxScaler(feature_range = (0, 1))
    apple_training_scaled = scaler.fit_transform(apple_training_processed)

    for i in range(60, len(apple_training_complete)):
        features_set.append(apple_training_scaled[i-60:i, 0])
        labels.append(apple_training_scaled[i, 0])

    features_set, labels = np.array(features_set), np.array(labels)
    features_set = np.reshape(features_set, (features_set.shape[0], features_set.shape[1], 1))
    return features_set, labels, apple_training_complete, scaler

def test(file, apple_training_complete, scaler):
    apple_testing_complete = pd.read_csv(file)
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


    return apple_testing_processed, test_features

def forecasting(model,test_features):
    predictions = model.predict(test_features)
    predictions = scaler.inverse_transform(predictions)
    return predictions

###### Program #######

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

features_set, labels, apple_training_complete, scaler = protot(file)

modelSimpleRNN = model_SimpleRNN(features_set,labels,u=50)
modelLSTM = model_LSTM(features_set,labels,u=50)

apple_testing_processed, test_features = test(file_test, apple_training_complete, scaler)

predictionsSimpleRNN = forecasting(modelSimpleRNN,test_features)
predictionsLSTM = forecasting(modelLSTM,test_features)

plt.figure(figsize=(10,6))
plt.plot(apple_testing_processed, color='blue', label='Actual Apple Stock Price')
plt.plot(predictionsSimpleRNN , color='darkgreen', label='Predicted Apple Stock Price with SimpleRNN')
plt.plot(predictionsLSTM , color='red', label='Predicted Apple Stock Price with LSTM')
plt.title('Apple Stock Price Prediction')
plt.xlabel('Date')
plt.ylabel('Apple Stock Price')
plt.legend()
plt.show()