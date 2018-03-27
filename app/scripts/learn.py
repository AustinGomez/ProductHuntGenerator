from __future__ import print_function

import argparse

from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential, model_from_json
from tensorflow.python.client import device_lib

from app.scripts.utils import *

print(device_lib.list_local_devices())

# Parsing arguments for Network definition
ap = argparse.ArgumentParser()
ap.add_argument('-data_dir', default='./services/producthunt.txt')
ap.add_argument('-batch_size', type=int, default=50)
ap.add_argument('-layer_num', type=int, default=2)
ap.add_argument('-seq_length', type=int, default=50)
ap.add_argument('-hidden_dim', type=int, default=500)
ap.add_argument('-generate_length', type=int, default=500)
ap.add_argument('-nb_epoch', type=int, default=20)
ap.add_argument('-mode', default='train')
ap.add_argument('-weights', default='')
args = vars(ap.parse_args())

DATA_DIR = args['data_dir']
BATCH_SIZE = args['batch_size']
HIDDEN_DIM = args['hidden_dim']
SEQ_LENGTH = args['seq_length']
WEIGHTS = args['weights']
GENERATE_LENGTH = args['generate_length']
LAYER_NUM = args['layer_num']

# Creating training data
X, y, VOCAB_SIZE, ix_to_char = load_data(DATA_DIR, SEQ_LENGTH)

# Either load the model or create it.
if WEIGHTS != '':
    # Loading the trained weights
    print('Loading model')
    json_file = open('model.json', 'r', encoding='utf-8')
    model_json = json_file.read()
    json_file.close()
    model = model_from_json(model_json)
    model.load_weights(WEIGHTS)
    print("Loaded model from disk")
else:
    model = Sequential()
    model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
    for i in range(LAYER_NUM - 1):
        model.add(Dropout(0.2))
        model.add(LSTM(HIDDEN_DIM, return_sequences=True))
    model.add(TimeDistributed(Dense(VOCAB_SIZE)))
    model.add(Activation('softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

if args['mode'] == 'generate':
    generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)

nb_epoch = 0

# Training if there is no trained weights specified
if args['mode'] == 'train' or WEIGHTS == '':
    while True:
        print('\n\nEpoch: {}\n'.format(nb_epoch))
        model.fit(X, y, batch_size=BATCH_SIZE, verbose=1, epochs=1)
        nb_epoch += 1
        if nb_epoch % 5 == 0:
            generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
        if nb_epoch % 10 == 0:
            # serialize model to JSON
            model_json = model.to_json()
            with open("model.json", "w") as json_file:
                json_file.write(model_json)
            model.save_weights('checkpoint_layer_{}_hidden_{}_epoch_{}.hdf5'.format(LAYER_NUM, HIDDEN_DIM, nb_epoch))
