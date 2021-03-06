#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define CACHE_SIZE 1

unsigned long long fibonacci_list[CACHE_SIZE];

unsigned long long fibonacci_seq(
    int );
unsigned long long fibonacci_rec(
    int );

unsigned long long fibonacci_seq(
    int n ) 
{
	unsigned long long fib1, fib2, tmp;
	switch(n)
	{
		case 0: 
		case 1:
			return n;
		default:
			;
			fib1 = 1;
			fib2 = 1;
			tmp = 0;
			for(int i = 2; i < n; ++i)
			{
				tmp = fib1 + fib2;
				fib1 = fib2;
				fib2 = tmp;
			}
			return fib2;
	}
}

unsigned long long fibonacci_rec(
    int n )
{
	unsigned long long fib1, fib2, res;
	switch(n)
	{
		case 0: 
		case 1:
			return (unsigned long long)n;
		default:
		;
			if( (n-2 >= CACHE_SIZE) || (fibonacci_list[n-2] == 0) )
			{
				fib1 = fibonacci_rec(n-2);
				if(n-2 < CACHE_SIZE)
					fibonacci_list[n-2] = fib1;
			}
			else
				fib1 = fibonacci_list[n-2];
			if( (n-1 >= CACHE_SIZE) || (fibonacci_list[n-1] == 0) )
			{
				fib2 = fibonacci_rec(n-1);
				if(n-1 < CACHE_SIZE)
					fibonacci_list[n-1] = fib2;
			}
			else
				fib2 = fibonacci_list[n-1];
			res = fib1+fib2;
			if( n < CACHE_SIZE)
			{
			  fibonacci_list[n] = res;
			}
			return res;
	}
}

int main(
    void )
{
        int n = 46;
        unsigned long long fib;
	time_t start_time = time(NULL);
	clock_t start_clock = clock();

	printf("Algorithm\t\tN value\t\tResult\t\t\tCPU time\tReal time\n"
	       "---------------------------------------------"
	       "-------------------------------------------\n");
	fib = fibonacci_seq(n);
	printf("Sequential\t\t%d\t\t%llu\t\t%.2f\t\t%.2f\n", 
		n, 
		fib, 
	       (double) (clock()-start_clock)/CLOCKS_PER_SEC, 
		difftime(time(NULL), start_time));
	start_time = time(NULL);
	start_clock = clock();
	fib = fibonacci_rec(n);++fib;--fib;
	printf("Recurrent\t\t%d\t\t%llu\t\t%.2f\t\t%.2f\n", 
		n, 
		fib, 
	       (double) (clock()-start_clock)/CLOCKS_PER_SEC, 
		difftime(time(NULL), start_time));
  return EXIT_SUCCESS;
}
