#include <stdio.h>
#include <stdlib.h>

int main()
{
	char buf[32] = {0};
	unsigned int sz = sizeof(buf);
	int i1 = -1;

	printf("unsigned int sz = %u, int i1 = %d\n\n", sz, i1);
	printf("i1 < sz			: %d\n", i1 < sz);		// false !!!!
	printf("i1 < (int)sz	: %d\n", i1 < (int)sz); // true

	system("pause");
	return 0;
}