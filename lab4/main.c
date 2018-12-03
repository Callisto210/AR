#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>
#include <string.h>

int cmpfunc_asc(const void * a, const void * b) {
	return ( *(int*)a - *(int*)b );
}

int cmpfunc_desc(const void * a, const void * b) {
	return ( *(int*)b - *(int*)a );
}

void merge_lesser(int *result, int *a, int *b, size_t size) {
	size_t i, j=0, k=0;

	for (i=0; i < size*2; i++) {
		if (j >= size) {
			result[i] = b[k++];
			continue;
		}
		if (k >= size) {
			result[i] = a[j++];
			continue;
		}
		if (a[j] < b[k])
			result[i] = a[j++];
		else
			result[i] = b[k++];
	}

	printf("%s a[]: ", __func__);
	for (i=0; i < size; i++)
		printf("%d ", a[i]);
	printf("\n");
	
	printf("%s b[]: ", __func__);
	for (i=0; i < size; i++)
		printf("%d ", b[i]);
	printf("\n");

	printf("%s result[]: ", __func__);
	for (i=0; i < 2*size; i++)
		printf("%d ", result[i]);
	printf("\n");
}

void merge_greater(int *result, int *a, int *b, size_t size) {
	int i, j=size-1, k=size-1;

	for (i=0; i < 2*size; i++) {
		if (j < 0) {
			result[i] = b[k--];
			continue;
		}
		if (k < 0) {
			result[i] = a[j--];
			continue;
		}
		if (a[j] > b[k])
			result[i] = a[j--];
		else
			result[i] = b[k--];
	}

	printf("%s a[]: ", __func__);
	for (i=0; i < size; i++)
		printf("%d ", a[i]);
	printf("\n");
	
	printf("%s b[]: ", __func__);
	for (i=0; i < size; i++)
		printf("%d ", b[i]);
	printf("\n");

	printf("%s result[]: ", __func__);
	for (i=0; i < 2*size; i++)
		printf("%d ", result[i]);
	printf("\n");
}

int two_to_power[] = {1, 2, 4, 8, 16};
int cpus_to_dim[] = {0, 0, 1, 2, 2, 3, 3, 3, 3};

int main(int argc, char** argv) {
	int world_rank, partner;
	int world_size;	
	int n;
	int i, m;
	int array_size;
	int *array = NULL;
	int sub_array_size;
	int *sub_array, *foreign_sub_array, *result_array, *tmp;
	double ttime;

	MPI_Init(&argc, &argv);
	MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
	MPI_Comm_size(MPI_COMM_WORLD, &world_size);
	
	if (world_rank == 0) {
		n = atoi(argv[1]);
		array = malloc(n * sizeof(int));
		srand(time(NULL));
		for(i = 0; i < n; i++) {
			array[i] = rand() % n;
		}
	}

	/* Broadcast number of elements to others */
	MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
	//printf("Number of all elements %d\n", n);

	sub_array_size = n/world_size;

	sub_array = malloc( 2 * sub_array_size * sizeof(int));
	foreign_sub_array = malloc(sub_array_size * sizeof(int));
	result_array = malloc(2 * sub_array_size * sizeof(int));

	/* Send part of array to processes */
	MPI_Scatter(array, sub_array_size, MPI_INT, sub_array, sub_array_size, MPI_INT, 0, MPI_COMM_WORLD);

	if (world_rank == 0) {
		free(array);
	}

	ttime -= MPI_Wtime();
#if 0
	for (int i = 0; i < world_size; i++) {
		MPI_Barrier(MPI_COMM_WORLD);
		if (i == world_rank) {
			printf("CPU %d: ", world_rank);
			for (m = 0; m < sub_array_size; m++) {
				printf("%d ", sub_array[m]);
				fflush(stdout);
			}
			printf("\n");
		}
	}
#endif

	qsort(sub_array, sub_array_size, sizeof(*sub_array), (world_rank % 2) ? cmpfunc_desc : cmpfunc_asc);

#if 0
	for (int i = 0; i < world_size; i++) {
		MPI_Barrier(MPI_COMM_WORLD);
		if (i == world_rank) {
			printf("CPU %d: ", world_rank);
			for (m = 0; m < sub_array_size; m++) {
				printf("%d ", sub_array[m]);
				fflush(stdout);
			}
			printf("\n");
		}
	}
	printf("\n");
#endif

	/* Perform merge */
	for (i=1; i<=cpus_to_dim[world_size]; i++) {
		MPI_Barrier(MPI_COMM_WORLD);
		for (m=i-1; m>=0; m--) {
			partner = world_rank ^ (1 << m);
			if (partner < world_size) {
				/* Perform compare & exchange */
				MPI_Sendrecv(	sub_array, sub_array_size, MPI_INT, partner, i*cpus_to_dim[world_size]+m,
						sub_array + sub_array_size, sub_array_size, MPI_INT, partner, i*cpus_to_dim[world_size]+m,
						MPI_COMM_WORLD, MPI_STATUS_IGNORE);
				//printf("CPU %d to %d i=%d m=%d\n", world_rank, partner, i, m);
				qsort(sub_array, 2*sub_array_size, sizeof(*sub_array), (world_rank && (1 << i)) ? cmpfunc_desc : cmpfunc_asc);

				if (world_rank && (1 << m))
					memcpy(sub_array, sub_array + sub_array_size, sub_array_size);

			}

#if 0
			for (int i = 0; i < world_size; i++) {
				MPI_Barrier(MPI_COMM_WORLD);
				if (i == world_rank) {
					printf("CPU %d: ", world_rank);
					for (int m = 0; m < sub_array_size; m++) {
						printf("%d ", sub_array[m]);
						fflush(stdout);
					}
					printf("\n");
				}
			}
			printf("\n");
#endif
		}
	}

#if 0
	for (int i = 0; i < world_size; i++) {
		MPI_Barrier(MPI_COMM_WORLD);
		if (i == world_rank) {
			printf("CPU %d: ", world_rank);
			for (m = 0; m < sub_array_size; m++) {
				printf("%d ", sub_array[m]);
				fflush(stdout);
			}
			printf("\n");
		}
	}
#endif
	ttime += MPI_Wtime();

        if (world_rank == 0)
                printf("%d, %d, %.10f\n", n, world_size, ttime);
	MPI_Finalize();
	return (0);

}
