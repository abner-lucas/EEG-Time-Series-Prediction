from sklearn.preprocessing import MinMaxScaler
import numpy as np
from src.compile_data import *
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
import tensorflow as tf

def data_norm(data, v_min, v_max):
    # data = np.reshape(data, (v_min, 1))
    norm = MinMaxScaler(feature_range=(v_min, v_max))
    return norm.fit_transform(data)
    
    # mini = min(data)
    # maxi = max(data)
    # return (data - mini)/(maxi - mini)


def split_sequence(data, n_steps):
    x, y = list(), list()
    # Tipo A
    for i in range(len(data)):
        seq_x, seq_y = data[i][:-1], data[i][-1]
        x.append(seq_x)
        y.append(seq_y)

    #  Tipo B
    # for i in range(len(data)):
    #     end_ix = i + n_steps
    #     if (end_ix > len(data)-1): break
    #     seq_x, seq_y = data[i:end_ix], data[end_ix]
    #     x.append(seq_x)
    #     y.append(seq_y)

    # Tipo C
    # p = 5
    # df1 = df[['col']].copy()
    # for i in range(p):
    #   df1[f'x_{i + 1}'] = df1.col.shift(i + 1)
    # df1.dropna(axis=0, inplace=True)
    # df1.head()
    return np.array(x), np.array(y)

def train_test_split(df, val_size, test_size):
    val_size = int(len(df['subject_id'].unique()) * (val_size))
    s_validation = random.choices(df['subject_id'].unique(), k=val_size)
    
    test_size = int(len(df['subject_id'].unique()) * (test_size))
    s_test = random.choices(df['subject_id'].unique(), k=test_size)

    means= mean_sensors(df, s_test)
    means_ = np.concatenate([means for _ in range(len(df['subject_id'].unique()))])
    df['mean'] = means_

    subjects_validation = df[df['subject_id'].isin(s_validation)].reset_index(drop=True)
    subjects_validation.drop(columns=['subject_id', 'group', 'time'], inplace=True)
    #subjects_test['mean'] = subjects_test[subjects_test.columns[:]].mean(axis=1)

    subjects_test = df[df['subject_id'].isin(s_test)].reset_index(drop=True)
    subjects_test.drop(columns=['subject_id', 'group', 'time'], inplace=True)
    #subjects_test['mean'] = subjects_test[subjects_test.columns[:]].mean(axis=1)

    subjects_train = df[~df['subject_id'].isin(s_test) & ~df['subject_id'].isin(s_validation)].reset_index(drop=True)
    subjects_train.drop(columns=['subject_id', 'group', 'time'], inplace=True)
    #subjects_train['mean'] = subjects_train[subjects_train.columns[:]].mean(axis=1)

    return subjects_train, subjects_validation, subjects_test, means

def MLP(n_features, n_neurons, kernel_initializer, activation, func_loss, optimizer, metrics):
    model = Sequential()
    model.add(Dense(n_neurons, input_dim=n_features, kernel_initializer=kernel_initializer,
                    activation=activation))
    model.add(Dropout(0.2))
    model.add(Dense(n_neurons, kernel_initializer=kernel_initializer, activation=activation))
    model.add(Dense(1))
    model.compile(loss=func_loss, optimizer=optimizer, metrics=metrics)
    return model

def build_model(hp):
    # Tune the learning rate for the optimizer
    # Choose an optimal value from 0.01, 0.001, or 0.0001
    hp_learning_rate = hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])

    # Tune the optimizer
    
    hp_optimizer = hp.Choice('optimizer', values=['adam', 'sgd', 'adagrad', 'rmsprop'])
    if hp_optimizer == 'adam':
        hp_optimizer = tf.keras.optimizers.Adam(learning_rate=hp_learning_rate)
    elif hp_optimizer == 'sgd':
        hp_optimizer = tf.keras.optimizers.SGD(learning_rate=hp_learning_rate)

    hp_net_depth = hp.Int('net_depth', min_value = 2, max_value = 6)


    # Tune the number of units in the first Dense layer
    # Choose an optimal value between 9-54
    hp_units = []
    for i in range(hp_net_depth):
        hp_units.append(hp.Int('units'+str(i), min_value=9, max_value=54, step=9))

    # Tune kernel_initializer
    hp_kernel_init= hp.Choice('kernel_init', values=['random_normal', 'uniform', 'random_uniform'])

    hp_activation = hp.Choice('activation', values=['relu','sigmoid', 'linear', 'softmax'])
    hp_activation_out = hp.Choice('activation_out', values=['relu','sigmoid', 'linear', 'softmax'])

    model = Sequential()
    for i in range(hp_net_depth):
        model.add(Dense(units=hp_units[i], activation=hp_activation, kernel_initializer=hp_kernel_init))
        if i == hp_net_depth-1:
            model.add(Dense(1, activation=hp_activation_out, kernel_initializer=hp_kernel_init))
    model.compile(optimizer = hp_optimizer, loss = 'mse', metrics=['mse'])

    return model