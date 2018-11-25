#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <time.h>

#define G 6.6740831e-11

struct star {
	long long x;
	long long y;
	long long z;
	long long m;
	double ax;
	double ay;
	double az;
};

int main() {
	size_t stars, i, j;
	struct star* universe;
	double d;
	clock_t time;

	scanf("%zu", &stars);
	universe = malloc(stars * sizeof(*universe));

	for (i = 0; i < stars; i++) {
		scanf("%lld; %lld; %lld; %lld",
		    &universe[i].x,
		    &universe[i].y,
		    &universe[i].z,
		    &universe[i].m
		    );
		universe[i].ax = 0.0;
		universe[i].ay = 0.0;
		universe[i].az = 0.0;
	}

	time = -clock();
	for (i = 0; i < stars; i++)
		for (j = i; j < stars; j++)
			if (i != j) {
				d = pow(pow(universe[j].x - universe[i].x, 2) +
				    pow(universe[j].y - universe[i].y, 2) +
				    pow(universe[j].z - universe[i].z, 2), 3.0/2.0);

				universe[i].ax += G*universe[j].m*(universe[j].x - universe[i].x)/d;
				universe[i].ay += G*universe[j].m*(universe[j].y - universe[i].y)/d;
				universe[i].az += G*universe[j].m*(universe[j].z - universe[i].z)/d;

				universe[j].ax += G*universe[i].m*(universe[i].x - universe[j].x)/d;
				universe[j].ay += G*universe[i].m*(universe[i].y - universe[j].y)/d;
				universe[j].az += G*universe[i].m*(universe[i].z - universe[j].z)/d;
			}

	time += clock();
#if 0
	for (i = 0; i < stars; i++) {
		printf("%f, %f, %f\n", universe[i].ax, universe[i].ay, universe[i].az);
	}
#endif

	printf("%ld, 1, %.10f\n", stars, (double)time/(double)CLOCKS_PER_SEC);	

	return (0);
}

