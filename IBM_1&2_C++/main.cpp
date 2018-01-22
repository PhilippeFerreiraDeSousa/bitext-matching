#undef  __DEPRECATED //neglect the warnings in using hash_map

#include<iostream>
#include<fstream>
#include<sstream>
#include<string>
#include<vector>
#include<map>
#include<set>
#include<cstdlib>
#include<limits.h>
#include<utility>

#include "gl_defs.h"
#include "vocab.h"
#include "sentence.h"
#include "model12.h"
#include "hmm.h"

using namespace std;


int main(int argc, char **argv)
{
//        if(argc < 5){
//                cout<<"HELP: Please call "<<argv[0]<<" in this format: "<<argv[0]<<" source.vcb target.vcb source_target.snt source_target.cooc"<<endl;
//                exit(1);
//        }

        VcbList evcb(argv[1]);
        VcbList fvcb(argv[2]);
        fvcb.readVocalList();
        evcb.readVocalList();
        SentenceHandle sentcorpus(argv[3]);
        ofstream out_alignment("alignment");
        
        return 0;
}
