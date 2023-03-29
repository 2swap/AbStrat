#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <string>
using namespace std;

const int SEQ = 3;
const int LENGTH = SEQ*SEQ;

int _lis(int arr[], int n, int* max_ref)
{
    if (n == 1)
        return 1;
 
    int res, max_ending_here = 1;
 
    for (int i = 1; i < n; i++) {
        res = _lis(arr, i, max_ref);
        if (arr[i - 1] < arr[n - 1]
            && res + 1 > max_ending_here)
            max_ending_here = res + 1;
    }
 
    if (*max_ref < max_ending_here)
        *max_ref = max_ending_here;
 
    return max_ending_here;
}
 
int lis(int arr[], int n)
{
    int max = 1;
    _lis(arr, n, &max);
    return max;
}

bool is_valid(int list[]){
	if(lis(list, LENGTH)>SEQ) return false;
	int arr[LENGTH];
	for(int i = 0; i < LENGTH; i++){
		arr[i] = LENGTH+1-list[i];
	}
	if(lis(arr, LENGTH)>SEQ)return false;
	return true;
}

int main(int argcount, char** args){
	int count = 0;
	int fac = 1;
	for(int i = 1; i <= LENGTH; i++)
		fac *= i;
	for(int i = 0; i < fac; i++){
		int arr[LENGTH];
		int code = i;
		for(int j = 0; j < LENGTH; j++){
			arr[j] = 0;
		}
		for(int j = LENGTH; j > 0; j--){
			int index = code % j;
			code /= j;
			for(int k = 0; k < LENGTH; k++){
				if(arr[k] != 0)
					continue;
				if(index == 0){
					arr[k] = j;
					break;
				}
				index--;
			}
		}
		if(is_valid(arr)){
			count++;
			for(int j = 0; j < LENGTH; j++)
				cout << arr[j];
			cout << endl;
		}
	}
	cout << count << " solutions" << endl;
}

