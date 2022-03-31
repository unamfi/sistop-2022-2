
# Proyecto 2 Bryan Velasco & Christian Leyva
## Un día en el aeropuerto Felipe Ángeles.
### Situación:
Se acaba de inaugurar el nuevo aeropuerto Felipe ángeles en el que se cuentan las siguientes zonas de operación:
- Pista de aterrizaje/despegue.
- Torre de control.
- Zona de espera(terrestre).
- Zona de espera (áerea).
- Zona de carga/descarga de pasajeros.
- Zona de descarga/carga de mercancía.

Se sabe que se tiene un flujo continuo de peticiones de la pista de aterrizaje las cuales son gestionadas por 
la torre de control, la torre de control deberá administrar los aterrizajes y despegues según como lleguen las 
peticiones de los aviones (sin generar inanición a alguno de los aviones), cada uno de los aviones que aterriza 
volverá a despegar tras dejar a sus pasajeros o mercancía y ser llenado nuevamente con los pasajeron o la mercancía.

El andén de carga/descarga de pasajeros permite la operación de hasta 10 aviones comerciales al mismo tiempo
y el andén de carga/descarga de mercancía permite la operación de hasta 6 aviones de carga también al mismo tiempo.

Cuando un avión no puede aterrizar se deja volando en la zona de espera aérea y cuando un avión no puede despegar 
se deja esperando en la zona de espera terrestre.

### Consecuencias nocivas de la concurrencia:
En un aeropuerto la peor situación de concurrencia se da cuando existe un excedente de tráfico aéreo que obliga a 
los aviones a sobrevolar el aeropuerto o retrazar el despegue más de lo debido, incurriendo en retrasos o inclusive
accidentes. Por esta razón una correcta administración de los espacios es primordial para cualquier torre de control.

### Eventos concurrentes para los cuales el ordenamiento no resulte importante:
Dado que el tiempo de permanencia de cada avión en el aeropuerto es una característica intrínseca de cada cargamento,
el tiempo que estos tarden en despegar de nuevo generará un nuevo ordenamiento en los despegues, por ello su orden de 
salida no resulta relevante.

## Documentación
## Descripción de los mecanismos de sincronización empleados
Los mecanismos de sincronización utilizados son los siguientes:
  - Rendezvous: El rendezvous fue utilizado para establecer una comunicación entre el avión y la torre de control y de
  esta manera asignarle la pista al avión.
  ![image](https://user-images.githubusercontent.com/86135452/161147861-90406903-097f-4cc0-933d-9d3cae45edf0.png)
  - Mutex: El mutex fue utilizado para proteger la pista de aviación y que esta sea utilizada por más de un
  - Multiplex:
## Lógica de operación
### Identificación del estado compartido (variables o estructuras globales)
### Descripción algorítmica del avance de cada hilo/proceso
### Descripción de la interacción entre ellos (sea mediante los mecanismos de sincronización o de alguna otra manera)
## Descripción del entorno de desarrollo, suficiente para reproducir una ejecución exitosa
### ¿Qué lenguaje emplean? ¿Qué versión?
### ¿Qué bibliotecas más allá de las estándar del lenguaje?
### ¿Bajo qué sistema operativo / distribución lo desarrollaron y/o probaron?
## Ejemplos o pantallazos de una ejecución exitosa
