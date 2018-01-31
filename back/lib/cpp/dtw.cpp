
extern "C" float dtw(vect* rec1, vect* rec2, float freq) {
	n = rec1->length;
	m = rec2->length;

	float** tab = new float*[m*n];
    for (int k=0; k<m*n; k++) {
        tab[k] = new int[3];
    }
    for (int j=0; j<n; j++) {
        // cout  << " | ";
        for (int i=0; i<m; i++) {
            if (j == 0) {
                tab[i][0] = i;
                tab[i][1] = 0;
            } else if (i == 0) {
                tab[id(0, j)][0] = j;
                tab[id(0, j)][1] = 1;
            } else {
                if (word1[i-1] == word2[j-1]) {
                    tab[j*(m+1)+i][0] = tab[(j-1)*(m+1)+i-1][0];
                    tab[j*(m+1)+i][1] = -1;
                }
                else {
                    if (tab[j*(m+1)+i-1][0] <= tab[(j-1)*(m+1)+i][0] &&
                        tab[j*(m+1)+i-1][0] <= tab[(j-1)*(m+1)+i-1][0]) {
                        tab[j*(m+1)+i][0] = tab[j*(m+1)+i-1][0]+1;
                        tab[j*(m+1)+i][1] = 0;
                    } else if (tab[(j-1)*(m+1)+i][0] <= tab[(j-1)*(m+1)+i-1][0]) {
                        tab[j*(m+1)+i][0] = tab[(j-1)*(m+1)+i][0]+1;
                        tab[j*(m+1)+i][1] = 1;
                    } else {
                        tab[j*(m+1)+i][0] = tab[(j-1)*(m+1)+i-1][0]+1;
                        tab[j*(m+1)+i][1] = 2;
                    }
                }
            }
            // cout << tab[j*(m+1)+i][0] << " | ";
        }
        // cout << endl;
    }
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
    k = l = 0;
    for (int i=pathLen-1; i>=0; i--) {
        switch (backtrack[i]) {
            case -1:
                k++;
                l++;
                break;
            case 0:
                cout << "Insérer '"
                     << word1[k]
                     << "' en position "
                     << k+1;
                word2 = word2.insert(l, word1.substr(k, 1));
                k++;
                l++;
                break;
            case 1:
                cout << "Supprimer '"
                     << word2[l]
                     << "' en position "
                     << l+1;
                word2 = word2.erase(l, 1);
                break;
            case 2:
                cout << "Substituer '"
                     << word2[l]
                     << "' par '"
                     << word1[k]
                     << "' en position "
                     << l+1;
                word2.replace(l, 1, word1.substr(k, 1));
                k++;
                l++;
        }
        if (backtrack[i] != -1) {
            cout << " -> "
                 << word2
                 << endl;
        }
    }

    cout << endl
         << "La distance de Levenshtein entre "
         << word1
         << " et "
         << word2
         << " est "
         << d_L
         << "."
         << endl
         << "____________________________________________________________________"
         << endl
         << endl;

    for (int k=0; k<(m+1)*(n+1); k++) {
        delete[] tab[k];
    }
    delete[] tab;
    delete[] backtrack;
}

void free_mem(double* a)
{
 delete[] a;
}