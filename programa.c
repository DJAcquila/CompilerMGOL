#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	int T0;
	int T1;
	/*------------------------------*/
	int B;
	literal c;
	double A;



	printf("Digite um numero:");
	scanf("%d",&B);
	B = 2;
	B = 3;
	T0=B>=0;
	while(T0){
		printf("iteracao...iterando...");
		T1=B-1;
		B = T1;
T0=B>=0;
	}
	printf("programa finalizado");
}