#include <stdio.h>
#include <time.h> 
#include <stdlib.h> 
#include <math.h>
#include <stdint.h>

#define MIN 1
#define MAX 6000000

#define IGNORE_PRINTF

uint64_t prime(
  int64_t );

uint64_t prime(
  int64_t n )
{
  if ( (n == 2) || (n == 3) )
  {
    return 1;
  }
  if ( (n % 2 == 0) || (n % 3 == 0) )
  {
    return 0;
  }
  for (uint64_t i = 5, inc = 2; i*i <= n; i += inc, inc = 6 - inc)
  {
    if (n % i == 0)
      return 0;
    }
    return 1;
}

int main(
    void )
{
	time_t start_time = time(NULL);
	clock_t start_clock = clock();
  int prime_counter = 0, mp_counter = 0;
  int mp_prime_counter = 0, mpp_counter = 0;
  for(uint64_t i = MIN; i < MAX; ++i)
  {
    if(prime(i))
    {
      ++prime_counter;
      #ifndef IGNORE_PRINTF 
        printf("%d\t", i);
      #endif
      ;
      uint64_t mp = (uint64_t)(pow(2,i)-1);
      if(mp <= MAX && mp >= MIN)
      {
        ++mp_counter;
        #ifndef IGNORE_PRINTF 
          printf("%d\t", mp);
        #endif
        if(prime(mp))
        {
          ++mp_prime_counter;
          #ifndef IGNORE_PRINTF 
            printf("%d\t", mp);
          #endif
          if(mp != 1)
          {
            uint64_t mpp = mp*(uint64_t)(pow(2, i-1));
            if(mpp < MAX)
            {
              ++mpp_counter;
              #ifndef IGNORE_PRINTF
                printf("%d\n", mpp);
              #endif
            }
            else
            {
              #ifndef IGNORE_PRINTF 
                printf("-\n");
              #endif
              ;
            }
          }
          else
          {
            #ifndef IGNORE_PRINTF 
              printf("-\n");
            #endif
            ;
          }
        }
        else
        {
          #ifndef IGNORE_PRINTF 
            printf("-\t-\n");
          #endif
          ;
        }
      }
      else
      {
        #ifndef IGNORE_PRINTF 
          printf("-\t-\t-\n");
        #endif
        ;
      }
    }
  }
  printf("MIN\tMAX\tPrimes\tMersennes\tPrime Mersennes\t");
  printf("\tPerfect Mersennes\tCPU Time\tReal Time\n");
  printf("%d\t%d\t%d\t%d\t\t%d\t\t\t\t%d\t\t%.2f sec\t%.2f sec", 
    MIN, 
    MAX, 
    prime_counter,
    mp_counter, 
    mp_prime_counter, 
    mpp_counter, 
    ((double)clock()-start_clock)/CLOCKS_PER_SEC, difftime(time(NULL),start_time));
    return EXIT_SUCCESS;
}
