#include <iostream>
#include <cassert>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <sstream>
using namespace std;
char alph [4] = {' ','|','-','+'};
int w=1, h=1, freeSpots = 0;
int term = 0, solnsFound = 0, knight = 0;

int** createBoard(){
	int** board = new int*[h];
	for(int y = 0; y < h; y++) board[y] = new int[w];
	for(int x = 0; x < w; x++) for(int y = 0; y < h; y++) board[y][x] = -1;
	return board;
}

int** getBoardList(int** board){
	int** boardList = new int*[freeSpots];
	int i = 0;
	for(int y = 0; y < h; y++)
		for(int x = 0; x < w; x++)
			if(board[y][x] != -3) boardList[i++] = &(board[y][x]);
	return boardList;
}

bool inBounds(int y, int x){
	return y>=0 && x>=0 && y < h && x < w;
}

bool isValid(int** board){
	if(knight)
		for(int y = 0; y < h; y++) for(int x = 0; x < w; x++){
			int here = board[y][x];
			if(here < 2) continue;
			int dy = 2, dx = 1;
			bool nextFound = false;
			for(int i = 0; i < 8; i++){
				if(i%4==0) dy = -dy;
				else if(i%4==2) dx = -dx;
				else { int temp = dx; dx=dy; dy=-temp; }
				if(inBounds(y+dy,x+dx)) if(board[dy+y][dx+x] == -1 || here-1 == board[dy+y][dx+x]) { nextFound = true; break; }
			}
			if(!nextFound) return false;
		}
	else
		for(int y = 0; y < h; y++) for(int x = 0; x < w; x++)
			for(int dy = -1; dy <= 1; dy++) for(int dx = -1; dx <= 1; dx++)
				if(inBounds(y+dy,x+dx) && abs(board[y][x]-board[dy+y][dx+x]) == 1) return false;
	return true;
}

void printVBar(){
	for(int i = 0; i < w; i++) cout << "+---";
	cout << '+' << endl;
}

string getChar(int code){
	if(code == -1) return "   ";
	if(code < 0) return "###";
	ostringstream oss;
	oss << " " << code;
	if(code<10) oss << " ";
	return oss.str();
}

void printBoard(int** board){
	cout << endl;
	printVBar();
	for(int y = 0; y < h; y++){
		cout << '|';
		for(int x = 0; x < w; x++) cout << getChar(board[y][x]) << '|';
		cout << endl;
		printVBar();
	}
	cout << endl;
}

void printPoke(){
	char ch = 'a';
	cout << endl;
	printVBar();
	for(int y = 0; y < h; y++){
		cout << '|';
		for(int x = 0; x < w; x++) cout << ' ' << (ch++) << " |";
		cout << endl;
		printVBar();
	}
	cout << endl; 
}

void deleteBoard(int** board, int** boardList){
	delete [] boardList; // you dont need to loop thru boardList
	for(int i = 0; i < h; i++) delete [] board[i];
	delete [] board;
}

void getDimensions(){
	cout << endl << "Width: ";
	cin >> w;
	cout << endl << "Height: ";
	cin >> h;
}

void pokeHoles(int** board){
	printPoke();
	cout << "Poke Holes (sentinel: '.') : ";
	char coords = '.';
	while(true){
		cin >> coords;
		if(coords == '.') return;
		int c = coords - 'a';
		board[c/w][c%w] = -3;
	}
}

int countFreeSpots(int** board){
	int tally = 0;
	for(int y = 0; y < h; y++) for(int x = 0; x < w; x++) if(board[y][x] != -3) tally++;
	return tally;
}

void trySolve(int** board, int** boardList){
	if(!isValid(board)) return;
	int i = 0;
	for(i; i < freeSpots; i++) if(*(boardList[i]) == -1) break;
	if(i == freeSpots){ // leaf node
		solnsFound++;
		if(solnsFound == 1)printBoard(board);
		if(solnsFound % 10000 == 0) cout << solnsFound << " solutions found and counting..." << endl;
		if(term) { deleteBoard(board, boardList); exit(0); }
		return;
	}
	for(int n = 1; n <= freeSpots; n++){
		bool alreadyThere = false;
		for(int j = 0; j < freeSpots; j++) if(*(boardList[j]) == n) { alreadyThere = true; break; }
		if(alreadyThere) continue;
		*(boardList[i]) = n;
		trySolve(board, boardList);
	}
	*(boardList[i]) = -1;
}

int main(int argc, char* argv[]){
	if(argc > 1 && argv[1][0] == 't') term = 1;
	if(argc > 2 && argv[2][0] == 'k') knight = 1;
	getDimensions();
	int** board = createBoard();
	pokeHoles(board);
	freeSpots = countFreeSpots(board);
	int** boardList = getBoardList(board);
	printBoard(board);
	cout << "Solving..." << endl;
	trySolve(board, boardList);
	deleteBoard(board, boardList);
	cout << "Solutions found: " << solnsFound << endl << endl;
}
