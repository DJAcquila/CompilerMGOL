#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	int T0;
	int T1;
	int T2;
	/*------------------------------*/
	int B;
	literal c;
	double A;



	printf("Digite um numero:");
	scanf("%d",&B);
	B = 2;
	B = 3;
	T0=B==2;
	if(T0){
		B = 9;
	}
	T1=B>=0;
	while(T1){
		printf("iteracao...iterando...");
		T2=B-1;
		B = T2;
T1=B>=0;
	}
	printf("programa finalizado");
}