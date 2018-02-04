// compile with : g++ -shared -O3 -Wall -fPIC -o dtw.so dtw.cpp
#include <assert>

//class vect
//{
//	int length;
//	vect(int len) {
//		length = len;
//		vec = float[length];
//	}
//	~vec() {
//		delete[] vec;
//	}
//	float& at(int i) {
//		assert(0 <= i && i < length)
//		return vec[i];
//	}
//private:
//	float* vec
//};

class tableau {
	int nb_rows;
	int nb_cols;
	vect(rows, cols) {
		nb_rows = rows,
		nb_cols = cols;
		_weight = new float[nb_rows*nb_rows];
    }
    ~vect() {
		delete[] _weight;
		delete[] _ancestor;
    }
	float& weight(int i, int j) {
		assert(0 <= i && i < nb_rows && 0 <= j && j < nb_cols);
		return _weight[j+m*i];
	}
	float& ancestors(int i, int j) {
		assert(0 <= i && i < nb_rows && 0 <= j && j < nb_cols);
		return _ancestor[j+m*i];
	}

private:
	float* _weight;
	int* _ancestor;	// 0: (-1, -1), 1: (-2, -1), 2: (-1, -2)
};

float dtw(const vector& rec1, const vector& rec2, float freq);
