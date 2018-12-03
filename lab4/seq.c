#include <stdlib.h>
#include <stdio.h>
#include <time.h>

int cmpfunc_asc(const void * a, const void * b) {
	return ( *(int*)a - *(int*)b );
}

int main(int argc, char **argv) {
	int n, i;
	int *array;
	clock_t ttime;

	n = atoi(argv[1]);
	array = malloc(n * sizeof(int));
	srand(time(NULL));
	for(i = 0; i < n; i++) {
		array[i] = rand() % n;
	}

	ttime = -clock();
	qsort(array, n, sizeof(*array), cmpfunc_asc);
	ttime += clock();

	printf("%d, 1, %.10f\n", n, (double)ttime/(double)CLOCKS_PER_SEC);	

}
