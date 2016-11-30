#classify tarot w/naive bayes. 
#pgulley

import nltk
import random

rw_cards = [
		"fool", "magician", "high priestess", "empress", "emperor", "hierophant","lovers",
		"chariot", "strength","hermit", "wheel of fortune", "justice", "hanged man", "death", 
		"temperance", "devil", "tower", "star", "moon", "sun", "judgement", "world"]

def mean(list_of_ints):
	tot = sum(list_of_ints)
	return tot/len(list_of_ints)

def extract_features(post):
	features = {}
	for word in nltk.word_tokenize(post):
		features['contains({})'.format(word.lower())] = True
	return features

def process_files():
	all_lines = []
	for card in rw_cards:
		o_ = open("{0}_clean.txt".format(card.replace(" ","_")))
		lines = o_.readlines()
		o_.close()
		for line in lines:
			all_lines.append((extract_features(line), card))
	random.shuffle(all_lines)
	return all_lines

def main(num_tests, training_mult, v=False):
	results = []
	all_fposts = process_files()
	for i in range(num_tests): 
		fposts = list(all_fposts)
		random.shuffle(fposts)
		test_size = int(len(fposts) * 0.1)
		train_set, test_set = fposts[test_size:]*training_mult, fposts[:test_size] 
		classifier = nltk.NaiveBayesClassifier.train(train_set)
		results.append(nltk.classify.accuracy(classifier, test_set))
	stats = (min(results), max(results), mean(results))
	if v:
		print("Accuracy | min: {}, max: {}, mean: {}".format(*stats))
	return stats

if __name__ == "__main__":
	main(num_tests=10, training_mult=5, v=True)

"""
Accuracy | min: 0.39872068230277186, max: 0.4562899786780384, mean: 0.4228144989339019
LOL should not be surprised at these numbers but eeeek 
also a decent amount of this  is going to be because of the names occuring IN the lines. 
gosh. 

"""


