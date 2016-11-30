![header](tarot_header.jpg)
# tarot-nlp
Following a thread: low-complexity experiments revolving around the Major Arcana and Text Classification

Contents
--------
* tarot_scraper: 
	Get raw data from web, perform simple sainification stuff.
* tarot_stats: 
	Perform basic stats on data
* bayes_classify:
	Classification using a naive bayes classifier from NLTK
* dist_bayes:
	Different approach than bayes_classify- trains one binary bayes classifier for each card, 
	computes likelihood for each card and uses softmax to select prediction. ~2x improvement 

TODO
----
* More Data, always. 
* Experiment with LTSM & other DL classification techniques. 
* Improve data structure (currently uses a dir of txt files. no bueno.)
* Improve Code structure- DRY stuff. 
