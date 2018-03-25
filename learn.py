import numpy
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils


filename = "producthunt.txt"
raw_text = open(filename).read().lower().replace('\n', ' ')
print(raw_text)

# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
total_characters = len(raw_text)
total_vocab = len(chars)
print("Total vocabulary: ", total_vocab)

sequence_length = 100
dataX, dataY = [], []
for i in range(0, total_characters - sequence_length, 1):
    sequence_in = raw_text[i:i + sequence_length]
    sequence_out = raw_text[i + sequence_length]
    dataX.append([char_to_int[char] for char in sequence_in])
    dataY.append(char_to_int[sequence_out])
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)

X = numpy.reshape(dataX, (n_patterns, sequence_length, 1))
X = X / float(total_vocab)
y = np_utils.to_categorical(dataY)

# Model definition.
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(256))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')

# Checkpoint definition
filepath = "{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

# fit the model
model.fit(X, y, epochs=50, batch_size=64, callbacks=callbacks_list)


