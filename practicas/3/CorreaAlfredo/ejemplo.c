#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>

/*
	Programa que hace uso de las llamadas al sistema
	fork(), getpid(), y getppid().
	
	Ejemplifica la creación de un proceso hijo y la
	obtención  del identificador de proceso para 
	cada proceso.
*/

main()

{
	int pidP, pidH;
	
	pidH = fork(); // Se crea el proceso hijo.
	
	if(pidH != 0 )  // Código del pid del padre
	{
		pidP = getpid(); // Obtengo el pid del padre
		printf("\nSoy el padre, mi identificador de proceso es: %d", pidP);
		printf("\nMi hijo tiene el pid= %d", pidH);
	}
	
	else  // Código del hijo
	{
		printf("\nSoy el hijo, mi pid es: %d", getpid());
		printf("\nEl pid de mi padre es: %d ", getpid());
	}
}
