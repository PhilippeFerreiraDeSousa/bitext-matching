from string import ascii_uppercase, ascii_lowercase, digits
from IBM2_func import _train_IBM2, show_matrix
import re
from math import ceil, floor
from operator import itemgetter
from matplotlib.pyplot import plot, show, title, xlim, ylim, xlabel, ylabel, xticks, legend, matshow
from numpy import zeros, ones, infty

# Rsultults
# nb occurr     nb matches    nb après lissage
#     3            166              138
#     4             71               62
#     5             58               58
#     6             13               13
#     7             47               47
#     8             16               16
#    9-20           73               73
#                                                                                                                                           

OCCUR_MIN = 4
FREQ_STEP = 0.001
FREQ_MAX = 0.002	# temps que l'incertitude sur la position du mot correspondant dans le texte d'en face est inférieur à l'écart entre 2 occurences.
FREQ_RATIO = 1.25
DTW_FACTOR = 1
BEGINNING_THRESHOLD = infty

# Pinocchio (pas bon)
#THRESHOLD = 10000
#FREQ_MIN = 0.00002
#FREQ_MAX = 0.01
#FREQ_RATIO = 1.2
#DTW_FACTOR = 1.5

FR_WORD_RE = r"\w+'?"
EN_WORD_RE = r"'?\w+"
SENTENCE_RE = r'[^ ]+"?[^\.\?!;:"]+[\.\?!;:"]+'
PARAGRAPH_RE = r"[^\n]*\w[^\n]*"

def paragraphs(text):
	return re.findall(PARAGRAPH_RE, text)
def sentences(paragraph):
	return re.findall(SENTENCE_RE, paragraph)
def words(sentence, WORD_RE):
	return re.findall(WORD_RE, sentence if "'" not in sentence else sentence.replace("n't", " not"))

def _clean(word):
	return word.lower()

def clean(element):
	assert (type(element) is str or type(element) is list), "you can clean strings or lists only, {} given".format(type(element))
	return (
		_clean(element) if type(element) is str else
		[clean(subelement) for subelement in element]
	)

def print_text(text):	# not used
	print('\n\n'.join(['\n'.join([str(sentence) for sentence in paragraph]) for paragraph in text]))

def read_file(instance, language):
	with open("../../text/{}/{}.txt".format(language, instance), "r") as text_file:
	    text = "\n".join([line for line in text_file])

	WORD_RE = EN_WORD_RE if language == "en" else FR_WORD_RE
	original_text = [sentences(paragraph) for paragraph in paragraphs(text)]
	clean_text = [[clean(words(sentence, WORD_RE)) for sentence in paragraph] for paragraph in original_text]

	return original_text, clean_text

def parse(clean_text):
	word_indices = {}
	word_freq = {}
	word_offset = 0
	sen_offset = 0
	for id_par, par in enumerate(clean_text):
		word_offset_in_par = 0
		for id_sen, sen in enumerate(par):
			for id_word, word in enumerate(sen):
				indices = ((id_par, id_sen, id_word), word_offset_in_par, sen_offset, word_offset)
				if word not in word_indices:
					word_indices[word] = [indices]
				else:
					word_indices[word].append(indices)
				word_offset+=1
				word_offset_in_par+=1
			sen_offset+=1
	nb_words = word_offset
	nb_sen = sen_offset
	recency_vect = {}
	for word, indices_list in word_indices.items():
		recency_vect[word] = [indices_list[0][3]/nb_words]
		for idx in range(1, len(indices_list)):
			recency_vect[word].append((indices_list[idx][3]-indices_list[idx-1][3])/nb_words)
		recency_vect[word].append(1-indices_list[-1][3]/nb_words)

	for word, indices in word_indices.items():
		word_freq[word] = len(indices)/nb_words

	freq_ranking = sorted([(word, freq) for word, freq in word_freq.items()], key=itemgetter(1))

	# print(word_indices["i"])
	# print(word_freq["i"])
	#for i in range(20):
	#	print(top_freq[i])

	return word_indices, recency_vect, word_freq, freq_ranking, nb_words, nb_sen

def compare_recency(en_word, fr_word, en_recency, fr_recency):
	plot(list(range(len(en_recency))), en_recency, label=en_word)
	plot(list(range(len(fr_recency))), fr_recency, label=fr_word)
	title("Vecteur de récence")
	xlabel("Indice de portions correspondantes")
	ylabel("Longueur relative de portion")
	legend()
	show()

mu = lambda a, b: abs(a-b) 

