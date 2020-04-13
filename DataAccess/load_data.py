data_path='/Users/tigergoodbread/PycharmProjects/AI-Forecast/GUI.py'
class load_data_class():

   def load_data(self,data_path):
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

       full_train_path = data_path+train_path
       full_valid_path = data_path+valid_path
       full_test_path = data_path+test_path
       return full_train_path, full_valid_path, full_test_path
#train_data, valid_data, test_data = load_data(data_path)

   def countingPklSize(self,full_train_path,full_valid_path,full_test_path):

       trainSize = 0
       validSize = 0
       testSize = 0

       with open(full_train_path, 'rb') as f1:
           while True:
               try:
                   temp = pickle.load(f1)
               except (EOFError):
                   break
               trainSize = trainSize+1
       f1.close()

       with open(full_valid_path, 'rb') as f2:
           while True:
               try:
                   temp = pickle.load(f2)
               except (EOFError):
                   break
               validSize = validSize + 1
       f2.close()

       with open(full_test_path, 'rb') as f3:
           while True:
               try:
                   temp = pickle.load(f3)
               except (EOFError):
                   break
               testSize = testSize + 1
       f3.close()

       return trainSize, validSize, testSize

   #offset = 4

   def getYData(train_path, valid_path, test_path, offset):
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

   #train_Y, valid_Y, test_Y = getYData(train_data, valid_data, test_data, offset)

