import pandas
import re
import sys
import pickle
import time
from textblob.classifiers import NaiveBayesClassifier
import itertools
import numpy as np
import random as ra
import atexit



# def clean(text):
#     return re.sub(r'http\S+', '', text)
#
#
# def polarity_checker(number):
#     if number == 0:
#         return "neg"
#     elif number == 4:
#         return "pos"
#
#
# read = pandas.read_csv("trainingset.csv", encoding='latin-1', names=["value", "id", "date", "query", "name", "tweet"])
#
# full_data = []
# start_time = time.time()
# for i in range(read["value"].count()):
#     tweet = clean(read["tweet"][i])
#     polarity = polarity_checker(read["value"][i])
#     full_data.append((tweet, polarity))
#     percent_done = (i/read["value"].count()) * 100
#     b = "done {} out of {}. ".format(i, read["value"].count()) + str(percent_done) + "% done!"
#     sys.stdout.write('\r'+b)
#
# print("\nGetting the data took {} seconds!".format(time.time()-start_time))

with open("shuffledlist.pickle", 'rb') as f:
    full_data = pickle.load(f)

training_data = (tweet for tweet in full_data[:1500000])
#test_data = full_data[1500000:]


try:
    with open("sentimentclassifier.pickle", "rb") as file:
        classifier = pickle.load(file)
        print("Got existing classifier")
except EOFError:
    classifier = NaiveBayesClassifier(full_data[:1000])
    print("Made new classifier")
del full_data

feeding_size = 1000
left_splice = 11000
right_splice = feeding_size + left_splice

count = 0
new_start_time = time.time()
past_times = 0

while right_splice < 1500000:
    loop_time = time.time()
    data = itertools.islice(training_data,left_splice,right_splice)
    try:
        classifier.update(data)
    except Exception:
        print("Houston we got a problem")
        with open("sentimentclassifier.pickle", "wb") as sentiment:
             pickle.dump(classifier, sentiment)
        sys.exit("Yo it ended at {} and {}".format(left_splice, right_splice))
    past_times += time.time() - loop_time
    count += 1
    string = "Left: {} Right: {}. Took {} seconds. Total Time Elapsed: {}. Average Time for each: {}. Count: {}."\
        .format(left_splice, right_splice, time.time()-loop_time, time.time() - new_start_time, past_times/count, count)
    sys.stdout.write('\r' + string)
    left_splice += feeding_size
    right_splice += feeding_size
    with open("sentimentclassifier.pickle", "wb") as sentiment:
        pickle.dump(classifier, sentiment)
        print("Done dumping cycle {}!".format(count))

print("Done! Right: {}, Left: {}!".format(left_splice, right_splice))

with open("sentimentclassifier.pickle", "wb") as sentiment:
    pickle.dump(classifier, sentiment)


print("Training took {} seconds!".format(time.time()-new_start_time))