def _dtw(rec1, rec2, freq):
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
	k = (1 if freq <= FREQ_STEP else 2)
	for i in range(1, n):
		for j in range(max(ceil((i-1)/2), m-2*(n-i)+1), min(2*i+2, m-floor((n-i)/2))):
			minimum = [warp[i-1, j-1]+mu(rec1[i], rec2[j]), (i-1, j-1)]
			for l in range(1, k):
				if i >= 1+l:
					cost = warp[i-1-l, j-1]+mu(sum([rec1[t] for t in range(i-l, i+1)]), rec2[j])
					if cost < minimum[0]:
						minimum = [cost, (i-1-l, j-1)]
				else:
					break
			for l in range(1, k+1):
				if j >= 1+l:
					cost = warp[i-1, j-1-l]+mu(rec1[i], sum([rec2[t] for t in range(j-l, j+1)]))
					if cost < minimum[0]:
						minimum = [cost, (i-1, j-1-l)]
				else:
					break
			warp[i, j] = minimum[0]
			#print(warp[i,j])
			warp_antecedant[0][i, j] = minimum[1][0]
			warp_antecedant[1][i, j] = minimum[1][1]
		#print("\n")
	#matshow(warp)
	show()
	#for i in range(n):
	#	print([(warp_antecedant[0][i, j], warp_antecedant[1][i, j]) for j in range(m)])
	return warp[n-1, m-1]/freq**DTW_FACTOR, warp_antecedant

def dtw(word1, word2, rec1, rec2, freq, threshold, graph=False):
	value, warp_antecedant = _dtw(rec1, rec2, freq)
	n, m = len(rec1), len(rec2)
	if  value <= threshold:
		backtracking = [(n-1, m-1)]
		while backtracking[-1] != (-1, -1):
			#print(backtracking[-1])
			backtracking.append((warp_antecedant[0][backtracking[-1]], warp_antecedant[1][backtracking[-1]]))
		backtracking.reverse()
		print(word1, "|", word2, "(", freq, "):", value)
		if graph:
			adjustedrec1 = [sum([rec1[k] for k in range(backtracking[idx-1][0]+1, backtracking[idx][0]+1)]) for idx in range(1, len(backtracking))]
			adjustedrec2 = [sum([rec2[k] for k in range(backtracking[idx-1][1]+1, backtracking[idx][1]+1)]) for idx in range(1, len(backtracking))]
			plot(adjustedrec1, label=word1)
			plot(adjustedrec2, label=word2)
			title("Correspondance par dilatation temporelle")
			xlabel("Indice de portion entre occurences")
			ylabel("Longueur relative de portion")
			legend()
			show()
		draw = False
		if draw:
			freqs1 = [sum(rec1[:i]) for i in range(len(rec1))]
			freqs2 = [sum(rec2[:i]) for i in range(len(rec2))]
			match_points1 = [freqs1[backtracking[idx][0]+1] for idx in range(len(backtracking)-1)]
			match_points2 = [freqs2[backtracking[idx][1]+1] for idx in range(len(backtracking)-1)]
			#print(backtracking)
			#for p in freqs1:
			#	plot([0.95, 1.05], [p, p])
			#for p in freqs1:
			#	plot([1.95, 2.05], [p, p])
			for idx in range(len(match_points1)):
				plot([1, 2], [match_points1[idx], match_points2[idx]])
			plot([1, 1], [1, 2])
			plot([2, 2], [1, 2])
			show()
		return value, backtracking[:-1]
	else:
		return value, None


def filter_smooth(match_list):	# the list must be ordered
	assert match_list, "Aucun match trouvé"
	print("Smooth filtering")
	filtered_match_list = [match_list[0]]
	removed = []
	for i in range(1, len(match_list)-1):	# borne par 10 la dérivée disrète
		if abs((filtered_match_list[-1][1][3]+match_list[i+1][1][3])/2-match_list[i][1][3]) < 10*abs(match_list[i+1][0][3]-filtered_match_list[-1][0][3])/2:
			filtered_match_list.append(match_list[i])
		else:
			removed.append(match_list[i])
	filtered_match_list.append(match_list[-1])
	return filtered_match_list, removed

def filter_per_par(match_list):	# the list must be ordered
	assert match_list, "Aucun match trouvé"
	print("Per paragraph filtering")
	filtered_match_list = [match_list[0]]
	removed = []
	for i in range(1, len(match_list)-1):	# check that paragraph number is increasing
		if filtered_match_list[-1][1][0][0] <= match_list[i][1][0][0] <= match_list[i+1][1][0][0]:
			filtered_match_list.append(match_list[i])
		else:
			removed.append(match_list[i])
	return filtered_match_list, removed

