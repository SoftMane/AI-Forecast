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
offset = 8
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



def countingPklSize(data_path):
   train_data, valid_data, test_data = load_data(data_path)
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


#For getting needed y (temperature) values for greater offsets, saw 48 hours instead of 1
#Could probably be combined with above counting function to be more efficient
#Needs the paths to each data file and the desired offset (in hours)
def getYData(train_path,valid_path,test_path,offset):
    train_Y = []
    valid_Y = []
    test_Y = []
    with open(train_path, 'rb') as train:
        for x in range(offset):
            temp = pickle.load(train)
        while True:
            try:
                train_Y.append(pickle.load(train)[3][4])
            except (EOFError):
                break
    with open(valid_path, 'rb') as valid:
        for x in range(offset):
            temp = pickle.load(valid)
        while True:
            try:
                valid_Y.append(pickle.load(valid)[3][4])
            except (EOFError):
                break
    with open(test_path, 'rb') as test:
        for x in range(offset):
            temp = pickle.load(test)
        while True:
            try:
                test_Y.append(pickle.load(test)[3][4])
            except (EOFError):
                break
    return train_Y, valid_Y, test_Y


class KerasBatchGenerator(object):

    def __init__(self, data, y, num_steps, batch_size, file_size, skip_step=1):
        self.data = data
        self.y = y
        self.num_steps = num_steps
        self.batch_size = batch_size
        self.file_size = file_size
        #self.vocabulary = vocabulary
        # this will track the progress of the batches sequentially through the
        # data set - once the data reaches the end of the data set it will reset
        # back to zero
        self.current_idx = 0
        self.current_spot = 0
        # skip_step is the number of words which will be skipped before the next
        # batch is skimmed from the data set
        self.skip_step = skip_step
        #self.file_length = file_length
# add in counter and open file then close after reading in correct amount.
# Check if way to load certain index with pickle stuff

    def generate(self):
        temp_y = []
        while True:
            with open(self.data, 'rb') as f:
                x = np.zeros((self.batch_size+(num_steps-1), 12), dtype=float)
                y2 = np.zeros((self.batch_size, num_steps,1), dtype=float)
                for t in range(self.current_spot):
                    temp = pickle.load(f)
                for i in range(self.batch_size+(num_steps-1)):
                    if self.current_idx + self.num_steps >= len(self.data):
                        # reset the index back to the start of the data set
                        self.current_idx = 0
                    if(i == 0):
                        temp_x = pickle.load(f)
                        temp_x = np.array(temp_x).astype('float64')
                        temp_x = np.delete(temp_x, 3, axis=0) #removes erie data row
                        #temp_x = temp_x.flatten(order='C')
                        #temp_x = np.array(temp_x)
                        #need to make this flexible at some point
                        x[i] = temp_x[0][3],temp_x[1][3],temp_x[2][3],temp_x[0][4], temp_x[1][4], temp_x[2][4], \
                               temp_x[0][5], temp_x[1][5], temp_x[2][5], \
                                  temp_x[0][6], temp_x[1][6], temp_x[2][6]
                        #assign the temp values of the cities that are not erie
                    else:
                        x[i] = temp_y[0][3],temp_y[1][3],temp_y[2][3],temp_y[0][4], temp_y[1][4], temp_y[2][4], \
                               temp_y[0][5], temp_y[1][5], temp_y[2][5], \
                                  temp_y[0][6], temp_y[1][6], temp_y[2][6]
                        #print(x[i])
                    #x[i] = pickle.load(f)# self.data[self.current_idx:self.current_idx + self.num_steps]
                    temp_y = np.array(pickle.load(f), dtype=np.float)#self.data[self.current_idx + 1:self.current_idx + self.num_steps + 1]
                    if i < batch_size: #makes sure this doesn't go out of range
                        for t in range(num_steps):
                            y2[i][t][0] = self.y[i+self.current_spot + t]
                    #y[i] = temp_y[3][4]
                    temp_y = np.delete(temp_y, 3, axis=0) #removes erie data row
                    #temp_y = temp_y.flatten(order='C') #flattens to 1,33
                    #temp_y = np.array(temp_y)
                    #y[i] = temp_y
                    #y[i, :, :] = to_categorical(temp_y, num_classes=self.vocabulary)
                    self.current_idx += self.skip_step
                    self.current_spot += 1
                # x = np.reshape(x, (batch_size,1, 30))
                # y2 = np.reshape(y2, (batch_size,1))
                #this section of code creates the array of 'windows' used as input, needs to be more flexible
                x2 = np.zeros((batch_size,num_steps,12))
                for i in range(batch_size):
                    temp = []
                    for z in range(num_steps):
                        temp.append(x[i+z])
                    x2[i]=temp
                yield x2, y2 #Y NEEDS TO BE 48,4,1 (3 previous then temp trying to predict) But this doesn't make much sense..
            f.close()
            if self.current_spot > (self.file_size-2*(batch_size+(num_steps-1))): #reset if not enough data left for a batch
                self.current_spot = 0
