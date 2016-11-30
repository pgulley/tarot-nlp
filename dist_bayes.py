#Bayes Distribution Classifier
#One classifier per class- each is just a binary classifier. 

import nltk
import random

rw_cards = [ card.replace(" ", "_") for card in [
		"fool", "magician", "high priestess", "empress", "emperor", "hierophant","lovers",
		"chariot", "strength","hermit", "wheel of fortune", "justice", "hanged man", "death", 
		"temperance", "devil", "tower", "star", "moon", "sun", "judgement", "world"]]

import numpy

#This will make things nicer
def softmax(x):
    """Compute softmax values for each sets of scores in x."""
    return numpy.exp(x) / numpy.sum(numpy.exp(x), axis=0)

def mean(list_of_ints):
	tot = sum(list_of_ints)
	return tot/len(list_of_ints)

def extract_features(sent, as_list=False):
	features = {}
	if as_list:
		for word in sent:
			features['contains({})'.format(word.lower())] = True
	else:
		for word in nltk.word_tokenize(sent):
			features['contains({})'.format(word.lower())] = True
	return features


def data_prep():
	final_data = {}

	brown_sents = list(nltk.corpus.brown.sents())
	random.shuffle(brown_sents)
	
	for card in rw_cards:
		o_ = open("{0}_clean.txt".format(card))
		t_lines = o_.readlines()
		o_.close()

		datum_card = [{
						"features":(extract_features(t_lines[i]), card), 
						"source":card} 
						for i in range(len(t_lines))]
		
		#get some non-tarot tests in there. Maybe will fux things up but #whoknows
		datum_non_card = [{
						"features":(extract_features(brown_sents.pop(), as_list=True), "other"), 
						"source":"other"} 
						for i in range(len(t_lines))]
		
		final_data[card] = datum_card + datum_non_card
	return final_data #{card-name:data-set}

def probdist_str(pb):
	return "<ProbDist | {}>".format(pb._prob_dict)

def prob_dist(sent, classifiers):
	probs = softmax([classifiers[card].prob_classify(sent).prob(card) for card in rw_cards])
	return dict(zip(rw_cards, probs))
	
#There's a better way to have organized this data. 

def exp(data, training_mult = 5, meta_test_size = 10, v = False):
	#Train
	print("\nTraining Classifiers")
	classifiers = {}
	for card_name in rw_cards:
		card = data[card_name]
		random.shuffle(card)
		test_size = int(len(card) * 0.1)
		train_set = [c["features"] for c in card[test_size:]*training_mult]
		test_set = [c["features"]  for c in card[:test_size]]
		NBC = nltk.NaiveBayesClassifier.train(train_set)
		if v:
			print("Accuracy for {} | {}".format(card_name, nltk.classify.accuracy(NBC, test_set)))
		classifiers[card_name] = NBC
		#{card:nbc}
	#Test
	print("\nTesting Classifiers")
	meta_test = [item["features"] for sublist in data.values() for item in sublist if item["source"] != "other"]
	random.shuffle(meta_test)
	accuracy = []
	for test_sent in meta_test[:meta_test_size]:
		card = test_sent[1]
		stats = prob_dist(test_sent[0], classifiers)
		max_ = max(stats, key=lambda key: stats[key])
		correct = max_==card
		accuracy.append(correct)
		if v:
			print("--------------------")
			print("Ground Truth Card: {}".format(card))
			print("Prediction: {} | Correct: {}".format(max_, correct))
			print("Stats: {}".format(stats))

	percent_correct = len([i for i in accuracy if i == True]) / len(accuracy)

	print("Percent Correct: {}".format(percent_correct))
	return classifiers, percent_correct


def main():
	data = data_prep()
	a_tal = []
	for i in range(100):
		_, correct = exp(data, meta_test_size=100, v=False)
		a_tal.append(correct)
	stats = (min(a_tal), max(a_tal), mean(a_tal))
	print("Accuracy | min: {}, max: {}, mean: {}".format(*stats))


if __name__ == "__main__":
	main()
	#HEYYY CHECK IT! We're at baseline 77% which, well, is decent compared to baseline 40% from the pure-bayes approach. 
	#Accuracy | min: 0.6, max: 0.81, mean: 0.7088000000000002