def filter_non_bijective_matches(match_list, en_clean_text, fr_clean_text):
	en_match = {}
	fr_match = {}
	filtered_match_list = []
	removed = []
	for match in match_list:
		en_word = en_clean_text[match[0][0][0]][match[0][0][1]][match[0][0][2]]
		fr_word = fr_clean_text[match[1][0][0]][match[1][0][1]][match[1][0][2]]
		if en_word not in en_match:
			en_match[en_word] = [[match], fr_word]
		elif fr_word == en_match[en_word][1]:
			en_match[en_word][0].append(match)
		elif match[2] < en_match[en_word][0][0][2]:
				en_match[en_word] = [[match], fr_word]
		if fr_word not in fr_match:
			fr_match[fr_word] = [[match], en_word]
		elif en_word == fr_match[fr_word][1]:
			fr_match[fr_word][0].append(match)
		elif match[2] < fr_match[fr_word][0][0][2]:
			fr_match[fr_word] = [[match], en_word]
	for en_word, [match_list, fr_word] in en_match.items():
		if en_word == fr_match[fr_word][1]:
			filtered_match_list.extend(match_list)
		else:
			removed.extend(match_list)

	return sorted(filtered_match_list, key=lambda x: x[0][3]), removed

def estimate_threshold(en_freq_ranking, fr_freq_ranking, en_recency_vect, fr_recency_vect, en_word_indices, fr_word_indices, en_nb_words):
	en_nb_different_words = len(en_freq_ranking)
	fr_nb_different_words = len(fr_freq_ranking)
	bound_inf, bound_sup = 0, 0
	match_list = []
	idx_freq_min, idx_freq_max = 0, en_nb_different_words-1

	while en_freq_ranking[idx_freq_min][1]*en_nb_words < OCCUR_MIN:	# au moins 4 occurrences 0.00023
		idx_freq_min+=1
	while en_freq_ranking[idx_freq_max][1] > FREQ_MAX:
		idx_freq_max-=1

	while idx_freq_min <= idx_freq_max:
		en_word, freq = en_freq_ranking[idx_freq_min]
		idx_freq_min+=1
		if freq*en_nb_words > OCCUR_MIN:
			break
		while bound_inf < fr_nb_different_words-1 and fr_freq_ranking[bound_inf][1] < freq/FREQ_RATIO:
			bound_inf+=1
		while bound_sup < fr_nb_different_words-1 and fr_freq_ranking[bound_sup][1] <= freq*FREQ_RATIO:
			bound_sup+=1
		for idx in range(bound_inf, bound_sup):
			fr_word = fr_freq_ranking[idx][0]
			value, path = dtw(en_word, fr_word, en_recency_vect[en_word], fr_recency_vect[fr_word], freq, BEGINNING_THRESHOLD)
			if path:
				for match in path:
					match_list.append((en_word_indices[en_word][match[0]], fr_word_indices[fr_word][match[1]], value))
	match_list.sort(key=itemgetter(2))
	match_list = match_list[:min(len(match_list), ceil(en_nb_words/250))]	# calibrer pour garder les 16 meilleures matches parmis les mots de 4 lettres pour ce texte de 16 000 mots
	threshold = match_list[-1][2]
	print("THRESHOLD :", threshold)
	return threshold, match_list, idx_freq_min, idx_freq_max, bound_inf, bound_sup

def matching_layer(threshold, match_list, en_freq_ranking, fr_freq_ranking, en_recency_vect, fr_recency_vect, en_word_indices, fr_word_indices, bound_inf, bound_sup):
	en_nb_different_words = len(en_freq_ranking)
	fr_nb_different_words = len(fr_freq_ranking)

	for en_word, freq in en_freq_ranking:
		#if freq >= FREQ_STEP:
		#	adjusted_freq_ratio = 2*FREQ_RATIO
		while bound_inf < fr_nb_different_words-1 and fr_freq_ranking[bound_inf][1] < freq/FREQ_RATIO:	#*nb_fr_words/nb_en_words
			bound_inf+=1
		while bound_sup < fr_nb_different_words-1 and fr_freq_ranking[bound_sup][1] <= freq*FREQ_RATIO:	#*nb_fr_words/nb_en_words
			bound_sup+=1
		for idx in range(bound_inf, bound_sup):
			fr_word = fr_freq_ranking[idx][0]
			value, path = dtw(en_word, fr_word, en_recency_vect[en_word], fr_recency_vect[fr_word], freq, threshold)
			if path:
				for match in path:
					match_list.append((en_word_indices[en_word][match[0]], fr_word_indices[fr_word][match[1]], value))

	match_list.sort(key=lambda x: x[0][3])

