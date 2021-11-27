#include<stdio.h>

float Q_rsqrt( float number )
{
	long i;
	float x2, y;
	const float threehalfs = 1.5F;

	x2 = number * 0.5F;
	y  = number;
	i  = * ( long * ) &y;                       // evil floating point bit level hacking
	i  = 0x5f3759df - ( i >> 1 );               // what the fuck? 
	y  = * ( float * ) &i;
	y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration
//	y  = y * ( threehalfs - ( x2 * y * y ) );   // 2nd iteration, this can be removed

	return y;
}

int main(int argc, char **argv){
    if (argc == 1) {
        printf("use: ./doom_fast_inverse_sqrt <expr>\n");
        return 0;
    }

    float number = 0;
    int err = sscanf(argv[1], "%f", &number);

    float result = Q_rsqrt(number);
    printf("%f", result);
    return 0;
}