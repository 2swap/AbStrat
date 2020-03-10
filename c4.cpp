#include <iostream>
#include <cassert>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <unordered_map>

using namespace std;
typedef unordered_map<double,int> Cache;

Cache cache;
char** realBoard;
char alph [4] = {' ','|','-','+'};
string players;
int w=5, h=4, c=4;

double hashBoard(char** board){
	double sum1 = 0, sum2 = 0;
	double cur = 1.0;
	for(int y = 0; y < h; y++) for(int x = 0; x < w; x++){
		     if(board[y][x] == 'O')     sum1+=cur;
		else if(board[y][x] == 'X')     sum1+=cur*2;
		     if(board[y][w-1-x] == 'O') sum2+=cur;
		else if(board[y][w-1-x] == 'X') sum2+=cur*2;
		cur/=1.014593378925692398138;
	}
	return sum1>sum2?sum1:sum2;
}

void createBoard(){
	realBoard = new char*[h];
	for(int y = 0; y < h; y++) realBoard[y] = new char[w];
	for(int x = 0; x < w; x++) for(int y = 0; y < h; y++) realBoard[y][x] = ' ';
}

bool inBounds(int y, int x){
	return y >= 0 && x >= 0 && y < h && x < w;
}

char whoWon(char** board, int y, int x){
	char col = board[y][x];
	int oy = y, ox = x;
	int dir = 0;
	for(int dy = -1; dy <= 1; dy++) for(int dx = -1; dx <= 1; dx++){
		y = oy; x = ox;
		int lsum = 0, rsum = 0;
		for(lsum; lsum < 3; lsum++){
			y+=dy; x+=dx;
			if(!inBounds(y,x) || col!=board[y][x]) break;
		}
		if(lsum == c-1) return col;
		y = oy; x = ox;
		for(rsum; rsum<c-1-lsum; rsum++){
			y-=dy; x-=dx;
			if(!inBounds(y,x) || col!=board[y][x]) break;
			if(rsum+lsum > c-3) return col;
		}
		if(dir == 3) return ' ';
		dir++;
	}
	assert(0);
	return ' ';
}

void printVBar(){
	for(int i = 0; i < w; i++) cout << "+---";
	cout << '+' << endl;
}

void printBoard(){
	cout << endl;
	printVBar();
	for(int y = h-1; y >= 0; y--){
		cout << '|';
		for(int x = 0; x < w; x++) cout << ' ' << realBoard[y][x] << " |";
		cout << endl;
		printVBar();
	}
	cout << ' ';
	for(int x = 0; x < w; x++) cout << ' ' << (x+1) << "  ";
	cout << endl << endl; 
}

void deleteBoard(char** board){
	for(int i = 0; i < h; i++) delete [] board[i];
	delete [] board;
}

char otherTurn(char turn){
	return turn=='O'?'X':'O';
}

int play(char** board, int x, char turn){
	for(int y = 0; y < h; y++){
		if(board[y][x] == ' '){
			board[y][x] = turn;
			return y;
		}
	}
	assert(0); // playing in a full column
	return -1;
}

//1 if the player who just went is winning.
int read(char** board, char turn, int depth, int lasty, int lastx){
	if(depth < 0) return 31415926;
	double hashed = hashBoard(board);
	Cache::iterator it = cache.find(hashed);
	if(it != cache.end() && it->second != 31415926) return it->second;
	
	if(lasty != -1) {
		char winner = whoWon(board, lasty, lastx);
		if(winner != ' ') { int ret = winner==turn?1:-1; cache[hashed] = ret; return ret; }
	}

	char nextTurn = otherTurn(turn);
	int max = -1000000000;
	bool movesLeft = false, anUnknown = false;
	for(int x = 0; x < w; x++){
		if(board[h-1][x] != ' ') continue;
		movesLeft = true;
		int y = play(board, x, nextTurn);
		int eval = read(board, nextTurn, depth-1, y, x);
		board[y][x] = ' ';
		if(eval == 31415926) {cache[hashed] = 31415926; anUnknown = true;}
		else if(eval > 0) {cache[hashed] = -1; return -1;}
		else if(eval > max) max = eval;
	}
	if(anUnknown) return 31415926;
	if(!movesLeft) { cache[hashed] = 0; return 0; } // we've read to the finish of a tie game.
	cache[hashed] = -max;
	return -max;
}

int solve(char** board, char turn){
	for(int i = 10; i < 50; i++){
		cout << "Solving depth " << i << endl;
		int x = read(board,turn,i,-1,-1);
		cout << x << "Map size: " << cache.size() << endl;
		if(x != 31415926) return x;
	}
	assert(0); return 0;
}

int robotMove(char** board, char turn){
	//sleep(1);
	cache.clear();
	int val = solve(board,otherTurn(turn));
	if(val< 0) cout <<   "I'm gonna win. ";
	if(val==0) cout << "We're gonna tie. ";
	if(val> 0) cout <<   "I'm gonna lose. ";
	int spot = -1, idk=-1, max = -1000000000;
	for(int x = 0; x < w; x++) {
		cout << "    " << (x+1) << ": ";
		if(board[h-1][x] != ' ') continue;
		int y = play(board,x,turn);
		double hashed = hashBoard(board);
		board[y][x] = ' ';
		Cache::iterator it = cache.find(hashed);
		idk = x;
		if(it == cache.end() || it->second == 31415926) continue;
		int eval = it->second;
		cout << eval;
		if(eval>max){
			max = eval;
			spot = x;
		}
	}
	if(spot == -1) spot = idk; // at least play something
	cout << (1+spot) << endl;
	return spot;
}

int main(){
	createBoard();
	cout << "Player Types?" << endl;
	cin >> players;

	char turn = 'X';
	int turnNo = 0;
	
	while(true){
		int x = -1;
		printBoard();
		cout << turn << ": ";
		if(players[turnNo%2] == 'h') {cin >> x; x--;}
		if(players[turnNo%2] == 'r' || x>100) {x = robotMove(realBoard, turn);}
		if(x < 0 || x >= w || realBoard[h-1][x] != ' ') {
			cout << "invalid."  << endl;
			break;
		}
		int y = play(realBoard,x,turn);
		char win = whoWon(realBoard,y,x);
		if(win != ' '){
			printBoard();
			cout << "Game Over! " << turn << " Wins!" << endl;
			break;
		}
		turn = otherTurn(turn);
		turnNo++;
		if(turnNo == w*h){
			printBoard();
			cout << "Game Over! It's a tie!" << endl;
			break;
		}
	}

	deleteBoard(realBoard);
}
