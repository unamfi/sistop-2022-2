public class EjThreadGroup extends Thread{ //Hereda de la clase

	/**
	*El metodo constructor necesita un grupo de hilos, en donde se van a colocar a todos los hilos,
	*para poder modificar el comportamiento de los hilos.
	*/
	public EjThreadGroup(ThreadGroup g, String n){
		super(g, n);
	}

	/**
	*Se hace un override del metodo run, para que se pueda verificar el orden los hilos
	*/
	public void run(){
		for (int i=0; i<10; i++) {
			System.out.println("Iteracion " + (i+1) + " del hilo " +getName());
		}
	}

	/**
	*El metodo permite poder corroborar la cantidad de hilos que estan en el grupo, para posteriormente imprimir
	*cada uno de hilos.
	*/
	public static void listarHilos(ThreadGroup grupoActual){
		int numHilos;
		Thread [] listaDeHilos;

		numHilos = grupoActual.activeCount(); //Cantidad de hilos activos
		listaDeHilos = new Thread[numHilos];
		grupoActual.enumerate(listaDeHilos); //Guarda en el arreglo los hilos que componene  al grupo

		System.out.println("\nNumero de hilo activos: " + numHilos + "\n");
		for(int i=0; i<numHilos; i++){
			System.out.println("\nHilo activo " + (i + 1) + " = " + listaDeHilos[i].getName());
		}
	}

	/**
	*Se crean los objetos de cada uno de los hilos y el grupo de los hilos.
	*/
	public static void main(String[] args) {
		ThreadGroup grupoHilos = new ThreadGroup("Grupo con prioridad normal"); //Secrea el grupo de hilos
		Thread hilo1 = new EjThreadGroup(grupoHilos, "Hilo 1 con prioridad maxima");
		Thread hilo2 = new EjThreadGroup(grupoHilos, "Hilo 2 con prioridad normal");
		Thread hilo3 = new EjThreadGroup(grupoHilos, "Hilo 3 con prioridad normal");
		Thread hilo4 = new EjThreadGroup(grupoHilos, "Hilo 4 con prioridad normal");
		Thread hilo5 = new EjThreadGroup(grupoHilos, "Hilo 5 con prioridad normal");

		hilo1.setPriority(Thread.MAX_PRIORITY); //Se invoca el metodo que otorga una prioridad a los hilos
		grupoHilos.setMaxPriority(Thread.NORM_PRIORITY);

		System.out.println("Prioridad del grupo: " + grupoHilos.getMaxPriority());

		System.out.println("Prioridad del hilo 1 = " + hilo1.getPriority());
		System.out.println("Prioridad del hilo 2 = " + hilo2.getPriority());
		System.out.println("Prioridad del hilo 3 = " + hilo3.getPriority());
		System.out.println("Prioridad del hilo 4 = " + hilo4.getPriority());
		System.out.println("Prioridad del hilo 5 = " + hilo5.getPriority());

		hilo1.start();
		hilo2.start();
		hilo3.start();
		hilo4.start();
		hilo5.start();

		listarHilos(grupoHilos);
	}
}