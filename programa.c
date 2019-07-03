#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	double T0;
	int T1;
	/*------------------------------*/
	literal A;
	int B;
	double c;



	c = 2.0;
	B = 34;
	T0=c<15.0;
	if(T0){
		T1=B>1;
		if(T1){
			printf("entrei");
		}
		c = 30.0;
		printf("sai");
	}
	B = 3;
}