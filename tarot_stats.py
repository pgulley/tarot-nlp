#Tarot NLP Basic stats 
#req python3
import nltk
data_dir = "data"

rw_cards = [
		"fool", "magician", "high priestess", "empress", "emperor", "hierophant","lovers",
		"chariot", "strength","hermit", "wheel of fortune", "justice", "hanged man", "death", 
		"temperance", "devil", "tower", "star", "moon", "sun", "judgement", "world"]

all_files = ["".join(open("{}/{}_clean.txt".format(data_dir, name.replace(" ","_")),"r").readlines()) for name in rw_cards]

all_files_concat = "".join(all_files)
master_vocab = sorted(
	set(
		[word.lower() for word in nltk.Text(nltk.word_tokenize(all_files_concat))]
		)
	)

def process_raw(raw):
	tokens = nltk.word_tokenize("".join(raw))
	txt = nltk.Text(tokens)
	words = [word.lower() for word in txt]
	fdist = nltk.FreqDist(words)
	return fdist

#Generate distribution for full corpus text. 
all_lines = "".join([line for f in all_files for line in f])

stats = {}
names_copy = list(rw_cards)
stats["all"] = process_raw(all_lines)

for f in all_files:
	f_name = names_copy.pop(0)
	f_len = len(f)
	f_stat = process_raw(f)
	corpus_fdist = {}
	for word in master_vocab:
		if word in f_stat:
			corpus_fdist[word] = f_stat[word] / f_len
		else:
			corpus_fdist[word] = 0
	stats[f_name] = corpus_fdist

#This is a null tokens list. Stopwords, punctuation, etc.
stopwords = nltk.corpus.stopwords.words('english')+list("!@#$%^&*()_+-=,./?`:'")+["''", "``","...", "n't", "'s"]

#top words
for stat in stats.items():
	not_stop = [word_pair for word_pair in stat[1].items() if word_pair[0] not in stopwords]
	top = sorted(not_stop, key=lambda k:k[1], reverse=True)
	print("{0} : {1}".format(stat[0],[wrd[0] for wrd in top[0:20]]))

#top bigrams?


