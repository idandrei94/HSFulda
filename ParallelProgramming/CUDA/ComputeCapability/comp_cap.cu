#include <stdio.h>
#include <stdlib.h>

void main(void)
{
	cudaDeviceProp deviceProp;
	cudaGetDeviceProperties(&deviceProp, 0);
	printf("Compute power: %d.%d\n", deviceProp.major, deviceProp.minor);
	cudaDeviceReset();
}