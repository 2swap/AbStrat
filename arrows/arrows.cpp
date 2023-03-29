#include <iostream>
#include <cmath>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <fstream>
using namespace std;



int mindepth = 0;

struct Board
{
	char** grid;
	int width;
	int height;
	int space_pos_x;
	int space_pos_y;
	int energy;
};



// 0
//3 1
// 2

int move_to_y(int move){
	if(move == 2)return 1;
	if(move == 0)return -1;
	return 0;

}
int move_to_x(int move){
	if(move == 1)return 1;
	if(move == 3)return -1;
	return 0;
}

char move_to_arrow(int move){
	if(move == 0)return 'v';
	if(move == 1)return '<';
	if(move == 2)return '^';
	if(move == 3)return '>';
	return '$';
}

int not_in_grid(int xy, int bound){
	return xy < 0 || xy >= bound;
}

bool apply_move(Board* board, int move){
	if(move < 0 || move > 3) return false;
	char expected_arrow = move_to_arrow(move);
	board->grid[board->space_pos_y][board->space_pos_x] = expected_arrow;

	for(int energy = 1; energy < 3; energy++){
		board->space_pos_x += move_to_x(move);
		board->space_pos_y += move_to_y(move);
	
		if(not_in_grid(board->space_pos_x, board->width) || not_in_grid(board->space_pos_y, board->height))
			return false;
		if(board->grid[board->space_pos_y][board->space_pos_x] == expected_arrow){
			board->grid[board->space_pos_y][board->space_pos_x] = ' ';
			board->energy -= energy;
			return true;
		}
	}
	return false;
}

char** string_to_grid(string s, int height, int width){
	char** ary = new char*[height];
	for(int y = 0; y < height; ++y) {
		ary[y] = new char[width];
		for(int x = 0; x < width; ++x) {
			ary[y][x] = s[y*width+x];
		}
	}
	return ary;
}

void print_board(Board* b){
	cout << endl;
	for(int y = 0; y < b->height; ++y) {
		for(int x = 0; x < b->width; ++x) {
			cout << b->grid[y][x];
		}
		cout << endl;
	}
}

void delete_board(Board* b){
	for(int i = 0; i < b->height; ++i) {
		delete [] b->grid[i];
	}
	delete [] b->grid;
	delete b;
}

Board* copy_board(Board* old_board){
	Board* new_board = new Board;
	char** ary = new char*[old_board->height];
	for(int y = 0; y < old_board->height; ++y) {
		ary[y] = new char[old_board->width];
		for(int x = 0; x < old_board->width; ++x) {
			ary[y][x] = old_board->grid[y][x];
		}
	}
	new_board->grid = ary;
	new_board->width = old_board->width;
	new_board->height = old_board->height;
	new_board->space_pos_y = old_board->space_pos_y;
	new_board->space_pos_x = old_board->space_pos_x;
	new_board->energy = old_board->energy;
	return new_board;
}

bool recurse(Board* board){
	if(board->energy == 0){
		cout << "solved" << endl;
		print_board(board);
		return true;
	}
	for(int i = 0; i < 4; i++){
		Board* new_board = copy_board(board);
		if(apply_move(new_board, i)){
			if(recurse(new_board)){
				print_board(board);
				delete_board(new_board);
				return true;
			}
		}
		delete_board(new_board);
	}
	return false;
}

bool human(Board* board){
	print_board(board);
	if(board->energy == 0){
		cout << "solved" << endl;
		return true;
	}
	char in = 'q';
	cin >> in;
	char arrowkeys[] = "sawd";
	char* ptr = strchr(arrowkeys, in);
	int i = ptr - arrowkeys;
	Board* new_board = copy_board(board);
	if(apply_move(new_board, i))
		human(new_board);
	else
		human(board);
	delete_board(new_board);
}

void initialize_energy(Board* board){
	int energy = 0;
	for(int y = 0; y < board->height; y++)
		for(int x = 0; x < board->width; x++){
			char arrow = board->grid[y][x];
			int move = 0;
			for(move; move < 4; move++){
				if(move_to_arrow(move) == arrow)
					break;
			}
			if(move == 4) continue;
			int dx = -move_to_x(move);
			int dy = -move_to_y(move);
			int i = 0;
			while(true){
				i++;
				int nx = x + dx * i;
				int ny = y + dy * i;
				if(not_in_grid(nx, board->width) || not_in_grid(ny, board->height) || board->grid[ny][nx] == '#')
					break;
				if(board->grid[ny][nx] == arrow)
					energy--;
			}
			energy += i - 1;
		}
	board->energy = energy;
}

void initialize_space_pos(Board* board){
	for(int y = 0; y < board->height; y++)
		for(int x = 0; x < board->width; x++)
			if(board->grid[y][x] == ' '){
				board->space_pos_y = y;
				board->space_pos_x = x;
				return;
			}
}

Board* load_board(string path){
	Board* board = new Board();
	board->width = 0;
	board->height = 0;

	string line = "";
	string gridtext = "";
	ifstream f(path.c_str());
	while (getline(f, line)) {
		gridtext += line;
		board->width = line.size();
		board->height++;
	}
	f.close();

	board->grid = string_to_grid(gridtext, board->height, board->width);

	initialize_space_pos(board);
	initialize_energy(board);
	return board;
}

int main(int argcount, char** args){
	if(argcount != 3 || args[1][0] != '-') {
		cout << "2 args expected:" << endl;
		cout << "-h(uman)/-r(obot) input.arr" << endl;
		return 1;
	}

	Board* board = load_board(args[2]);
	cout << "searching" << endl;
	if(args[1][1] == 'r')
		recurse(board);
	else if(args[1][1] == 'h')
		human(board);
	else
		cout << "Bad user-type flag." << endl;
	delete_board(board);
}

