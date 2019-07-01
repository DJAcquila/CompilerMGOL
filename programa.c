#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	int T0;
	double T1;
	int T2;
	int T3;
	/*------------------------------*/
	literal A;
	int B;
	double c;



	printf("Digite um nome: ");
	scanf("%s",A);
	printf("Digite um numero: ");
	scanf("%d",&B);
	T0=1+B;
	B = T0;
	c = 2.0;
	T1=c+1.0;
	c = T1;
	B = 3;
	T2=B>0;
	while(T2){
		printf("\nloop\n");
		T3=B-1;
		B = T3;
T2=B>0;
	}
	printf("\nprograma finalizado\n");
	printf("%d",B);
	printf("\n");
}