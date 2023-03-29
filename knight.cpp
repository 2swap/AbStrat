#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
#include <map>
using namespace std;
char alph [4] = {' ','|','-','+'};
int width = 3, height = 3;
int legalmoves [16] = {2, 1, 1, 2, -1, 2, -2, 1, -2, -1, -1, -2, 1, -2, 2, -1};

bool** createBoard(){
	bool** board = new bool*[height];
	for(int i = 0; i < height; i++) board[i] = new bool[width];
	return board;
}

bool** copyBoard(bool** copy){
	bool** board = new bool*[height];
	for(int i = 0; i < height; i++){
		board[i] = new bool[width];
		for(int j = 0; j < width; j++)
			board[i][j] = copy[i][j];
	}
	return board;
}

char charAt(bool** board, int y, int x){
	int sum = 0;
	if(y>=height||y<0) sum+=2;
	if(x>=width||x<0) sum+=1;
	if(sum>0) return alph[sum];
	return board[y][x]?'X':' ';
}

void printBoard(bool** board){
	cout << endl;
	for(int y = -1; y <= height; y++){
		cout << ' ' << (char)(y>=0&&y<height?('a'+y):' ');
		for(int x = -1; x <= width; x++) cout << charAt(board, y,x);
		cout << endl;
	}
	cout << "   ";
	for(int x = 0; x < width; x++) cout << (x+1);
	cout << endl << endl; 
}

void deleteBoard(bool** board){
	for(int i = 0; i < height; i++) delete [] board[i];
	delete [] board;
}

int read(bool** board, int y, int x, int moves){
	if(y == 0 && x == 0 && moves == width * height){
		printBoard(board);
		return true;
	}
	if(y == 0 && x == 0 && moves > 0){
		return false;
	}
	for(int i = 0; i < 8; i++){
		int ny = y+legalmoves[i*2];
		int nx = x+legalmoves[i*2+1];
		if(ny<0 || ny>=height || nx<0 || nx >= width) continue;
		if(board[ny][nx]) continue;
		bool** copy = copyBoard(board);
		copy[ny][nx] = true;
		bool red = read(copy, ny, nx, moves+1);
		deleteBoard(copy);
		if(red) {
			usleep(500000);
			printBoard(board);
			return true;
		}
	}
	return false;
}

int main(){
	cout << "Please enter the board height." << endl;
	cin >> height;
	if(height>19) {cout<<"Too Big!"; exit(0);}
	cout << "Please enter the board width." << endl;
	cin >> width;
	if(width>19) {cout<<"Too Big!"; exit(0);}
	bool** board = createBoard();

	if(!read(board, 0, 0, 0))
		cout << "No solution";

	deleteBoard(board);
}
