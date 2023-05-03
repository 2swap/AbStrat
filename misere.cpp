#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <map>
using namespace std;
map<double,bool> cache;
bool** realBoard;
char alph [4] = {' ','|','-','+'};
string players;
int sz = 3, len = 3;

double hashy(bool** board){
	int k = sz-1;
	double sums [8] = {0,0,0,0,0,0,0,0};
	double cur = 1.0;
	for(int i = 0; i < sz; i++) for(int j = 0; j < sz; j++){
		if(board[i][j])     sums[0]+=cur;
		if(board[j][i])     sums[1]+=cur;
		if(board[k-i][j])   sums[2]+=cur;
		if(board[k-j][i])   sums[3]+=cur;
		if(board[i][k-j])   sums[4]+=cur;
		if(board[j][k-i])   sums[5]+=cur;
		if(board[k-i][k-j]) sums[6]+=cur;
		if(board[k-j][k-i]) sums[7]+=cur;
		cur/=2;
	}
	for(int i = 1; i < 8; i++) if(sums[i]>sums[0])sums[0]=sums[i];
	return sums[0];
}

void createBoard(){
	realBoard = new bool*[sz];
	for(int i = 0; i < sz; i++) realBoard[i] = new bool[sz];
}

bool** copyBoard(bool** copy){
	bool** board = new bool*[sz];
	for(int i = 0; i < sz; i++){
		board[i] = new bool[sz];
		for(int j = 0; j < sz; j++)
			board[i][j] = copy[i][j];
	}
	return board;
}

bool isDead(bool** board){
	for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++){
		int sumH = 0, sumV = 0, sumD = 0, sumR = 0;
		for(int i = 0; i < len; i++){
			if(x+len<=sz) sumH+=board[y][x+i];
			if(y+len<=sz) sumV+=board[y+i][x];
			if(x+len<=sz && y+len<=sz){
				sumD+=board[y+i][x+i];
				sumR+=board[y+len-i-1][x+i];
			}
		}
		if(sumD==len||sumR==len||sumH==len||sumV==len) return true;
	}
	return false;
}

char charAt(int y, int x){
	int sum = 0;
	if(y>=sz||y<0) sum+=2;
	if(x>=sz||x<0) sum+=1;
	if(sum>0) return alph[sum];
	return realBoard[y][x]?'X':' ';
}

void printBoard(){
	cout << endl;
	for(int y = -1; y <= sz; y++){
		cout << ' ' << (char)(y>=0&&y<sz?('a'+y):' ');
		for(int x = -1; x <= sz; x++) cout << charAt(y,x);
		cout << endl;
	}
	cout << "   ";
	for(int x = 0; x < sz; x++) cout << (x+1);
	cout << endl << endl; 
}

void deleteBoard(bool** board){
	for(int i = 0; i < sz; i++) delete [] board[i];
	delete [] board;
}

int isGood(bool** board){
	double hashed = hashy(board);
	map<double,bool>::iterator it = cache.find(hashed);
	if(it != cache.end()) return it->second;
	if(isDead(board)){
		//cache[hashed] = false;
		return false;
	}
	for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++){
		if(board[y][x]) continue;
		bool** copy = copyBoard(board);
		copy[y][x] = true;
		if(isGood(copy)) {
			cache[hashed] = false;
			return false;
		}
	}
	cache[hashed] = true;
	return true;
}

string robotMove(bool** board){
	sleep(1);
	int I = -1, J = 0;
	for(int i = 0; i < sz; i++) for(int j = 0; j < sz; j++){
		if(board[i][j]) continue;
		bool** playHere = copyBoard(board);
		playHere[i][j] = true;
		if(isGood(playHere)){
			string p1(1,i+'a');
			string p2(1,j+'1');
			deleteBoard(playHere);
			return p1+p2+", I'm gonna win.";
		}
		if(!isDead(playHere)) {I=i;J=j;}
		if(I==-1) {I=i;J=j;}
		deleteBoard(playHere);
	}
	string p1(1,I+'a');
	string p2(1,J+'1');
	return p1+p2+", I'm gonna lose.";
}

int main(){
	cout << "Please enter the board size you'd like to play." << endl;
	cin >> sz;
	if(sz>9) {cout<<"Too Big!"; exit(0);}
	createBoard();
	cout << "Please enter the length of a connection." << endl;
	cin >> len;
	cout << "Player Types?" << endl;
	cin >> players;

	int turnNo = 0;
	
	while(true){
		string move;
		printBoard();
		if(players[turnNo%2] == 'r') {move = robotMove(realBoard); cout << move << endl;}
		else cin >> move;
		turnNo++;
		int y = move[0] - 'a';
		int x = move[1] - '1';
		if(x < 0 || realBoard[y][x]) {
			cout << "Game Over! Player " << (turnNo%2+1) << " Resigned!"  << endl;
			break;
		}
		realBoard[y][x] = true;
		if(isDead(realBoard)){
			printBoard();
			cout << "Game Over! Player " << (turnNo%2+1) << " Wins!"  << endl;
			break;
		}
	}

	deleteBoard(realBoard);
}
