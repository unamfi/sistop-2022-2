#include <stdio.h>
#include<pthread.h>
int func(void)
{
   printf("Thread %x \n",pthread_self()); //Id del hilo creado
   pthread_exit(NULL);
}
int main()
{
    pthread_t th1, th2; //direcciones donde estaran los hilos
    
    //Se crean dos hilos sin parametros y con atributos por defecto
    
    pthread_create(&th1,NULL,(void*)func,NULL);
    pthread_create(&th2,NULL,(void*)func,NULL);
    printf("El proceso ligero principal continua ejecutandose");
    
    //Se espera a que terminen los hilos
    pthread_join(th1,NULL);
    pthread_join(th2,NULL);
    printf("Se terminaron de ejecutar los hilos\n");
    return(0);
}
