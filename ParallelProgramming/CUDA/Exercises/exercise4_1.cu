#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define P 2
#define Q 3
#define R 4

__device__ __constant__ double* cuda_matrix_b;

/* define macro to check the return value of a CUDA function */
#define CheckRetValueOfCudaFunction(val) \
 if (val != cudaSuccess) \
 { \
 fprintf (stderr, "file: %s line %d: %s.\n", \
 __FILE__, __LINE__, cudaGetErrorString (val)); \
 cudaDeviceReset (); \
 exit (EXIT_FAILURE); \
 }

__global__ void printKernel( const double * __restrict__ arr, const size_t q, const size_t r)
{
  printf("%d x %d\n", q, r);
  int tid = (int) (blockIdx.x * blockDim.x + threadIdx.x);
  if(tid < q)
  {
    for(int j = 0; j < r; ++j)
    {
      printf("(tid %d) Printing element[%d][%d]: %f\n", tid, tid, j, arr[tid*q+j]);
    }
    printf("\n");
  }
}

void init_arrays(double **a, double *b, double **c)
{
  for(int i = 0; i < P; ++i)
  {
    for(int j = 0; j < Q; ++j)
    {
      a[i][j] = i * P + j;
    }
  }

  for(int i = 0; i < Q; ++i)
  {
    for(int j = 0; j < R; ++j)
    {
      b[i*Q+j] = i * Q + j;
    }
  }

  for(int i = 0; i < P; ++i)
  {
    for(int j = 0; j < R; ++j)
    {
      c[i][j] = 0;
    }
  }
}

int main( void )
{
  cudaError_t cuda_ret;		
	time_t start_time;
	clock_t start_clock;

  double **a;
  double *b;
  double **c;

  start_clock = clock();
  start_time = time(NULL);


  // MEMORY ALLOCATION
  a = (double**)malloc(sizeof(double*) * P);

  b = (double*)malloc(sizeof(double) * Q * R);
  cuda_ret = cudaMalloc((void**)&cuda_matrix_b, sizeof(double) * Q * R);
  CheckRetValueOfCudaFunction(cuda_ret);

  c = (double**)malloc(sizeof(double*)*P);

  for(int i = 0; i < P; ++i)
  {
    a[i] = (double*)malloc(sizeof(double) * Q);
    c[i] = (double*)malloc(sizeof(double) * R);
  }

  // INIT LOCAL DATA
  init_arrays(a, b, c);
  cudaMemcpy(cuda_matrix_b, b, sizeof(double) * Q * R, cudaMemcpyHostToDevice);

  // DO THE MAGIC

  printKernel <<<5, 6>>> (cuda_matrix_b , Q, R);
  cuda_ret = cudaDeviceSynchronize ();
  CheckRetValueOfCudaFunction (cuda_ret);


  // FREE 
  for(int i = 0; i < P; ++i)
  {
    free(c[i]);
  }
  
  for(int i = 0; i < Q; ++i)
  {
    free(a[i]);
    CheckRetValueOfCudaFunction(cuda_ret);
  }

  free(a);
  free(b);
  free(c);

  cudaFree(&cuda_matrix_b);
  CheckRetValueOfCudaFunction(cuda_ret);

  cudaDeviceReset();
  CheckRetValueOfCudaFunction(cuda_ret);

  printf("CPU time:\t\t%.2f\t\tReal time: \t\t%.2f",
		((double)(clock()-start_clock))/CLOCKS_PER_SEC, 
		difftime(time(NULL), start_time));
  return EXIT_SUCCESS;
}
