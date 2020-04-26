#include <iostream>
#include <cassert>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <map>

using namespace std;

int* realBoard;

const char alph [4] = {' ','|','-','+'};
string players;

const int m=6;						// holes per side
const int n=1;						// counters per hole
const int h=m*2+2;					// total number of pits in board
const int northsKalahah = m*2+1;	// Array index of North's large pit
const int southsKalahah = m;		// Array index of South's large pit
const int totalStones = n*m*2;		// Amount of stones on board in total




//MATH
//MATH
//MATH
//MATH
//MATH

// Returns whether index x is a kalahah or not
bool isKalahah(int x){
	return x == northsKalahah || x == southsKalahah;
}

// Returns whether index x is a small south pit or kalahah
bool isSouthSide(int x){
	return x < southsKalahah;
}

// Returns whether index x is a small south pit or kalahah
bool isNorthSide(int x){
	return x > southsKalahah && x < northsKalahah;
}







//BOARDS
//BOARDS
//BOARDS
//BOARDS
//BOARDS

// Makes an empty board
int* createBoard(){
	int* board = new int[h];
	for(int i = 0; i < h; ++i) if(!isKalahah(i)) board[i] = n;
	return board;
}

// Safely deletes a board
void deleteBoard(int* board){
	delete [] board;
}

// Returns a deep copy of the input board
int* copyBoard(int* copy){
	int* board = new int[h];
	for (int i = 0; i < h; ++i) board[i] = copy[i];
	return board;
}

// Is the game over?
bool isComplete(int* board){
	return board[southsKalahah] + board[northsKalahah] == totalStones;
}

// Heuristic in which positive favors South
int heuristic(int* board){
	return board[southsKalahah] - board[northsKalahah];
}

// Says the winner
char whoWon(int* board){
	if (!isComplete(board)) return ' '; // Game isn't over!
	if (board[southsKalahah]>board[northsKalahah]) return 'S'; // South ( First Player) won!
	if (board[southsKalahah]<board[northsKalahah]) return 'N'; // North (Second Player) won!
	return 'T'; // It's a complete tie game!
}

// Prints a bar without newlines. ct=2 --> +---+---+
void printVBar(int ct){
	for(int i = 0; i < ct; ++i) cout << "+---";
	cout << '+';
}

// Prints a nice looking ascii board
void printBoard(int* board){
	cout << endl;

	printVBar(m+2);

	cout << "+   + ";
	for(int x = 2*m; x > m; --x) cout << ' ' << board[x] << " +";
	cout << endl;

	cout << "+ " << board[northsKalahah] << " +";
	printVBar(m);
	cout << "+ " << board[southsKalahah] << " +" << endl;

	cout << "+   + ";
	for(int x = 0; x < m; ++x) cout << ' ' << board[x] << " +";
	cout << endl;

	printVBar(m+2);

	cout << endl << ' ';
	for(int x = 0; x < m; x++) cout << ' ' << (x+1) << "  ";
	cout << endl << endl; 
}

// Picks up the stones at location x and plays them.
void play(int* board, int x, bool turn){

	// You can't play from the kalahahs
	assert(x != northsKalahah && x != southsKalahah);
	
	// You must play from your own side
	if( turn) assert(isSouthSide(x));
	if(!turn) assert(isNorthSide(x));

	int ct = board[x];
	int hand = x;
	while(ct > 0){
		hand=(hand+1)%h;
		if(hand == (turn?northsKalahah:southsKalahah)) hand=(hand+1)%h; // Don't place in opponent's kalahah
		board[hand]++;
		ct--;
	}

	// Capture
	if(!isKalahah(hand) && board[hand]==1 && board[(hand+h/2)%h]!=0){
		board[hand] = 0;
		board[(turn?southsKalahah:northsKalahah)] += 1+board[(hand+h/2)%h];
		board[(hand+h/2)%h] = 0;
	}
}

// 1 if the player who just went is winning.
int alphabeta(int* board, int depth, double alpha, double beta, bool turn){
	if(depth == 0 || isComplete(board)) return heuristic(board);
	double value;
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
	sleep(1);
	int max = -100000;
	int spot = -1;
	for(int x = 0; x < m; x++) {
		if (board[x] != ' ') continue;
		int* playHere = copyBoard(board);
		play(playHere,x,turn);
		int eval = alphabeta(playHere, depth, -100000000, 100000000, turn);
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

	//true  == first to move  == south
	//false == second to move == north
	bool turn = true;
	
	while(true){
		int x = -1;
		printBoard(realBoard);
		cout << turn << ": ";
		if(players[turn] == 'h') {cin >> x; x--;}
		if(players[turn] == 'r' || x>100) {x = robotMove(realBoard, turn, 0);}
		if(x < 0 || x >= h || realBoard[x] != ' ') {
			cout << "invalid."  << endl;
			break;
		}
		play(realBoard,x,turn);
		char win = whoWon(realBoard);
		if(win != ' '){
			printBoard(realBoard);
			cout << "Game Over! " << (players[turn]==h?"Human":"Robot") << " Wins!" << endl;
			break;
		}
		turn = !turn;
	}

	deleteBoard(realBoard);
}
