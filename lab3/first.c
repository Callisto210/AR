#include <mpi.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#define G 6.6740831e-11
#define NUMBER_OF_TESTS (1)

struct star {
	long long x;
	long long y;
	long long z;
	long long m;
	double ax;
	double ay;
	double az;
};

int main(int argc, char** argv) {
	int rank, size;
	int next, prev;
	unsigned long stars, i, j, tmp, other_stars_n;
	struct star *universe, *other_stars, *other_stars_second, *other_stars_tmp;
	double d, time;
	int cpu;

	MPI_Init(&argc, &argv);

	MPI_Comm_rank(MPI_COMM_WORLD, &rank);
	MPI_Comm_size(MPI_COMM_WORLD, &size);

	if (rank == 0) {
		FILE *data = fopen("input.txt", "r");

		fscanf(data, "%zu", &stars);
		universe = malloc(((stars/size) + ((0 < stars % size) ? 1 : 0)) * sizeof(*universe));

		printf("Stars in file %ld\n", stars);

		/* Propagate number of stars to processor */
		for (j = 1; j < size; j++) {
			tmp = stars/size + ((j < stars % size) ? 1 : 0);
			MPI_Send(&tmp, 1, MPI_UNSIGNED_LONG, j, 0, MPI_COMM_WORLD);

			for (i = 0; i < tmp; i++) {
				fscanf(data, "%lld; %lld; %lld; %lld",
				    &universe[i].x,
				    &universe[i].y,
				    &universe[i].z,
				    &universe[i].m
				    );
				universe[i].ax = 0.0;
				universe[i].ay = 0.0;
				universe[i].az = 0.0;
			}
			MPI_Send(universe, tmp * sizeof(*universe), MPI_UNSIGNED_CHAR, j, 0, MPI_COMM_WORLD);
		}
		/* Load remaining stars to CPU 0 */
		stars = stars/size + ((0 < stars % size) ? 1 : 0);
		for (i = 0; i < stars; i++) {
			fscanf(data, "%lld; %lld; %lld; %lld",
			    &universe[i].x,
			    &universe[i].y,
			    &universe[i].z,
			    &universe[i].m
			    );
			universe[i].ax = 0.0;
			universe[i].ay = 0.0;
			universe[i].az = 0.0;
		}

		fclose(data);

	} else {
		/* Receive number of stars */
		MPI_Recv(&stars, 1, MPI_UNSIGNED_LONG, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
		printf("CPU %d received %ld stars\n", rank, stars);
		universe = malloc(stars * sizeof(*universe));

		/* Receive information about stars */
		MPI_Recv(universe, stars * sizeof(*universe), MPI_UNSIGNED_CHAR, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
	}

	/* Obtain neighbours */
	if (size > 1) {
		next = (rank + 1 < size) ? rank + 1 : 0;
		prev = (rank - 1 >= 0) ? rank - 1 : size - 1;
	} else {
		next = MPI_PROC_NULL;
		prev = MPI_PROC_NULL;
	}

	time = 0.0;
#if 1
	for (int cpu = 0; cpu < size; cpu++) {
		MPI_Barrier(MPI_COMM_WORLD);
		if (cpu != rank)
			continue;
		printf("CPU: %d %p %ld %d %d\n", rank, universe, stars, next, prev);
		fflush(stdout);
	}
#endif
	/* Copy own stars to buffer */
	other_stars_n = stars;
	other_stars = malloc((other_stars_n+1) * sizeof(*other_stars));
	other_stars_second = malloc((other_stars_n+1) * sizeof(*other_stars));
	memcpy(other_stars, universe, other_stars_n * sizeof(*other_stars));

	for (int t=0; t < NUMBER_OF_TESTS; t++) {
		time -= MPI_Wtime();
		for (int k = 0; k < size; k++) {
#if 0
			cpu = k;
			cpu = (cpu + 1 < size) ? cpu + 1 : 0;
			for (int l = 0; l < size; l++) {
				MPI_Barrier(MPI_COMM_WORLD);
				if (cpu == rank || size == 1) {
					printf("Iteration: %d CPU: %d\n", k, cpu);
					for (i = 0; i < other_stars_n; i++) {
						printf("%lld; %lld; %lld; %lld\n",
						    other_stars[i].x,
						    other_stars[i].y,
						    other_stars[i].z,
						    other_stars[i].m
						    );
					}
				}
				cpu = (cpu + 1 < size) ? cpu + 1 : 0;
			}
#endif
			for (i = 0; i < stars; i++)
				for (j = 0; j < other_stars_n; j++) {
					if (k != 0 || i != j) {
						d = pow(pow(other_stars[j].x - universe[i].x, 2) +
						    pow(other_stars[j].y - universe[i].y, 2) +
						    pow(other_stars[j].z - universe[i].z, 2), 3.0/2.0);

						universe[i].ax += G*other_stars[j].m*(other_stars[j].x - universe[i].x)/d;
						universe[i].ay += G*other_stars[j].m*(other_stars[j].y - universe[i].y)/d;
						universe[i].az += G*other_stars[j].m*(other_stars[j].z - universe[i].z)/d;
					}
				}

			tmp = other_stars_n;
			/* Pass/receive number of stars to/from neighbour */
			MPI_Sendrecv(	&tmp, 1, MPI_UNSIGNED_LONG, next, 1,
					&other_stars_n, 1, MPI_UNSIGNED_LONG, prev, 1,
					MPI_COMM_WORLD, MPI_STATUS_IGNORE);

			/* Pass/receive stars to/from neighbour */
			MPI_Sendrecv(	other_stars, tmp * sizeof(*other_stars), MPI_UNSIGNED_CHAR, next, 0,
					other_stars_second, other_stars_n * sizeof(*other_stars), MPI_UNSIGNED_CHAR, prev, 0,
					MPI_COMM_WORLD, MPI_STATUS_IGNORE);

			other_stars_tmp = other_stars;
			other_stars = other_stars_second;
			other_stars_second = other_stars_tmp;
		}
		time += MPI_Wtime();
	}

	cpu = 1;
	for (int l = 0; l < size; l++) {
		MPI_Barrier(MPI_COMM_WORLD);
		if (cpu == rank || size == 1) {
			for (i = 0; i < stars; i++) {
				printf("%f, %f, %f\n", universe[i].ax, universe[i].ay, universe[i].az);
				fflush(stdout);
			}
		}
		cpu = (cpu + 1 < size) ? cpu + 1 : 0;
	}

	MPI_Finalize();
	return (0);
}

