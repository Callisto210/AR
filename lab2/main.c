#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NUMBER_OF_ITERATIONS (5000)
#define NUMBER_OF_TESTS (10)

#define G (1000.0)
#define LAMBDA (37.0)
#define COEF (G/LAMBDA)


int main(int argc, char** argv) {
	int rank, size;
	int net_size, rows;
	int up, down;
	double **net_chunk;
	double time;

	if (argc < 2) {
		printf("No arguments\n");
		return (0);
	}

	net_size = atoi(argv[1]);
	time = 0.0;

	MPI_Init(&argc, &argv);

	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

	rows = net_size/size + ((rank < net_size % size) ? 1 : 0);

	/* Allocate 2 more rows to data exchange */
	net_chunk = (double **)malloc((rows+2) * sizeof(double *));
	for (int i=0; i < rows+2; i++)
		net_chunk[i] = (double *)malloc(net_size * sizeof(double));
	
	/* Obtain neighbours. Use MPI_PROC_NULL to avoid checking */	
	down = (rank + 1 < size) ? rank + 1 : MPI_PROC_NULL;
	up = (rank - 1 >= 0) ? rank - 1 : MPI_PROC_NULL;

	for (int t=0; t < NUMBER_OF_TESTS; t++) {
		time -= MPI_Wtime();

		for (int i=0; i < rows+2; i++)
			memset(net_chunk[i], 0, net_size * sizeof(double));

		/* In one iteration we are computing only half of points */
		for (int i=0; i<NUMBER_OF_ITERATIONS*2; i++) {
			/* Communicate */
			if ((rank % 2) == 0) {
				/* Even chunks sends data down */
				MPI_Sendrecv(	net_chunk[rows], net_size, MPI_DOUBLE, down, 0,
						net_chunk[rows+1], net_size, MPI_DOUBLE, down, 0,
						MPI_COMM_WORLD, MPI_STATUS_IGNORE);
				/* Even chunks sends data up */
				MPI_Sendrecv(	net_chunk[1], net_size, MPI_DOUBLE, up, 1,
						net_chunk[0], net_size, MPI_DOUBLE, up, 1,
						MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			} else {
				/* Odd chunks sends data up */
				MPI_Sendrecv(	net_chunk[1], net_size, MPI_DOUBLE, up, 0,
						net_chunk[0], net_size, MPI_DOUBLE, up, 0,
						MPI_COMM_WORLD, MPI_STATUS_IGNORE);
				/* Odd chunks sends data down */
				MPI_Sendrecv(	net_chunk[rows], net_size, MPI_DOUBLE, down, 1,
						net_chunk[rows+1], net_size, MPI_DOUBLE, down, 1,
						MPI_COMM_WORLD, MPI_STATUS_IGNORE);
			}

			/* Perform calculations */
			for (int j=1; j<rows+1; j++) {
				for (int k=(i+j) % 2; k<net_size; k+=2) {
					if (k == 0) { /* Lack of left element assuming 0 */
						net_chunk[j][k] = (	net_chunk[j-1][k] +
									net_chunk[j+1][k] +
									net_chunk[j][k+1] +
									(COEF/((double)net_size*(double)net_size)))/4;
					} else if (k == (net_size - 1)) { /* Lack of right element assuming 0 */
						net_chunk[j][k] = (	net_chunk[j-1][k] +
									net_chunk[j+1][k] +
									net_chunk[j][k-1] +
									(COEF/((double)net_size*(double)net_size)))/4;
					} else {
						net_chunk[j][k] = (	net_chunk[j-1][k] +
									net_chunk[j+1][k] +
									net_chunk[j][k-1] +
									net_chunk[j][k+1] +
									(COEF/((double)net_size*(double)net_size)))/4;
					}
				}
			}
		}

		time += MPI_Wtime();
	}
#if 0
	for (int cpu = 0; cpu < size; cpu++) {
		MPI_Barrier(MPI_COMM_WORLD);
		if (cpu != rank)
			continue;
		printf("CPU: %d\n", rank);
		printf("%d, %.10f\n", net_size, time/(double)NUMBER_OF_TESTS);
		for (int i = 1; i < rows+1; i++) {
			for (int j = 0; j < net_size; j++)
				printf ("%.2f ", net_chunk[i][j]);
			printf("\n");
		}
	}
#else
	if (rank == 0)
		printf("%d, %d, %.10f\n", net_size, size, time/(double)NUMBER_OF_TESTS);
#endif

	for (int i=0; i < rows+2; i++)
		free(net_chunk[i]);
	free(net_chunk);

	MPI_Finalize();

	return (0);
}
