#!./env/bin/python3
# coding=utf-8

import sys

if len(sys.argv) != 2:
    print("Usage:\n\t./train.py train_data.txt")
    print("Train format:\n\tY0 [tab] X0 [tab] X1 [tab] ... Xn")
    sys.exit(0)

import vocabulary as voc
voc.init()

import numpy as np

from keras.preprocessing import sequence
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.callbacks import ModelCheckpoint

print("Params:")
print(sys.argv)

x_train = []
y_train = []

samples_max = 100000
samples     = 0
train = sys.argv[1]
for l in open(train, "r"):
    d = l.split("\t")

    y = int(d[0]) 
    x = [int(x) for x in d[1:]]
    if y!=0 and y!=1 or len(x)==0:
        print(l) 
        continue
    
    x_train.append(x)
    y_train.append(y)
    
    if samples > samples_max: break
    samples += 1
    
x_train = np.array(x_train)
y_train = np.array(y_train)

print("Loading {} cases from '{}' complete".format(len(x_train), train))

# vocabulary size
max_features = 70000

# words in sequence
maxlen     = 100
batch_size = 32

print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)

print("x_train shape:", x_train.shape)
print("y_train shape:", y_train.shape)

model = Sequential()
model.add(Embedding(max_features, 128, input_length=maxlen))
model.add(LSTM(128, return_sequences=True))
model.add(LSTM(128))
model.add(Dropout(0.5))
#model.add(LSTM(128, dropout_W=0.2, dropout_U=0.2))  # try using a GRU 
model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              #class_mode="binary"
              metrics=['accuracy'])
              
checkpointer = ModelCheckpoint(filepath="out/checkpoint.{epoch:02d}.h5", verbose=1)
model.fit(
    x_train, y_train, 
    batch_size=batch_size, 
    nb_epoch=10,
    verbose=1,
    shuffle=True,
    callbacks=[checkpointer]
)

print("Save model")
model.save("out/final.h5")
