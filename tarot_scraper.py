import urllib2
from bs4 import BeautifulSoup as bs4

#Because there are no "standard" card sets
data_dir = "data"

rw_cards = [
		"fool", "magician", "high priestess", "empress", "emperor", "hierophant","lovers",
		"chariot", "strength","hermit", "wheel of fortune", "justice", "hanged man", "death", 
		"temperance", "devil", "tower", "star", "moon", "sun", "judgement", "world"]

rw_cards_alt = [
		"fool", "magician", "high priestess", "empress", "emperor", "hierophant","lovers",
		"chariot", "strength","hermit", "wheel of fortune", "justice", "hanged man", "death", 
		"temperance", "devil", "tower", "star", "moon", "sun", "judgment", "world"]

rw_cards_the = [
		"the fool", "the magician", "the high priestess", "the empress", "the emperor", "the hierophant","the lovers",
		"the chariot", "strength","the hermit", "wheel of fortune", "justice", "the hanged man", "death", 
		"temperance", "the devil", "the tower", "the star", "the moon", "the sun", "judgement", "the world"]

alt_cards_1 = [
		"fool", "magus", "priestess", "empress", "emperor", "hiero","lovers",
		"chariot", "adjustment","hermit", "fortune", "lust", "hanged", "death", 
		"art", "devil", "tower", "star", "moon", "sun", "aeon", "universe"]

alt_cards_2 = [
		"the fool", "the magician", "the papess", "the empress", "the emperor", "the pope","the lovers",
		"the chariot", "the strength","the hermit", "the wheel of fortune", "the justice", "the hanged man", "the death", 
		"the temperance", "the devil", "the tower", "the star", "the moon", "the sun", "the judgment", "the world"]

url_schemas = [
	("http://www.ata-tarot.com/resource/cards/maj{0:02d}.html",range(0,22)),
	("http://www.learntarot.com/maj{0:02d}.htm",range(0,22)),
	("http://www.tarot-cards-meanings-guide.com/{0}-tarot-card.html",[a.replace(" ","-") for a in alt_cards_2]),
	#("https://www.biddytarot.com/tarot-card-meanings/major-arcana/{0}/",[a.replace(" ","-") for a in rw_cards]), #403 forbidden
	("http://www.angelpaths.com/majors/{0}.html",alt_cards_1),
	("http://www.angelpaths.com/majors/{0}2.html",alt_cards_1), #This site has each card twice
	("http://www.psychic-revelation.com/reference/q_t/tarot/tarot_cards/{0}.html",[a.replace(" ", "_") for a in rw_cards_alt]),
	("http://www.tarotlore.com/tarot-cards/{0}",[a.replace(" ", "-") for a in rw_cards_the]),
	#tarot wikipedia has weird encodings that break things...
	("http://www.tarotwikipedia.com/tarot-card-meanings/major-arcana/{0}-tarot-card-meanings/", [a.replace(" ", "-") for a in rw_cards]),
	#tarotguide has an obnoxious internal structrue- no content on pure html response. 
	#("http://www.thetarotguide.com/{0}", [a.replace(" ", "-") for a in rw_cards_the]),
	("http://www.aeclectic.net/tarot/learn/meanings/", [a.replace(" ","-") for a in rw_cards]),
	]




def get_links(schema_tuple):
	links = []
	for i in schema_tuple[1]:
		links.append(schema_tuple[0].format(i))
	return links

all_links = [get_links(schema) for schema in url_schemas]

def badline(line):
	#Since auto-injected code sometimes gets caught with the content....
	illegal_seqs = ["=", "{","}",";","googletag", "Node"]
	if line == "":
		return True
	return any(char in line for char in illegal_seqs)

def link2text(link):
	response = urllib2.urlopen(link)
	raw = response.read()
	text = bs4(raw, "lxml").get_text().encode('utf-8').decode("ascii", "ignore")
	lines = [line for line in text.splitlines() if not badline(line)]
	return lines

splitline = "\n \n ======================================= \n \n"

def make_db():
	for card in range(0,22):
		name = rw_cards[card]
		print("Fetching descriptions for {0} ------------------".format(name))
		output_file = open("{}{}.txt".format(data_dir, name.replace(" ","_")),"w")
		for source in range(len(url_schemas)):
			link = all_links[source][card]
			print "		{0}".format(link)
			textlines = link2text(link)
			text = "\n".join(textlines)
			output_file.write(text)
			output_file.write(splitline)
		output_file.close()

def clean_db():
	print("Cleaning db")
	all_files_original = [open("{}/{}.txt".format(data_dir, name.replace(" ","_")),"r").readlines() for name in rw_cards]
	new_files = [open("{}/{}_clean.txt".format(data_dir, name.replace(" ","_")),"w") for name in rw_cards]
	for f in all_files_original:
		other = list(all_files_original)
		other.remove(f)
		other = [item for sublist in other for item in sublist]
		new_out = []
		for line in f:
			if line not in other or line==splitline:
				new_out.append(line)
		new_text = "".join(new_out)
		outputfile = new_files.pop(0)
		outputfile.write(new_text)
		outputfile.close()

if __name__ == "__main__":
	make_db() 
	clean_db()


