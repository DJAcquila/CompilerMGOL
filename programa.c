#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	int T0;
	double T1;
	int T2;
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
	T2=B>=2;
	if(T2){
		printf("\nok\n");
	}
	printf("\nprograma finalizado\n");
	printf("%d",B);
	printf("\n");
}