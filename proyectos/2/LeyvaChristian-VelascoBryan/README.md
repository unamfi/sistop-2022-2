
# Proyecto 2 Bryan Velasco & Christian Leyva
## Un día en el aeropuerto Felipe Ángeles.
Se acaba de inaugurar el nuevo aeropuerto felipe ángeles en el que se cuentan las siguientes zonas de operación:
- Pista de aterrizaje/despegue.
- Torre de control.
- Zona de espera(terrestre).
- Zona de espera (áerea).
- Zona de carga/descarga de pasajeros.
- Zona de descarga/carga de mercancía.

Se tiene un flujo continuo de peticiones de aterrizaje en la pista de aterrizaje las cuales son gestionadas por 
la torre de control, la torre de control deberá gestionar los aterrizajes y despegues según como lleguen las 
peticiones de los aviones (sin generar inanición a alguno de los aviones), cada uno de los aviones que aterriza 
volverá a despegar tras dejar sus pasajeros o mercancía y ser llenado nuevamente con los pasajeron o la mercancía.

El andén de carga/descarga de pasajeros permite la operación de hasta 10 aviones comerciales y el andén de 
carga/descarga de mercancía permite la operación de hasta 6 aviones de carga al mismo tiempo.

Cuando un avión no puede aterrizar se deja volando en la zona de espera aérea y cuando un avión no puede despegar 
se deja esperando en la zona de espera terrestre.
