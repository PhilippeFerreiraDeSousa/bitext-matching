from string import ascii_uppercase, ascii_lowercase, digits
import re
from operator import itemgetter
from matplotlib.pyplot import plot, show
from numpy import zeros, infty

WORD_SEP = r"\W+"
SENTENCE_SEP = r'[\.\?!;:"]+'
PARAGRAPH_SEP = r'\n+'
PART_SEP = r'\n\n+'

def parts(text):
	return re.split(PART_SEP, text)
def paragraphs(text):
	return re.split(PARAGRAPH_SEP, text)
def sentences(paragraph):
	return re.split(SENTENCE_SEP, paragraph)
def words(sentence):
	return list(filter(None, re.split(WORD_SEP, sentence)))

def _clean(word):
	return 

def clean(element):
	assert (type(element) is str or type(element) is list), "you can clean strings or lists only, {} given".format(type(element))
	return (
		element.lower() if type(element) is str else
		[clean(subelement) for subelement in element]
	)

def main(file_name):
	with open("../../text/"+file_name, "r") as text_file:
	    text = "\n".join([line for line in text_file])

	data = filter(None, [filter(None, [clean(words(sentence)) for sentence in sentences(paragraph)]) for paragraph in paragraphs(text)])
	#print('\n\n'.join(['\n'.join([str(sentence) for sentence in paragraph]) for paragraph in data]))

	word_indices = {}
	word_freq = {}
	offset = 0
	for id_par, par in enumerate(data):
		for id_sen, sen in enumerate(par):
			for id_word, word in enumerate(sen):
				indices = (id_par, id_sen, id_word, offset)
				if word not in word_indices:
					word_indices[word] = [indices]
				else:
					word_indices[word].append(indices)
				offset+=1
	nb_words = offset
	print("Mots :", len(word_indices))
	recency_vect = {}
	for word, indices_list in word_indices.items():
		recency_vect[word] = [indices_list[0][3]/nb_words]
		for indices in indices_list[1:]:
			recency_vect[word].append(indices[3]/nb_words-recency_vect[word][-1])
		recency_vect[word].append(1-recency_vect[word][-1])

	for word, indices in word_indices.items():
		word_freq[word] = len(indices)/nb_words

	freq_ranking = sorted([(word, freq) for word, freq in word_freq.items()], key=itemgetter(1))

	# print(word_indices["i"])
	# print(word_freq["i"])
	#for i in range(20):
	#	print(top_freq[i])

	return data, word_indices, recency_vect, word_freq, freq_ranking

def compare_recency(en_word, fr_word):
	en_recency = en_recency_vect[en_word]
	plot(list(range(len(en_recency))), en_recency)

	fr_recency = fr_recency_vect[fr_word]
	plot(list(range(len(fr_recency))), fr_recency)
	show()

mu = lambda a, b: abs(a-b) 

def dtw(en_word, fr_word, freq):
	rec1, rec2 = en_recency_vect[en_word], fr_recency_vect[fr_word]
	n, m = len(rec1), len(rec2)
	warp = zeros((n, m))	# on initialise à warp[-1, -1] = 0
	for i in range(n):
		for j in range(m):
			minimum = [abs(rec1[i]-rec2[j]), (i-1, j-1)]
			ysum = rec1[i]
			xsum = rec2[j]
			for k in range(i-1, 0):
				ysum+=rec1[k]
				if mu(ysum, rec2[j]) < minimum[0]:
					minimum = [mu(ysum, rec2[j]), (k-1, j-1)]
				if ysum >= rec2[j]:
					break
			for l in range(j-1, 0):
				xsum+=rec2[l]
				if mu(xsum, rec1[i]) < minimum[0]:
					minimum = [mu(ysum, rec1[i]), (i-1, l-1)]
				if xsum >= rec1[i]:
					break
			warp[i, j] = warp[minimum[1]]+minimum[0]

	if warp[n-1, m-1]/freq <= 140:
		return warp[n-1, m-1]/freq
	else:
		return None


en_data, en_word_indices, en_recency_vect, en_word_freq, en_freq_ranking = main("en/le-petit-prince--antoine-de-saint-exupery.txt")
fr_data, fr_word_indices, fr_recency_vect, fr_word_freq, fr_freq_ranking = main("fr/le-petit-prince--antoine-de-saint-exupery.txt")

# compare_recency("prince", "prince")
# compare_recency("house", "maison")
# print(dtw("prince", "prince", en_word_freq["prince"]))
# print(dtw("house", "maison", en_word_freq["house"]))

nb_fr_words = len(fr_freq_ranking)
nb_en_words = len(en_freq_ranking)
bound_inf, bound_sup = 0, 0
idx_freq_min, idx_freq_max = 0, nb_en_words-1

while en_freq_ranking[idx_freq_min][1] < 0.00015:	# au moins 3 occurrences
	idx_freq_min+=1
while en_freq_ranking[idx_freq_max][1] > 0.003:
	idx_freq_max-=1

for word, freq in en_freq_ranking[idx_freq_min: idx_freq_max+1]:
	while bound_inf < nb_fr_words-1 and fr_freq_ranking[bound_inf][1] < freq*nb_fr_words/nb_en_words/1.1:	# nb_fr_words/nb_en_words est entre 1.1 et 1.15
		bound_inf+=1
	while bound_sup < nb_fr_words-1 and fr_freq_ranking[bound_sup][1] <= freq*nb_fr_words/nb_en_words*1.1:
		bound_sup+=1
	for idx in range(bound_inf, bound_sup):
		value = dtw(word, fr_freq_ranking[idx][0], freq)
		if value:
			print(word, "|", fr_freq_ranking[idx][0], "(", freq, "):", value)