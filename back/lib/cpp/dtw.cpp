#include <limits>
#include <cmath>
#include "dtw.h"
using namespace std;

float mu(float a, float b) {
	return abs(a-b);
}

float dtw(const vector& rec1, const vector& rec2, float freq, threshold) {
	n = rec1.length;
	m = rec2.length;
	tableau tab(n, m);
	for (int j=0; j<n; j++) {
        for (int i=0; i<m; i++) {
        	weight(i, j) = numeric_limits<float>::infinity();
        }
    }
    weight(0, 0) = mu(rec1[0], rec2[0])
    tab.ancestor(0, 0) = 0;
	tab.weight(1, 0) = mu(rec2[0], rec1[0]+rec1[1]);
	tab.ancestor(1, 0) = 1;
	tab.weight(0, 1) = mu(rec1[0], rec2[0]+rec2[1]);
	tab.ancestor(0, 1) = 2;
    for (int j=1; j<n; j++) {
    	int inf = max(ceil((i-1.)/2.), m-2*(n-i)+1);
		int sup = min(2*i+2, m-floor((n-i)/2.));
        for (int i=inf; i<sup; i++) {
        	float min_val = tab.weight(i-1, j-1)+mu(rec1[i], rec2[j]);
        	int min_ancestor = 0;
			if (i>=2) {
				float cost = tab.weight(i-2, j-1)+mu(rec1[i]+rec1[i-1], rec2[j]);
				if (cost < min_val) {
					min_val = cost;
					min_ancestor = 1;
				}
			}
			if (j>=2) {
				float cost = tab.weight(i-1, j-2)+mu(rec2[j]+rec2[j-1], rec1[i]);
				if (cost < min_val) {
					min_val = cost;
					min_ancestor = 2;
				}
			}
			tab.weight(i, j) = min_val;
			tab.ancestor(i, j) = min_ancestor;
        }
    }

    if tab.weight(n-1, m-1)/freq <= threshold:
		backtracking = vector<pair<int,int>>(n-1, m-1);

	/////////////////////////////////	A convertir / merge
		while backtracking[-1] != (-1, -1):
			#print(backtracking[-1])
			backtracking.append((warp_antecedant[0][backtracking[-1]], warp_antecedant[1][backtracking[-1]]))
		backtracking.reverse()
		print(word1, "|", word2, "(", freq, "):", value)
		if graph:
			adjustedrec1 = [sum([rec1[k] for k in range(backtracking[idx-1][0]+1, backtracking[idx][0]+1)]) for idx in range(1, len(backtracking))]
			adjustedrec2 = [sum([rec2[k] for k in range(backtracking[idx-1][1]+1, backtracking[idx][1]+1)]) for idx in range(1, len(backtracking))]
			plot(adjustedrec1)
			plot(adjustedrec2)
			show()
		return value, backtracking[:-1]


    int d_L = tab[(m+1)*(n+1)-1][0];
    int k = m, l = n;
    int* backtrack = new int[m+1+n+1];
    int pathLen = 0;
    while (k != 0 || l != 0) {
        int valPath = tab[l*(m+1)+k][1];
        backtrack[pathLen] = valPath;
        pathLen++;
        switch (valPath) {
            case -1:
                k--;
                l--;
                break;
            case 0:
                k--;
                break;
            case 1:
                l--;
                break;
            case 2:
                k--;
                l--;
        }
    }
    ////////////////////////////////////////////////////////////:
}

void free_mem(double* a)
{
 delete[] a;
}