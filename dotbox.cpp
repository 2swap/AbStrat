#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <vector>
#include <fstream>
#include <unordered_set>
using namespace std;

typedef pair<int,int> coord;

struct Board
{
	unordered_set<coord> points;
	int size;
};

void print_board(Board* b){
	cout << endl;
	for(int y = 0; y < b->size; ++y) {
		for(int x = 0; x < b->size; ++x)
			cout << (b->points.count(coord(y, x))?"#":"-");
		cout << endl;
	}
}

bool validate(Board* board){
	unordered_set<int> dists;
	for(unordered_set<coord>::iterator p1 = board->points.begin(); p1 != board->points.end(); p1++)
		for(unordered_set<coord>::iterator p2 = board->points.begin(); p2 != p1; p2++){
			int dy = p2->first-p1->first;
			int dx = p2->second-p1->second;
			int d = dy*dy+dx*dx;
			if(d == 0 || dists.count(d))
				return false;
			dists.insert(d);
		}
	return true;
}

int main(int argcount, char** args){
	if(argcount != 2) {
		cout << "Need input number!" << endl;
		return 1;
	}

	Board* board = new Board();
	board->size = args[1][0]-'0';
	board->points.insert(coord(0,0));
	board->points.insert(coord(0,1));
	print_board(board);
}
