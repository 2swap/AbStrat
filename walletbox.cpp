#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <random>
using namespace std;

const int BOXES = 100;
int boxes[BOXES];

void randomize(){
	for(int i = 0; i < BOXES; i++) {
		boxes[i]=-1;
	}
	for(int i = 0; i < BOXES; i++) {
		int r = rand()%BOXES;
		while(true){
			if(boxes[r] == -1) {
				boxes[r] = i;
				break;
			}
			r++;
			r%=BOXES;
		}
	}
}

int flood(int i){
	if(boxes[i] == -1)
		return 0;
	boxes[i] = -1;
	int len = flood(boxes[i]);
	return len+1;
}

int longestChain(){
	int big = 0;
	for(int i = 0; i < BOXES; i++){
		big = max(big, flood(i));
	}
	return big;
}

int main(int argcount, char** args){
	randomize();
	cout << flood(50) << endl;
	int wins = 0;
	for(int i = 0; i < 1000; i++){
		randomize();
		if(longestChain()<=50)
			wins++;
	}
	cout << wins/1000.0 << endl;
}

