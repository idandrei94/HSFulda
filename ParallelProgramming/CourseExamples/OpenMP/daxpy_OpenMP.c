/* Simplified implementation of the DAXPY subprogram (double
 * precision alpha x plus y) from the Basic Linear Algebra
 * Subprogram library (BLAS).
 *
 * This version uses OpenMP.
 *
 * The default number of parallel threads depends on the
 * implementation, e.g., just one thread or one thread for every
 * virtual processor. You can for example request four threads, if
 * you set the environment variable "OMP_NUM_THREADS" to "4" before
 * you run the program, e.g., "setenv OMP_NUM_THREADS 4". If you
 * compile the program with the Oracle C compiler (former Sun C
 * compiler) the number of threads is reduced to the number of
 * virtual processors by default if the number of requested threads
 * is greater than the number of virtual processors. You can change
 * this behaviour if you set the environment variable "OMP_DYNAMIC"
 * to "FALSE" before you run the program, e.g., "setenv OMP_DYNAMIC
 * FALSE".
 *
 *
 * Compiling:
 *   cc  -xopenmp -o daxpy_OpenMP daxpy_OpenMP.c [omp_stubs.c] [-lrt]
 *   gcc -fopenmp -o daxpy_OpenMP daxpy_OpenMP.c [omp_stubs.c] [-lrt]
 *   icc -qopenmp -o daxpy_OpenMP daxpy_OpenMP.c [omp_stubs.c]
 *   cl  /GL /Ox /openmp daxpy_OpenMP.c [omp_stubs.c]
 *
 * Running:
 *   ./daxpy_OpenMP [size of vector]
 *
 *
 * File: daxpy_OpenMP.c			Author: S. Gross
 * Date: 04.08.2017
 *
 */

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <float.h>
#include <time.h>
#ifdef _OPENMP
  #include <omp.h>
#else
  #include "omp_stubs.h"
#endif

#define	DEFAULT_N 70000000		/* default vector size		*/
#define ALPHA	  5.0			/* scalar alpha			*/
#define EPS	  DBL_EPSILON		/* from float.h (2.2...e-16)	*/

void daxpy (int n, double alpha, double x[], double y[]);

int main (int argc, char *argv[])
{
  double  *x, *y,			/* addresses for vectors	*/
	  tmp_y0;			/* temporary value		*/
  int	  size,				/* vector size			*/
	  tmp_diff,			/* temporary value		*/
	  i;				/* loop variable		*/
  time_t  start_wall, end_wall;		/* start/end time (wall clock)	*/
  clock_t cpu_time;			/* used cpu time		*/

  switch (argc)
  {
    case 1:				/* no parameters on cmd line	*/
      size = DEFAULT_N;
      break;

    case 2:				/* one parameter on cmd line	*/
      size = atoi (argv[1]);
      if (size < 1)
      {
	fprintf (stderr, "\n\nError: Vector size must be greater "
		 "than zero.\n"
		 "I use the default size.\n");
	size = DEFAULT_N;
      }
      break;

    default:
      fprintf (stderr, "\n\nError: too many parameters.\n"
	       "Usage: %s [size of vector]\n", argv[0]);
      exit (EXIT_FAILURE);
  }

  /* allocate memory for both vectors					*/
  x = (double *) malloc ((size_t) size * sizeof (double));
  if (x == NULL)
  {
    fprintf (stderr, "File: %s, line %d: Can't allocate memory.\n",
	     __FILE__, __LINE__);
    exit (EXIT_FAILURE);
  }
  y = (double *) malloc ((size_t) size * sizeof (double));
  if (y == NULL)
  {
    fprintf (stderr, "File: %s, line %d: Can't allocate memory.\n",
	     __FILE__, __LINE__);
    exit (EXIT_FAILURE);
  }

  /* Initialize both vectors. The daxpy function computes
   * y = alpha * x + y. With the following initialization we get
   * constant values for the resulting vector.
   * new_y[i] = alpha * x[i] + y[i]
   *	      = alpha * i + alpha * (size - i)
   *	      = alpha * size
   */
  for (i = 0; i < size; ++i)
  {
    x[i] = (double) i;
    y[i] = ALPHA * (double) (size - i);
  }

  /* compute "y = alpha * x + y" and measure computation time		*/
  start_wall = time (NULL);
  cpu_time   = clock ();
  daxpy (size, ALPHA, x, y);
  end_wall = time (NULL);
  cpu_time = clock () - cpu_time;

  /* Check result. All elements should have the same value.		*/
  tmp_y0   = y[0];
  tmp_diff = 0;
  for (i = 0; i < size; ++i)
  {
    if (fabs (tmp_y0 - y[i]) > EPS)
    {
      tmp_diff++;
    }
  }
  if (tmp_diff == 0)
  {
    printf ("Computation was successful. y[0] = %6.2f\n", y[0]);
  }
  else
  {
    printf ("Computation was not successful. %d values differ.\n",
	    tmp_diff);
  }

  /* show computation time						*/
  printf ("elapsed time      cpu time\n"
	  "    %6.2f s      %6.2f s\n",
	  difftime (end_wall, start_wall),
	  (double) cpu_time / CLOCKS_PER_SEC);
  free (x);
  free (y);
  return EXIT_SUCCESS;
}


/* Simplified implementation of the DAXPY subprogram (double
 * precision alpha x plus y) from the Basic Linear Algebra
 * Subprogram library (BLAS). This subprogram computes
 * "y = alpha * x + y" with identical increments of size "1"
 * for the indexes of both vectors, so that we can omit the
 * increment parameters in the original function which has
 * the following prototype.
 *
 * void daxpy (int n, double alpha, double x[], int incx,
 *	       double y[], int incy);
 *
 *
 * input parameters:	n	number of elements in x and y
 *			alpha	scalar alpha for multiplication
 *			x	elements of vector x
 *			y	elements of vector y
 * output parameters:	y	updated elements of vector y
 * return value:	none
 * side effects:	elements of vector y will be overwritten
 *			  with new values
 *
 */
void daxpy (int n, double alpha, double x[], double y[])
{
  int i;				/* loop variable		*/

  #pragma omp parallel default(none) private(i) shared(n, alpha, x, y)
  {
    #pragma omp for
    for (i = 0; i < n; ++i)
    {
      y[i] += (alpha * x[i]);
    }
  }
}
