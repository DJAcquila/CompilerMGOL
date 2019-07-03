#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	double T0;
	int T1;
	double T2;
	int T3;
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
		T2=c+1.0;
		c = T2;
		T3=B>2;
		if(T3){
			printf("entrei2");
		}
		c = 2.0;
		printf("sai");
	}
	B = 3;
}