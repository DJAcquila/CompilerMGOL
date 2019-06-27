#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	int T0;
	int T1;
	double T2;
	/*------------------------------*/
	literal A;
	int B;
	double c;



	printf("Digite um nome:");
	scanf("%s",A);
	printf("Digite um numero:");
	scanf("%d",&B);
	T0=2+B;
	B = T0;
	T1=3+B;
	B = T1;
	c = 2.0;
	T2=c+1.0;
	c = T2;
	printf("programa finalizado");
	printf("%s",A);
}
