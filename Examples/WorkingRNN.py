import collections
import os
import urllib.request
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Activation, Embedding, Dropout, TimeDistributed, Flatten, Reshape
from tensorflow.keras.layers import LSTM
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint
import numpy as np
import pickle
import decimal


#tf.compat.v1.disable_eager_execution()
data_path = 'C:/Users/Rohg/PycharmProjects/AI-Forecast/DataAccess/'

# def read_words(filename):
#     with tf.io.gfile.GFile(filename, "rb") as f:
#         return f.read().decode("utf-8").replace("\n", "<eos>").split()
#
#
# def build_vocab(filename):
#     data = read_words(filename)
#
#     counter = collections.Counter(data)
#     count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
#
#     words, _ = list(zip(*count_pairs))
#     word_to_id = dict(zip(words, range(len(words))))
#
#     return word_to_id


# def file_to_word_ids(filename, word_to_id):
#     data = read_words(filename)
#     return [word_to_id[word] for word in data if word in word_to_id]


def load_data(data_path):
    # get the data paths
    train_path = "training.pkl"
    valid_path = "validation.pkl"
    test_path = "testing.pkl"

    # build the complete vocabulary, then convert text data to list of integers
    # word_to_id = build_vocab(train_path)
    # train_data = file_to_word_ids(train_path, word_to_id)
    # valid_data = file_to_word_ids(valid_path, word_to_id)
    # test_data = file_to_word_ids(test_path, word_to_id)
    # vocabulary = len(word_to_id)
    #reversed_dictionary = dict(zip(word_to_id.values(), word_to_id.keys()))

    # print(train_data[:5])
    # print(word_to_id)
    # print(vocabulary)
    # print(" ".join([reversed_dictionary[x] for x in train_data[:10]]))
    return data_path+train_path, data_path+valid_path, data_path+test_path

train_data, valid_data, test_data = load_data(data_path)

def countingPklSize(data_path):
   train_path = train_data
   valid_path = valid_data
   test_path = test_data

   trainSize = 0
   validSize = 0
   testSize = 0

   with open(train_path, 'rb') as f1:
       while True:
           try:
               temp = pickle.load(f1)
           except (EOFError):
               break
           trainSize = trainSize+1
   f1.close()

   with open(valid_path, 'rb') as f2:
       while True:
           try:
               temp = pickle.load(f2)
           except (EOFError):
               break
           validSize = validSize + 1
   f2.close()

   with open(test_path, 'rb') as f3:
       while True:
           try:
               temp = pickle.load(f3)
           except (EOFError):
               break
           testSize = testSize + 1
   f3.close()
   return trainSize, validSize, testSize

train_size, valid_size, test_size = countingPklSize(data_path)

#For getting needed y (temperature) values for greater offsets, saw 48 hours instead of 1
#Could probably be combined with above counting function to be more efficient
#Needs the paths to each data file and the desired offset (in hours)
def getYData(train_path,valid_path,test_path,offset):
    train_Y = []
    valid_Y = []
    test_Y = []
    with open(train_path) as train:
        for x in range(offset):
            pickle.load(train)
        while True:
            try:
                train_Y.append(pickle.load(train)[3][4])
            except (EOFError):
                break
    with open(valid_path) as valid:
        for x in range(offset):
            pickle.load(valid)
        while True:
            try:
                valid_Y.append(pickle.load(valid)[3][4])
            except (EOFError):
                break
    with open(test_path) as test:
        for x in range(offset):
            pickle.load(test)
        while True:
            try:
                test_Y.append(pickle.load(test)[3][4])
            except (EOFError):
                break


class KerasBatchGenerator(object):

    def __init__(self, data, num_steps, batch_size, file_size, skip_step=1):
        self.data = data
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.file_size = file_size
        #self.vocabulary = vocabulary
        # this will track the progress of the batches sequentially through the
        # data set - once the data reaches the end of the data set it will reset
        # back to zero
        self.current_idx = 0
        # skip_step is the number of words which will be skipped before the next
        # batch is skimmed from the data set
        self.skip_step = skip_step
        #self.file_length = file_length
