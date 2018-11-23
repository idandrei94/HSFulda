#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define P 1984
#define Q 1984
#define R 1984

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
  int i, j, k;
  //int sum;
  #pragma omp parallel for default(none), collapse(3), private(i,j,k),\
     shared(a,b,c)
  for(i = 0; i < P; ++i)
  {
    for(j = 0; j < R; ++j)
    {
      //sum = 0;
      for(k = 0; k < Q; ++k)
      {
        c[i][j] += a[i][k]*b[k][j];
      }
      //c[i][j] = sum;
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
  {
    for(int j = 0; j < Q; ++j)
    {
       a[i][j] = i*P+j;
    }
  }
  for(int i = 0; i < Q; ++i)
  {
    for(int j = 0; j < R; ++j)
    {
      b[i][j] = j==i;
    }
  }
  matrix_mul(a,b,c);
  printf("CPU time:\t\t%.2f\t\tReal time: \t\t%.2f\n",
		((double)(clock()-start_clock))/CLOCKS_PER_SEC, 
		difftime(time(NULL), start_time));
  printf("Two values: %f\t%f\n", c[0][0], c[15][15]);
  return EXIT_SUCCESS;
}
