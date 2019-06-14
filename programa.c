#include<stdio.h>
typedef char literal[256];
void main (void)
{
	/*----Variaveis temporarias----*/
	int T0;
	int T1;
	int T2;
	int T3;
	/*------------------------------*/
	literal A;
	int B;
	int c;



	printf("Digite um nome:");
	scanf("%s",A);
	printf("Digite um numero:");
	scanf("%d",&B);
	B = 2;
	B = 3;
	T0=B+1;
	c = T0;
	T1=c+1;
	c = T1;
	T2=B<1;
	if(T2){
		T3=c<2;
		if(T3){
			printf("texto");
		}
	}
	printf("programa finalizado");
}