//Programa que muestra cómo escribir datos hacia un archivo.

#include <stdio.h>

int main() {
    int i = 0;
    FILE *archivo = NULL;   //Se declara un apuntador a archivo.
    char nombre[30];        //Se declara una cadena.

    archivo = fopen("saludo.txt", "w"); //Se abre el archivo llamado "saludo.txt" en modo escritura ("w").
    if (archivo == NULL) {              //Si no se pudo abrir el archivo, termina el programa.
        printf("No se pudo abrir el archivo.\n");
        return 1;
    }

    printf("Ingresa tu nombre: ");
    fgets(nombre, 30, stdin);               //Se obtiene una cadena del teclado.

    fprintf(archivo, "Hola, %s.", nombre);  //fprintf hace lo mismo que printf, pero en vez de desplegar en pantalla, lo guarda en "archivo".
    fclose(archivo);                        //Se cierra el archivo previamente abierto.
    printf("Se guardo un archivo que te saluda.\n");

    return 0;
}