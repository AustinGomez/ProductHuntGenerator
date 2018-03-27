from __future__ import print_function
import numpy as np


# method for generating text
def generate_text(model, length, vocab_size, ix_to_char, seed=None):
    # starting with random character
    print("Generating...")
    if seed:
        char_to_ix = {char: ix for ix, char in ix_to_char.items()}
        ix = [char_to_ix[char] for char in seed]
        y_char = [char for char in seed]
    else:
        ix = [np.random.randint(vocab_size / 3)]
        y_char = [ix_to_char[ix[-1]]]
    X = np.zeros((1, 1000000, vocab_size))
    cur_len = 0
    i=0
    while cur_len < length:
        # appending the last predicted character to sequence
        X[0, i, :][ix[-1]] = 1
        text = ix_to_char[ix[-1]]
        # print(text, end="")
        ix = np.argmax(model.predict(X[:, :i + 1, :])[0], 1)
        char = ix_to_char[ix[-1]]
        y_char.append(char)
        i += 1
        if char == '\n':
            cur_len += 1
            print("Generated " + str(cur_len))

    x = ''.join(y_char).split('\n')
    if seed:
        x = seed + ''.join(y_char).split('\n')[0]
    names = [s for s in x if ("Startup Chat" not in s and ':' in s and len(s) > 10)]
    return names


# method for preparing the training data
def load_data(data_dir, seq_length):
    data = open(data_dir, 'r', encoding="utf8").read()
    chars = sorted(list(set(data)))
    VOCAB_SIZE = len(chars)

    print('Data length: {} characters'.format(len(data)))
    print('Vocabulary size: {} characters'.format(VOCAB_SIZE))

    ix_to_char = {ix: char for ix, char in enumerate(chars)}
    char_to_ix = {char: ix for ix, char in enumerate(chars)}

    X = np.zeros((int(len(data) / seq_length), seq_length, VOCAB_SIZE))
    y = np.zeros((int(len(data) / seq_length), seq_length, VOCAB_SIZE))
    for i in range(0, int(len(data) / seq_length)):
        X_sequence = data[i * seq_length:(i + 1) * seq_length]
        X_sequence_ix = [char_to_ix[value] for value in X_sequence]
        input_sequence = np.zeros((seq_length, VOCAB_SIZE))
        for j in range(seq_length):
            input_sequence[j][X_sequence_ix[j]] = 1.
            X[i] = input_sequence

        y_sequence = data[i * seq_length + 1:(i + 1) * seq_length + 1]
        y_sequence_ix = [char_to_ix[value] for value in y_sequence]
        target_sequence = np.zeros((seq_length, VOCAB_SIZE))
        for j in range(seq_length):
            target_sequence[j][y_sequence_ix[j]] = 1.
            y[i] = target_sequence
    return X, y, VOCAB_SIZE, ix_to_char
