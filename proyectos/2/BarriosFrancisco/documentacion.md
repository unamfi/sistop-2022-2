# Documentación #

## Mecanismos de sincronización empleados ##

En primer lugar, se usan varios mecanismos. Un mutex *sencillo*, el cual protegerá a las variables globales que los hilos puedan modificar. Un *torniquete*, el cual solo servirá para que los hilos que vayan en grupo (clientes) pasen de uno en uno. Otro mutex llamado *estante* el cual protegera a la lista de productos que se ofrecen en la tienda. Una lista de *barreras*, la cual puede ser accesada por cualquier hilo que vaya a entrar en grupo, y que servirá para *esperar* a los demás hilos. Y por último, un *evento*, el cual servirá para indicarle al hilo *proveedor* que un determinado producto esta por agotarse, y al recibir esta señal, el hilo adquirirá el estante para rellenar lo que hace falta. El uso de cada mecanismo se detallará mas adelante.

## Lógica de operación
### Variables y estructuras globales

De acuerdo a la imagen:

![Variables globales](/proyectos/2/BarriosFrancisco/Imagenes/Variables.png)

Observamos que los hilos se comparten: la lista de productos, una *lista de grupos* (la cual almacena la información de cada grupo), *una lista de compras* (que almacena el total de productos elegidos), la cantidad *máxima* de personas, grupos y productos que se pueden tener (donde *max_grupos* lo modifica el usuario al momento de ejecutar el código) y la lista de barreras.

### Descripción del algoritmo e interacción entre hilos

**Cliente** Empezamos con el hilo del cliente (No se incluye el código completo):

![Cliente](/proyectos/2/BarriosFrancisco/Imagenes/Cliente.png)

En donde empezamos generando dos variables con un valor aleatorio. Una variable se refiere al número del grupo del hilo, y otra a la cantidad de personas de ese grupo. Si se cumple la condición dada, entonces el cliente entra solo a la tienda. En caso contrario, se usa *grupo_existente* para ser modificada posteriormente en caso de que ya haya alguién de su grupo. Si no, entonces este hilo será el primero.
Se observa que cuando el cliente entra en un grupo, el mutex no se libera, ya que este será liberado en la función **esperar**.

**Esperar** Esta función hace que el hilo busque su barrera correspondiente de acuerdo a su grupo, y espera a los demás hilos:

![Barrera](/proyectos/2/BarriosFrancisco/Imagenes/espera_a_los_demas.png)

Cuando encuentra a su grupo, se libera el mutex, y se pone a esperar.

**Grupo comprando** La función de comprar para un hilo que viene a comprar solo es un tanto más sencilla. Para los grupos, de la lista de productos se escoge uno aleatoriamente, y si la cantidad del producto es menor a la cuarta parte de lo máximo, entonces se llama al proveedor. El *estante* se libera antes de llamar al proveedor, para que el proveedor pueda tomarlo.
Se busca la lista del grupo correspondiente, y se agrega (se suma 1) un producto a la lista. Si la lista se llena (lista[1] == maximo_productos) entonces los hilos se retiran.

![Compra grupal](/proyectos/2/BarriosFrancisco/Imagenes/compra_grupal.png)

Se inserta un ciclo *for*, que inicia en cero y llega hasta el máximo de productos que se pueden comprar. Este ciclo puede romperse en caso de que los hilos pertenencientes al grupo ya hayan llenado la lista de productos.

**El grupo se va** Antes de irse por completo, el lider del grupo debe eliminar su barrera, lista de compras, y la información de su grupo, con el fin de que un hilo pueda crear su nuevo grupo con el mismo número. Como varios hilos entran a *delete_group()* se corre el riesgo de caer en error al intentar ejecutar *grupos.remove(grupoinfo)*, porque si un hilo lo ejecuta, y otro hilo lo trata de ejecutar, se mandará un error porque la información de su grupo ya fue borrada.

![El grupo se nos va](/proyectos/2/BarriosFrancisco/Imagenes/Grupo_sale.png)


**Proveedor** Este hilo único siempre se pregunta si ya recibió la señal de que algo se está vaciando. Si lo recibe, entonces adquiere el *estante* y se pone a buscar que es lo que hace falta. Muy seguidamente también llena lo que aún no ha sido reportado por un Cliente pero que esta por agotarse, o puede tardar un poco en llenar lo que falta, pero de que lo llena, lo llena...

![Proveedor](/proyectos/2/BarriosFrancisco/Imagenes/Proveedor.png)


## Entorno de desarrollo
**Lenguaje de programación** Python 3.8

**Bibliotecas??** Solo se uso la referente a Threading, time y random

**Sistema operativo??** El programa se probó en Zorin OS 16.1 y en Windows, pero se desarrollo en Zorin OS

## Pantallazos
Aqui entra la cuestión de si el código funciona o no. Para un cliente individual si funciona como debe de ser, pero por alguna razón mis clientes son bien antisociales y no quieren entrar con un grupo ya creado (Solo llegan como dos a un grupo x, pero ya nadie más quiere entrar). Se supone que cuando se ejecuta el programa, pido el total de clientes y el máximo de grupos, con la sugerencia que se muestra (máximo grupos = total Clientes / 5), con el fin de evitar caer en el bloqueo de que cada hilo pueda pertenecer a un grupo diferente, y como estarían esperando por hilos que jamás van a llegar, se llegaría a bloqueo mutuo (por así decirlo).
Espero que a usted si le funcione esa parte. Según yo si debe funcionar la lógica de los grupos ya que tras varias pruebas anteriores (cuando mi código aún tenía varios errores mayores) su lógica si funcionaba.

![Ejecución](/proyectos/2/BarriosFrancisco/Imagenes/Ejecucion.png)