def filtration_layer(match_list, en_clean_text, fr_clean_text):
	print("Avant filtration :", len(match_list))
	plot([item[0][3] for item in match_list], [item[1][3] for item in match_list], label="sans filtration")
	#show()

	match_list, non_bijective_removed = filter_non_bijective_matches(match_list, en_clean_text, fr_clean_text)
	print("Après filtration des matches non bijectifs :", len(match_list))
	plot([item[0][3] for item in match_list], [item[1][3] for item in match_list], label="(1) par bijection")
	#show()

	match_list, smooth_removed = filter_smooth(match_list)
	print("Après filtration par lissage :", len(match_list))
	plot([item[0][3] for item in match_list], [item[1][3] for item in match_list], label="(2) par lissage")

	match_list, per_par_removed = filter_per_par(match_list)
	print("Après filtration par paragraphe croissant :", len(match_list))
	plot([item[0][3] for item in match_list], [item[1][3] for item in match_list], label="(3) par paragraphe croissant")
	title("Alignement après filtration (1), (2) puis (3)")
	xlabel("Indice de mot anglais")
	ylabel("Indice de mot français")
	legend()
	show()
	#plot([item[0][2] for item in match_list], [item[1][2] for item in match_list])
	#plot([item[0][2] for item in smooth_match_list], [item[1][2] for item in smooth_match_list])
	#show()
	#plot([item[0][0][0] for item in match_list], [item[1][0][0] for item in match_list])
	#plot([item[0][0][0] for item in smooth_match_list], [item[1][0][0] for item in smooth_match_list])
	#show()

	print("Non bijective matches removed")
	for match in non_bijective_removed:
		print(en_clean_text[match[0][0][0]][match[0][0][1]][match[0][0][2]], "|", fr_clean_text[match[1][0][0]][match[1][0][1]][match[1][0][2]])
	print("Smooth removed")
	for match in smooth_removed:
		print(en_clean_text[match[0][0][0]][match[0][0][1]][match[0][0][2]], "|", fr_clean_text[match[1][0][0]][match[1][0][1]][match[1][0][2]])
	print("Per par removed")
	for match in per_par_removed:
		print(en_clean_text[match[0][0][0]][match[0][0][1]][match[0][0][2]], "|", fr_clean_text[match[1][0][0]][match[1][0][1]][match[1][0][2]])

def zipf_curve(freq_ranking, nb_words, label, show=True):
	freqs = [freq_ranking[0][1]]
	zipf_law = [1]
	for word, freq in freq_ranking[1:]:
		if freqs[-1] == freq:
			zipf_law[-1]+=1
		else:
			freqs.append(freq)
			zipf_law.append(1)
	# print(sum([freqs[i]*zipf_law[i]**2 for i in range(len(freqs))])/len(freqs))
	nb_occurs = [freq*nb_words for freq in freqs]
	if show:
		line = plot(nb_occurs, zipf_law, label=label)

	return nb_occurs, zipf_law, line

def draw_occurences_chart(en_freq_ranking, fr_freq_ranking, en_nb_words, fr_nb_words):
	en_nb_occurs, en_zipf_law, en_line = zipf_curve(en_freq_ranking, en_nb_words, "anglais")
	fr_nb_occurs, fr_zipf_law, fr_line = zipf_curve(fr_freq_ranking, fr_nb_words, "français")
	inverse_square = plot([occurs for occurs in en_nb_occurs], [2000/occurs**2 for occurs in en_nb_occurs], ls=":", label=r"$\dfrac{1}{n^2}$")
	plot([OCCUR_MIN, OCCUR_MIN], [0, 1000], ls="--")
	plot([FREQ_MAX*en_nb_words, FREQ_MAX*en_nb_words], [0, 1000], ls="--")
	legend()
	title("Effectif avec même nombre d'occurrences")
	xlabel("Nombre d'occurrences d'un mot")
	ylabel("Nombre de mots")
	xlim(0, FREQ_MAX*en_nb_words+OCCUR_MIN)
	ylim(0, 100)
	show()

def apply_IBM(match_list, en_clean_text, fr_clean_text):
	corpus_IBM2 = []
	for match in match_list[:4]:
		if (en_clean_text[match[0][0][0]][match[0][0][1]], fr_clean_text[match[1][0][0]][match[1][0][1]]) not in corpus_IBM2:	
			corpus_IBM2.append((en_clean_text[match[0][0][0]][match[0][0][1]], fr_clean_text[match[1][0][0]][match[1][0][1]]))
	t_IBM2, a_IBM2 = _train_IBM2(corpus_IBM2, loop_count=1000)

	len(t_IBM2)
	len(a_IBM2)

	for (es, fs) in corpus_IBM2:
		#max_a = viterbi_alignment(es, fs, t_IBM2, a_IBM2).items()
		m = len(es)
		n = len(fs)
		args = (es, fs, t_IBM2, a_IBM2)
		print(show_matrix(*args))

