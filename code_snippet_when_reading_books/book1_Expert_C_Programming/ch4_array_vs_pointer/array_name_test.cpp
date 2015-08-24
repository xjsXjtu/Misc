#include <iostream>
using namespace std;

int main()
{
	char buf[256] = {0};

	// all of them are the same to the start address of the array
    cout << "buf    :" << (unsigned int)buf << endl;
    cout << "&buf   :" << (unsigned int)&buf << endl;
    cout << "&buf[0]:" << (unsigned int)&(buf[0]) << endl;

	// compile error: '++' needs l-value
	// cout << "buf++  :" << (unsigned int)(buf++) << endl;
    
	system("pause");
    return 0;
}