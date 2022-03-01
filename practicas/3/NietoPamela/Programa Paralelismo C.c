
//Hilos 
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

void *
segundoproceso (void *datos)
{

  char *texto = (char *) datos;
  
  while (1)
    {
    printf ("%s/n", texto);
    
       
}
}
int main(void)
{
    pthread_t proceso1;
    pthread_t proceso2;
    pthread_create(&proceso1, NULL,&segundoproceso," Hola mundo:)");
    pthread_create(&proceso2, NULL,&segundoproceso," Est C !l C -nea no puede ejecutarse sin antes llevar a cabo una bifurcaci C 3n ");
    pthread_join(proceso1,NULL);
    pthread_join(proceso2,NULL);
    
    
    /*ImpresiC3n infinita de un hola mundo
    while (1){
    printf(" Hola Mundo ");
    }
    //Al tratar de ejecutar otro ciclo while, es imposible salir del primer while
    while(1){
        printf(" Est C !l C -nea no puede ejecutarse sin antes llevar a cabo una bifurcaci C 3n ")
    }
*/
    return 0;
}

