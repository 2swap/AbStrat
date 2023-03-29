#include <cstdlib>
#include <iostream>

int main(){
int A = std::rand();
int B = std::rand();
std::cout << A << " " << B << std::endl;
B^=(A^=(B^=A));
std::cout << B << " " << A << std::endl;
return 0;
}