num_steps = 1
batch_size = 96
class RNN():

    def runRNN(self):
        train_data, valid_data, test_data = load_data(data_path)

        train_size, valid_size, test_size = countingPklSize(data_path)

        train_Y, valid_Y, test_Y = getYData(train_data, valid_data, test_data, offset)

        train_data_generator = KerasBatchGenerator(train_data, train_Y, num_steps, batch_size, train_size,
                                                   skip_step=1)
        valid_data_generator = KerasBatchGenerator(valid_data, valid_Y, num_steps, batch_size, valid_size,
                                                   skip_step=1)
        hidden_size = 120
        use_dropout = True
        model = Sequential()
        # model.add(Embedding(8000, embedding_size, input_length=num_steps))
        model.add(LSTM(hidden_size, input_shape=(num_steps, 12), return_sequences=True,
                       kernel_initializer=keras.initializers.VarianceScaling(),
                       recurrent_initializer=keras.initializers.VarianceScaling()))
        model.add(Dropout(.3))
        model.add(LSTM(hidden_size, return_sequences=True, kernel_initializer=keras.initializers.VarianceScaling(),
                       # 'orthogonal'
                       recurrent_initializer=keras.initializers.VarianceScaling(), activation='relu'))
        if use_dropout:
            model.add(Dropout(0.35))
            model.add(Activation('relu'))
        model.add(TimeDistributed(Dense(1)))  # 150 for one hot way?

        # model.add(TimeDistributed(Dense(1))) #150 for one hot way?
        # model.add(Flatten())
        # model.add(Dense(1))
        # try one hot representation instead? use categorical crossentropy, #change y into array with possible temperatures with correct one as 1
        # model.add(Flatten())

        model.compile(loss='mean_absolute_percentage_error', optimizer=tf.keras.optimizers.Adagrad(lr=.01),
                      metrics=['mean_absolute_percentage_error'])

        print(model.summary())
        checkpointer = ModelCheckpoint(filepath=data_path + '/model-{epoch:02d}.hdf5', verbose=1)
        num_epochs = 25
        # removed 8000// from batch_size*num_steps
        model.fit_generator(train_data_generator.generate(), train_size / (batch_size - 2), num_epochs,
                            validation_data=valid_data_generator.generate(),
                            validation_steps=valid_size / (batch_size - 2), callbacks=[checkpointer])

        model = load_model(data_path + "/model-25.hdf5")
        dummy_iters = 40
        example_training_generator = KerasBatchGenerator(valid_data, valid_Y, num_steps, batch_size, valid_size,
                                                         skip_step=1)
        print("Training data:")
        for i in range(dummy_iters):
            dummy = next(example_training_generator.generate())
        num_predict = 10

        for i in range(num_predict):
            data, y = next(example_training_generator.generate())
            # print(y.shape)
            # print(data[i])
            test = data[i]
            test = np.reshape(test, (1, num_steps, 12))
            prediction = model.predict(test)
            # test = np.reshape(data[0][i+1], (1,1,33))
            # print(test)
            print("Actual: " + str(((y[i] * (323.0 - 244.0) + 244.0) - 273.15) * (9.0 / 5.0) + 32.0))  # converts data to f
            print("Prediction: " + str(((prediction * (323.0 - 244.0) + 244.0) - 273.15) * (9.0 / 5.0) + 32.0))
            # predict_word = np.argmax(prediction[:, 24-1, :]) #24 was num_steps

        # test data set
        dummy_iters = 40
        example_test_generator = KerasBatchGenerator(test_data, test_Y, num_steps, batch_size, test_size,
                                                     skip_step=1)
        print("Test data:")
        for i in range(dummy_iters):
            dummy = next(example_test_generator.generate())
        num_predict = 10

        for i in range(num_predict):
            data, y = next(example_test_generator.generate())
            # print(y.shape)
            # print(data[i])
            test = data[i]
            test = np.reshape(test, (1, num_steps, 12))
            prediction = model.predict(test)
            # test = np.reshape(data[0][i+1], (1,1,33))

            print("Actual: " + str(((y[i] * (323.0 - 244.0) + 244.0) - 273.15) * (9.0 / 5.0) + 32.0))  # converts data to f
            print("Prediction: " + str(((prediction * (323.0 - 244.0) + 244.0) - 273.15) * (9.0 / 5.0) + 32.0))
