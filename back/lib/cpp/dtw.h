// compile with : g++ -shared -O3 -Wall -fPIC -o dtw.so dtw.cpp
#include <assert>

extern "C" struct vect /* defines a vector of floats */
{
	int length;
};

class tableau {
	int nb_rows;
	int nb_cols;
	vect(rows, cols) {
		nb_rows = nb_rows,
		nb_cols = nb_cols;
		_weight = new float[nb_rows*nb_rows];
    }
    ~vect(rows, cols) {
		delete[] _weight;
		delete[] _antecedants;
    }
	float& weight(int i, int j) {
		assert(0 <= i && i < nb_rows && 0 <= j && j < nb_cols);
		return _weight[j+m*i];
	}
	float& antecedants(int i, int j) {
		assert(0 <= i && i < nb_rows && 0 <= j && j < nb_cols);
		return _antecedants[j+m*i];
	}

private:
	float* _weight;
	int* _antecedants;
};

extern "C" float dtw(vect*, vect*, float);