# add in counter and open file then close after reading in correct amount.
# Check if way to load certain index with pickle stuff
    def generate(self):
        current_spot = 0
        temp_y = []
        while True:
            with open(self.data, 'rb') as f:
                x = np.zeros((self.batch_size, self.num_steps), dtype=float)
                y = np.zeros((self.batch_size), dtype=float)
                for t in range(current_spot):
                    temp = pickle.load(f)
                for i in range(self.batch_size):
                    if self.current_idx + self.num_steps >= len(self.data):
                        # reset the index back to the start of the data set
                        self.current_idx = 0
                    if(i == 0):
                        temp_x = pickle.load(f)
                        temp_x = np.array(temp_x).astype('float64')
                        temp_x = np.delete(temp_x, 3, axis=0) #removes erie data row
                        temp_x = temp_x.flatten(order='C')
                        temp_x = np.array(temp_x)

                        x[i] = temp_x #np.array(pickle.load(f)) #use temp object to hold this as np.array(pickle.load(f)) then assign to x[i]
                    else:
                        x[i] = temp_y
                        #print(x[i])
                    #x[i] = pickle.load(f)# self.data[self.current_idx:self.current_idx + self.num_steps]
                    temp_y = np.array(pickle.load(f), dtype=np.float)#self.data[self.current_idx + 1:self.current_idx + self.num_steps + 1]
                    y[i] = temp_y[3][4]
                    temp_y = np.delete(temp_y, 3, axis=0) #removes erie data row
                    temp_y = temp_y.flatten(order='C') #flattens to 1,33
                    temp_y = np.array(temp_y)
                    # # convert all of temp_y into a one hot representation
                    #y[i] = temp_y
                    #y[i, :, :] = to_categorical(temp_y, num_classes=self.vocabulary)
                    self.current_idx += self.skip_step
                    current_spot += 1
                x = np.reshape(x, (batch_size,1, 30))
                y = np.reshape(y, (batch_size,1))
                yield x, y
            f.close()
            if current_spot > self.file_size-batch_size:
                current_spot = 0

num_steps = 30
batch_size = 50
train_data_generator = KerasBatchGenerator(train_data, num_steps, batch_size, train_size,
                                           skip_step=1)
valid_data_generator = KerasBatchGenerator(valid_data, num_steps, batch_size, valid_size,
                                           skip_step=1)

embedding_size = 500
hidden_size = 30
use_dropout=True
model = Sequential()
#model.add(Embedding(8000, embedding_size, input_length=num_steps))
model.add(LSTM(hidden_size, input_shape=(1, 30), return_sequences=True, kernel_initializer=keras.initializers.VarianceScaling(),
              recurrent_initializer=keras.initializers.VarianceScaling()))
model.add(LSTM(hidden_size, return_sequences=True, kernel_initializer=keras.initializers.VarianceScaling(),
              recurrent_initializer=keras.initializers.VarianceScaling()))
model.add(TimeDistributed(Dense(30))) #150 for one hot way?
if use_dropout:
    model.add(Dropout(0.2))
#try one hot representation instead? use categorical crossentropy, #change y into array with possible temperatures with correct one as 1
#model.add(Flatten())
model.add(Activation('relu'))
model.add(Dense(1))
#model.add(Activation('sigmoid')) #maybe change activation function to help get one value? idk. this is why prediction is always 1 right now(old)
model.compile(loss='mean_absolute_error', optimizer=tf.keras.optimizers.Adagrad(lr=.03), metrics=['mean_absolute_percentage_error'])

print(model.summary())
checkpointer = ModelCheckpoint(filepath=data_path + '/model-{epoch:02d}.hdf5', verbose=1)
num_epochs = 5
#removed 8000// from batch_size*num_steps
model.fit_generator(train_data_generator.generate(), train_size/batch_size, num_epochs, #8000 was len(train_Data), //(batch_size*num_steps)
                        validation_data=valid_data_generator.generate(),
                        validation_steps=valid_size/batch_size, callbacks=[checkpointer]) #8000 was len(valid_data), //(batch_size*num_steps) m

model = load_model(data_path + "/model-05.hdf5")
dummy_iters = 40
example_training_generator = KerasBatchGenerator(train_data, num_steps, batch_size, train_size,
                                                  skip_step=1)
print("Training data:")
for i in range(dummy_iters):
    dummy = next(example_training_generator.generate())
num_predict = 10

for i in range(num_predict):
    data, y = next(example_training_generator.generate())
    #print(y.shape)
    #print(data[i])
    test = np.reshape(data[i],(1,1,30))
    prediction = model.predict(test)
    # test = np.reshape(data[0][i+1], (1,1,33))
    # print(test)
    print("Actual: " + str(((y[i][0]*323.0)-273.15)*(9.0/5.0)+32.0)) #converts data to f
    print("Prediction: " + str(((prediction*323.0)-273.15)*(9.0/5.0)+32.0))
    #predict_word = np.argmax(prediction[:, 24-1, :]) #24 was num_steps

# test data set
dummy_iters = 40
example_test_generator = KerasBatchGenerator(test_data, num_steps, batch_size, test_size,
                                                 skip_step=1)
print("Test data:")
for i in range(dummy_iters):
    dummy = next(example_test_generator.generate())
num_predict = 10

for i in range(num_predict):
    data, y = next(example_test_generator.generate())
    #print(y.shape)
    # print(data[i])
    test = np.reshape(data[i], (1, 1, 30))

    prediction = model.predict(test)
    # test = np.reshape(data[0][i+1], (1,1,33))
    # print(test)
    print("Actual: " + str(((y[i][0] * 323.0) - 273.15) * (9.0 / 5.0) + 32.0))  # converts data to f
    print("Prediction: " + str(((prediction * 323.0) - 273.15) * (9.0 / 5.0) + 32.0))
