# import os
import h5py
import numpy as np
# import matplotlib.pyplot as plt
# import argparse
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense
from keras.layers import LSTM
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.preprocessing import normalize

# TODO: need to update !!!


def shuffle_data(_data, seed=8):
    shuffle = np.array(range(np.size(_data, 0)))
    np.random.seed(seed)
    np.random.shuffle(shuffle)
    data_shuffled = _data.copy()
    for _i in range(len(shuffle)):
        data_shuffled[_i] = _data[shuffle[_i]]
    return data_shuffled


def norm_data(_data, _minmax=180):
    return _data/_minmax


def denorm_data(_data, _minmax=180):
    return _data*_minmax


def load_input_data(_infile):
    """
    loads h5 file
    :param h5file: containing array: 'data_matrix' [batch, frames, markers]
    :return: numpy array: data_matrix [batch, frames, markers]
    """
    input_file = h5py.File(_infile, 'r+')
    # return input_file['data_matrix'].value
    return input_file['container'].value


def split_training_set(_data, _splitpoint=200):
    """
    splits training data into training input and training responce of network
    :param data: array: data_matrix [batch, frames, markers]
    :param splitpoint: sepataion frame number train/test part
    :return: training input for LSTM (X : batch, frames, markers ; Y : batch, concatened frames+markers)
    """
    if _splitpoint < np.size(_data, 1):
        data_X = _data[:, :_splitpoint, :]
        data_Y = _data[:, _splitpoint:, :]
        markers_count = np.size(data_Y, 2)
        frames_count = np.size(data_Y, 1)
        data_Y = np.reshape(data_Y, (-1, frames_count*markers_count))
    else:
        data_X = -1
        data_Y = -1
    return data_X, data_Y


def train(_trainX, _trainY, _outpath, LSTM_kernels=2, epochs_number=2, batch_size=2):
    """
    LSTM training
    :param _trainX: training input
    :param _trainY: training output
    :param _outpath: filepath model to be saved to
    :param _train_params: not functional yet
    :return: history (keras model fit property)
    """
    time = np.size(_trainX, 1)
    features = np.size(_trainX, 2)

    model = Sequential()
    model.add(LSTM(LSTM_kernels, input_shape=(time, features)))
    model.add(Dense(np.size(_trainY, 1)))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.summary()
    _history = model.fit(_trainX, _trainY, epochs=epochs_number, batch_size=batch_size, verbose=2)
    model.save(_outpath)
    _log = ['LSTM ker: %i\n' % LSTM_kernels, 'batch size: %i\n' % batch_size, 'epoch: %i\n' % epochs_number, 'loss: %.6f\n' % _history.history["loss"][-1]]
    return _history, _log


def predict(_model, _input):
    if np.ndim(_input) == 2:
        _input = np.expand_dims(_input, axis=0)

    _batch_size, _, _markers_count = np.shape(_input)
    _prediction_long = _model.predict(_input)
    _prediction = np.reshape(_prediction_long, (_batch_size, -1, _markers_count))
    return _prediction


def load(_model):
    return load_model(_model)