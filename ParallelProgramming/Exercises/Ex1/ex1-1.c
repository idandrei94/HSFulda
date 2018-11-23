#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define P 400
#define Q 600
#define R 800

void print_matrix(
  int, 
  int w, 
  double [][w] );

void matrix_mul(
  double [][Q], 
  double [][R], 
  double [][R] );

void matrix_mul(
  double a[][Q], 
  double b[][R], 
  double c[][R] )
{
	for(int i = 0; i < P; ++i)
	{
		for(int j = 0; j < R; ++j)
		{
			// This are independent operations
			c[i][j] = 0;
			for(int k = 0; k < Q; ++k)
			{
				c[i][j] += a[i][k]*b[k][j];
			}
		}
	}
}

void print_matrix(
  int h,
  int w, 
  double matrix[][w] )
{
	for(int i = 0; i < h; ++i)
	{
		for(int j = 0; j < w; ++j)
		{
			printf("%f ", matrix[i][j]);
		}
		printf("\n");
	}
	printf("\n");
}

static double a[P][Q];
static double b[Q][R];
static double c[P][R];

int main(
  void )
{
	time_t start_time = time(NULL);
	clock_t start_clock = clock();
    for(int i = 0; i < P; ++i)
        for(int j = 0; j < Q; ++j)
        {
          a[i][j] = j+1;
        }
    for(int i = 0; i < Q; ++i)
      for(int j = 0; j < R; ++j)
      {
        b[i][j] = j+1;
      }
  
	matrix_mul(a,b,c);
  printf("CPU time:\t\t%.2f\t\tReal time: \t\t%.2f",
		((double)(clock()-start_clock))/CLOCKS_PER_SEC, 
		difftime(time(NULL), start_time));
	//print_matrix(P,Q,a);
	//print_matrix(Q,R,b);
	//print_matrix(P,R,c);
  return EXIT_SUCCESS;
}
