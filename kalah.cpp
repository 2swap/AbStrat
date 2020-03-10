#include <iostream>
#include <cassert>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <map>
using namespace std;
int* realBoard;
char alph [4] = {' ','|','-','+'};
string players;
int m=6, n=1, h=m*2+2;

int* createBoard(){
	int* board = new int*[m*2+2];
	for(int i = 0; i < h; ++i) if(i != m && i != m*2+1) board[y] = n;
	return board;
}

int* copyBoard(int* copy){
	int* board = new int*[h];
	for (int i = 0; i < h; ++i) board[i] = copy[i];
	return board;
}

bool isComplete(int* board){
	return board[m]+board[2*m+1]==n*m*2;
}

int heuristic(int* board){
	return board[m]-board[2*m+1];
}

char whoWon(int* board){
	if (!isComplete(board)) return ' '; // Game isn't over!
	if (board[m]<board[m*2+1]) return 'N'; // North (Second Player) won!
	if (board[m]>board[m*2+1]) return 'S'; // South (First Player) won!
	return 'T'; // It's a complete tie game!
}

void printVBar(int ct){
	for(int i = 0; i < ct; i++) cout << "+---";
	cout << '+';
}

void printBoard(int* board){
	cout << endl;


	printVBar(m+2);

	cout << "+   + ";
	for(int x = 2*m; x > m; --x) cout << ' ' << board[x] << " +";
	cout << endl;

	cout << "+ " << board[2m+1] << " +";
	printVBar(m);
	cout << "+ " << board[m] << " +" << endl;

	cout << "+   + ";
	for(int x = 0; x < m; ++x) cout << ' ' << board[x] << " +";
	cout << endl;

	printVBar(m+2);


	cout << endl << ' ';
	for(int x = 0; x < w; x++) cout << ' ' << (x+1) << "  ";
	cout << endl << endl; 
}

void deleteBoard(int* board){
	delete [] board;
}

void play(int* board, int x){
	assert(x != m && x != 2*m+1);
	int ct = board[x];
	int hand = x;
	while(ct > 0){
		hand++;
		board[hand%(2*m+2)]++;
		ct--;
	}
}

//1 if the player who just went is winning.
int alphabeta(int* board, int depth, double alpha, double beta, bool turn){
	if(depth == 0 || isComplete(board)) return heuristic(board);
	int value;
	if(turn){
		value = -10000;
		for(int i = 0; i < m; i++){
			if(board[m] == 0) continue;
			value = max(value, alphabeta(child, depth-1, alpha, beta, false));
			alpha = max(alpha, value);
			if(alpha>=beta) break;
		}
	}
	else{
		value = 10000;
		for(int i = m+1; i < 2*m+1; i++){
			value = min(value, alphabeta(child, depth-1, alpha, beta, true));
			beta = min(beta, value);
			if(alpha>=beta) break;
		}
	}
	return value;
}//call: alphabeta(origin, depth, -inf, +inf, ?true?)

int robotMove(int* board, char turn, int depth){
	//sleep(1);
	//cache.clear();
	int max = -1000000;
	int spot = -1;
	for(int x = 0; x < w; x++) {
		if(board[h-1][x] != ' ') continue;
		int* playHere = copyBoard(board);
		play(playHere,x,turn);
		int eval = evaluate(playHere, turn, depth);
		deleteBoard(playHere);
		cout << " " << eval << " ";
		if(eval>max){
			max = eval;
			spot = x;
		}
	}
	if(max> 0) cout <<   "I'm gonna win. "  << (1+spot) << endl;
	if(max==0) cout << "We're gonna tie. "  << (1+spot) << endl;
	if(max< 0) cout <<   "I'm gonna lose. " << (1+spot) << endl;
	return spot;
}

int main(){
	createBoard();
	cout << "Player Types?" << endl;
	cin >> players;

	bool turn = true;
	
	while(true){
		int x = -1;
		printBoard();
		cout << turn << ": ";
		if(players[turnNo%2] == 'h') {cin >> x; x--;}
		if(players[turnNo%2] == 'r' || x>100) {x = robotMove(realBoard, turn, 0);}
		if(x < 0 || x >= w || realBoard[h-1][x] != ' ') {
			cout << "invalid."  << endl;
			break;
		}
		play(realBoard,x,turn);
		char win = whoWon(realBoard);
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
