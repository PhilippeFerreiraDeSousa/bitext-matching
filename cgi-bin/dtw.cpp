#include "dtw.h"
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <locale>
#include <map>

using namespace std;

bool is_end_of_sentence(const string& word) {
    vector<char> strip = {'.', '?', '!', ';'};
    for (std::string::size_type i=0; i<word.length(); i++) {
        for (int j=0; j<strip.size(); j++) {
            if (word[i] == strip[j]) {
                return true;
            }
        }
    }
    return false;
}

void clean(string& word) {
    locale loc;
    for (string::size_type i=0; i<word.length(); ++i) {
        if (isalnum(word[i]) || word[i] == '-') {
            word[i] = tolower(word[i],loc);
        } else {
            word.erase(word.begin()+i);
        }
    }
}

void read_text() {
    vector<string> Words;
    ifstream myFile;
    string word;
    int id_line = 0;
    int id_word = 0;
    map<string, int*> word_indices;
    map<string, int*> word_indices_paragraphs;
    map<string, int> word_frequency;
    map<int, string> indice_paragraph;
    myFile.open("../text/en/le-petit-prince--antoine-de-saint-exupery.txt");
    if (myFile.is_open()) {
        while (myFile >> word) {
            if (is_end_of_sentence(word) || myFile.peek() == '\n') {
                clean(word);
                cout << word;
                cout << '\n';
            } else {
                clean(word);
                cout << word;
                cout << ' ';
            }
            if (myFile.peek() == '\n') {
                id_line++;
                cout << id_line << " : " << endl;
            }
            Words.push_back(word);
            id_word++;
        }
    }
    else cout << "Unable to open file";
}
