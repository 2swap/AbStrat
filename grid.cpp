#include <iostream>
#include <iomanip>
#include <string>
using namespace std;







const int sz = 9;
int lens[44] = {4,3,3,5,4,4,3,5,5,4,
		3,6,6,8,8,7,7,9,8,8,
		6,9,9,11,10,10,9,11,11,10,
		6,9,9,11,10,10,9,11,11,10,
		5,8,8,10};
int spine[9] = {3,4,5,6,7,8,9,10,11};






bool inBounds(int y, int x){
	return x>=0 && y>=0 && x<sz && y<sz;
}
bool touch(int** grid, int y, int x, int num){//returns if num is bordering [y,x]
	for(int dy = y-1; dy < y+2; dy++)
		for(int dx = x-1; dx < x+2; dx++)
			if(inBounds(dy,dx) && grid[dy][dx] == num) return true;
	return false;
}
void grade(int** grid, int** test){
	for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++) test[y][x] = (touch(grid,y,x,lens[grid[y][x]]) || grid[y][x] == -1)?1:0;
}
void printLine(){
	cout << endl << "\t+";
	for(int i = 0; i < sz; i++) cout << "----+";
	cout << endl << "\t|";
}
void printGrid(int** grid, int** test){
	grade(grid, test);
	cout << endl << endl;
	printLine();

	int maxV = -2;
	for(int y = 0; y < sz; y++){
		for(int x = 0; x < sz; x++){
			cout << (test[y][x]==0?"#":" ");
			if(grid[y][x]>0){
				if(grid[y][x] < 10) cout << " ";
				cout<<grid[y][x];
			}
			else cout << "  ";
			cout << (test[y][x]==0?"#|":" |");
			if(grid[y][x] > maxV) maxV=grid[y][x];
		}
		printLine();
	}
	cout << "\tMax value is: " << maxV << endl << endl << endl;
}
int** makeGrid(int i){
	int** grid = new int*[sz];
	for(int y = 0; y < sz; y++){
		grid[y] = new int[sz];
		for(int x = 0; x < sz; x++) grid[y][x] = i;
	}
	return grid;
}
void delGrid(int** grid){
	for(int i = 0; i < sz; i++) delete [] grid[i];
	delete [] grid;
}

//================================================================
//================================================================


void wrongFill(int** grid){
	
	//spore
	for(int i = 0; i < 9; i++)
		for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++)
			if(grid[y][x] == -1 && touch(grid,y,x,spine[i])) grid[y][x]=-2;

	for(int i = 1; i < 44; i++){

		//if the number is already on the grid, skip it
		bool cont = false;
		for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++) if(grid[y][x] == i) cont = true;
		if(cont) continue;			
		
		//if we can find a spot that this number can go to, place.
		for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++)
			if(grid[y][x] == -2){
				grid[y][x] = i;
				x = y = 1000;//manual break
			}
	}
}
void naiveFill(int** grid){
	bool diff = true;
	while(diff){
		diff = false;
		for(int i = 1; i < 44; i++){

			//if the number is already on the grid, skip it
			bool cont = false;
			for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++) if(grid[y][x] == i) cont = true;
			if(cont) continue;			

			//if we can find a spot that this number can go to that blocks no other, place.
			for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++)
				if(grid[y][x] == -1 && touch(grid,y,x,lens[i])){
					bool place = true;
					for(int j = 0; j < 9; j++)//spine
						if(spine[j] != lens[i] && touch(grid,y,x,spine[j])) {
							place = false; 
							break;
						}
					if(place){
						grid[y][x] = i;
						diff = true;
						x = y = i = 1000;//manual break
					}
				}
		}
	}
}
void swap(int** grid, int a, int b){
	for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++){
		if(grid[y][x] == a){
			grid[y][x] = b;
			continue;
		}
		if(grid[y][x] == b) grid[y][x] = a;
	}
	
}
bool shuffle(int** grid, int** test){
	grade(grid, test);
	int y1 = -1, x1 = -1, hold = -1;
	for(int y = 0; y < sz; y++) for(int x = 0; x < sz; x++) if(test[y][x] == 0){
		if(y1 == -1){
			y1 = y; x1 = x;
			hold = grid[y][x];
		}else{
			int temp = grid[y][x];
			grid[y][x] = hold;
			hold = temp;
		}
	}
	if(y1 != -1){
		grid[y1][x1] = hold;
	}
	return y1 == -1;
}






int main(){
	int** grid = makeGrid(-1);
	int** test = makeGrid(0);
	grid[4][3] = 5;
	grid[3][2] = 4;
	grid[2][1] = 9;
	grid[3][4] = 3;
	grid[2][5] = 6;
	grid[4][5] = 10;
	grid[1][6] = 11;
	grid[5][2] = 8;
	grid[5][4] = 7;
	naiveFill(grid);
        wrongFill(grid);
	for(int i = 0; i < 100; i++) if(shuffle(grid, test)) break;
	printGrid(grid, test);
	delGrid(grid);
	delGrid(test);
}
