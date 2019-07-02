#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	int T0;
	int T1;
	double T2;
	int T3;
	int T4;
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
	T1=1+B;
	B = T1;
	c = 2.0;
	T2=c+1.0;
	c = T2;
	B = 3;
	T3=B>0;
	while(T3){
		printf("\nloop\n");
		T4=B-1;
		B = T4;
		T3=B>0;
	}
	printf("\nprograma finalizado\n");
	printf("%d",B);
	printf("\n");
}