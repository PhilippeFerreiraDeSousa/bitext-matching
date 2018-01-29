from string import ascii_uppercase, ascii_lowercase, digits
import re
from math import ceil, floor
from operator import itemgetter
from matplotlib.pyplot import plot, show
from numpy import zeros, ones, infty

WORD_SEP = r"\W+"
SENTENCE_SEP = r'[\.\?!;:"]+'
PARAGRAPH_SEP = r'(\n)+'
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

	pars = paragraphs(text)
	print(paragraphs)
	data = filter(None, [filter(None, [clean(words(sentence)) for sentence in sentences(paragraph)]) for paragraph in pars])
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

def _dtw(rec1, rec2):
	n, m = len(rec1), len(rec2)
	warp = infty*ones((n, m))	# les 1 font office de +infinity
	warp_antecedant = (zeros((n, m), dtype=int), zeros((n, m), dtype=int))
	warp[0, 0] = mu(rec1[0], rec2[0])
	warp_antecedant[0][0, 0] = -1
	warp_antecedant[1][0, 0] = -1
	warp[1, 0] = mu(rec2[0], rec1[0]+rec1[1])
	warp_antecedant[0][1, 0] = -1
	warp_antecedant[1][1, 0] = -1
	warp[0, 1] = mu(rec1[0], rec2[0]+rec2[1])
	warp_antecedant[0][0, 1] = -1
	warp_antecedant[1][0, 1] = -1
	for i in range(1, n):
		for j in range(max(ceil((i-1)/2), m-2*(n-i)+1), min(2*i+2, m-floor((n-i)/2))):
			minimum = [warp[i-1, j-1]+mu(rec1[i], rec2[j]), (i-1, j-1)]
			if i>=2:
				cost = warp[i-2, j-1]+mu(rec1[i]+rec1[i-1], rec2[j])
				if cost < minimum[0]:
					minimum = [cost, (i-2, j-1)]
			if j>=2:
				cost = warp[i-1, j-2]+mu(rec2[j]+rec2[j-1], rec1[i])
				if cost < minimum[0]:
					minimum = [cost, (i-1, j-2)]
			warp[i, j] = minimum[0]
			warp_antecedant[0][i, j] = minimum[1][0]
			warp_antecedant[1][i, j] = minimum[1][1]
	#for i in range(n):
	#	print([(warp_antecedant[0][i, j], warp_antecedant[1][i, j]) for j in range(m)])
	return warp[n-1, m-1], warp_antecedant

def dtw(en_word, fr_word, freq, graph=False):
	rec1, rec2 = en_recency_vect[en_word], fr_recency_vect[fr_word]
	value, warp_antecedant = _dtw(rec1, rec2)
	n, m = len(rec1), len(rec2)
	if  value/freq**1.2 <= 600:
		backtracking = [(n-1, m-1)]
		while backtracking[-1] != (-1, -1):
			#print(backtracking[-1])
			backtracking.append((warp_antecedant[0][backtracking[-1]], warp_antecedant[1][backtracking[-1]]))
		backtracking.reverse()
		print(en_word, "|", fr_word, "(", freq, "):", value/freq**1.2)
		if graph :
			adjustedrec1 = [sum([rec1[k] for k in range(backtracking[idx-1][0]+1, backtracking[idx][0]+1)]) for idx in range(1, len(backtracking))]
			adjustedrec2 = [sum([rec2[k] for k in range(backtracking[idx-1][1]+1, backtracking[idx][1]+1)]) for idx in range(1, len(backtracking))]
			plot(adjustedrec1)
			plot(adjustedrec2)
			show()
		return value, backtracking[:-1]
	else:
		return None, None


def filter_warping(match_list):	# the list must be ordered
	filtered_match_list = [match_list[0]]
	for i in range(1, len(match_list)-1):
		if abs((filtered_match_list[-1][1]+match_list[i+1][1])/2-match_list[i][1]) < 10*abs(match_list[i+1][0]-filtered_match_list[-1][0])/2:
			filtered_match_list.append(match_list[i])
	return filtered_match_list

en_data, en_word_indices, en_recency_vect, en_word_freq, en_freq_ranking = main("en/le-petit-prince--antoine-de-saint-exupery.txt")
fr_data, fr_word_indices, fr_recency_vect, fr_word_freq, fr_freq_ranking = main("fr/le-petit-prince--antoine-de-saint-exupery.txt")

#compare_recency("flowers", "fleurs")
#dtw("flowers", "fleurs", en_word_freq["flowers"], True)
#compare_recency("prince", "prince")
#dtw("prince", "prince", en_word_freq["prince"], True)
#compare_recency("why", "pourquoi")
#dtw("why", "pourquoi", en_word_freq["why"], True)
#print(dtw("!", "!", en_word_freq["!"]))

nb_fr_words = len(fr_freq_ranking)
nb_en_words = len(en_freq_ranking)
bound_inf, bound_sup = 0, 0
idx_freq_min, idx_freq_max = 0, nb_en_words-1
match_list = []

while en_freq_ranking[idx_freq_min][1] < 0.00015:	# au moins 5 occurrences
	idx_freq_min+=1
while en_freq_ranking[idx_freq_max][1] > 0.005:
	idx_freq_max-=1

for en_word, freq in en_freq_ranking[idx_freq_min: idx_freq_max+1]:
	while bound_inf < nb_fr_words-1 and fr_freq_ranking[bound_inf][1] < freq*nb_fr_words/nb_en_words/1.1:	# nb_fr_words/nb_en_words est entre 1.1 et 1.15
		bound_inf+=1
	while bound_sup < nb_fr_words-1 and fr_freq_ranking[bound_sup][1] <= freq*nb_fr_words/nb_en_words*1.1:
		bound_sup+=1
	for idx in range(bound_inf, bound_sup):
		fr_word = fr_freq_ranking[idx][0]
		value, path = dtw(en_word, fr_word, freq)
		if path:
			for match in path:
				match_list.append((en_word_indices[en_word][match[0]][3], fr_word_indices[fr_word][match[1]][3]))
				if abs(en_word_indices[en_word][match[0]][3]-fr_word_indices[fr_word][match[1]][3]) >= 5000:
					print(en_word, "!=", fr_word)

match_list.sort(key=itemgetter(0))
plot([item[0] for item in match_list], [item[1] for item in match_list])
print("Avant filtration :", len(match_list))
filtered_match_list = filter_warping(match_list)
plot([item[0] for item in filtered_match_list], [item[1] for item in filtered_match_list])
print("Après filtration :", len(filtered_match_list))
show()



# TODO
# dtw renvoie les indices des mots qui match + afficher graph pour illustrer
# Cognat avec inflexions : distance de Levenshtein, distance de Jaro-Winkler, virer n't  ou tout mot avec '
# tester dtw de l'article
# aligner sur ponctuation
# générer lists de par, phrases
# tester algo Victoriya / Nada
# tester sur la bible et pinocchio
# tester findall(r'\w+'*)

# portugais, YT, Illuin