def bisect_match(en_clean_text, fr_clean_text):
	pass

def main(instance):
	en_original_text, en_clean_text = read_file(instance, "en")
	en_word_indices, en_recency_vect, en_word_freq, en_freq_ranking, en_nb_words, en_nb_sen = parse(en_clean_text)
	print("Longueur du texte {} ({}): {} mots.".format(instance, "en", en_nb_words))
	print("Nombres de mots différents : {}.".format(len(en_word_indices)))
	fr_original_text, fr_clean_text = read_file(instance, "fr")
	fr_word_indices, fr_recency_vect, fr_word_freq, fr_freq_ranking, fr_nb_words, fr_nb_sen = parse(fr_clean_text)
	print("Longueur du texte {} ({}): {} mots.".format(instance, "fr", fr_nb_words))
	print("Nombres de mots différents : {}.".format(len(fr_word_indices)))

	#bisect_match()

	draw_occurences_chart(en_freq_ranking, fr_freq_ranking, en_nb_words, fr_nb_words)

	compare_recency("but", "mais", en_recency_vect["but"], fr_recency_vect["mais"])
	dtw("but", "mais", en_recency_vect["but"], fr_recency_vect["mais"], en_word_freq["but"], infty, True)

	#compare_recency("cat", "chat", en_recency_vect["cat"], fr_recency_vect["chat"])
	#dtw("cat", "chat", en_recency_vect["cat"], fr_recency_vect["chat"], en_word_freq["cat"], infty, True)
	compare_recency("flowers", "fleurs", en_recency_vect["flowers"], fr_recency_vect["fleurs"])
	dtw("flowers", "fleurs", en_recency_vect["flowers"], fr_recency_vect["fleurs"], en_word_freq["flowers"], infty, True)
	compare_recency("king", "roi", en_recency_vect["king"], fr_recency_vect["roi"])
	dtw("king", "roi", en_recency_vect["king"], fr_recency_vect["roi"], en_word_freq["king"], infty, True)
	compare_recency("prince", "prince", en_recency_vect["prince"], fr_recency_vect["prince"])
	dtw("prince", "prince", en_recency_vect["prince"], fr_recency_vect["prince"], en_word_freq["prince"], infty, True)
	compare_recency("why", "pourquoi", en_recency_vect["why"], fr_recency_vect["pourquoi"])
	dtw("why", "pourquoi", en_recency_vect["why"], fr_recency_vect["pourquoi"], en_word_freq["why"], infty, True)
	#print(dtw("!", "!", en_word_freq["!"]))

	threshold, match_list, idx_freq_min, idx_freq_max, bound_inf, bound_sup = estimate_threshold(en_freq_ranking, fr_freq_ranking, en_recency_vect, fr_recency_vect, en_word_indices, fr_word_indices, en_nb_words)
	matching_layer(threshold, match_list, en_freq_ranking[idx_freq_min: idx_freq_max+1], fr_freq_ranking, en_recency_vect, fr_recency_vect, en_word_indices, fr_word_indices, bound_inf, bound_sup)
	print("Nombre de phrases en anglais :", en_nb_sen)
	print("Nombre de phrases en français :", fr_nb_sen)
	filtration_layer(match_list, en_clean_text, fr_clean_text)



	for match in match_list:
		print(en_original_text[match[0][0][0]][match[0][0][1]])
		print(fr_original_text[match[1][0][0]][match[1][0][1]])
		print("\n")

	#apply_IBM(match_list)


main("le-petit-prince--antoine-de-saint-exupery")
# main("bible")
# main("pinocchio")


# TODO
# dtw renvoie les indices des mots qui match + afficher graph pour illustrer
# Cognat avec inflexions : distance de Levenshtein, distance de Jaro-Winkler, virer n't  ou tout mot avec '
# tester dtw de l'article
# aligner sur ponctuation
# générer lists de par, phrases
# tester algo Victoriya / Nada
# tester sur la bible et pinocchio
# tester findall(r'\w+'*)

#dans le formulaire
#alignement paragraphe par paragraphe
#alignement phrase par phrase
#séparateur de paragraphe et phrase

# portugais, YT, Illuin

# dtw en c++ avec multiprocessing sur Leviathan
# appliqué dtw localement avec MIN_OCCUR plus le-petit-prince--antoine-de-saint-exupery
# aligner

# remove dulicate aligned
# we can  keep only duplicate match to filter
# bisect filter
# matshow