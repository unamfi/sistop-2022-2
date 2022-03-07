public class EjThreadGroup extends Thread {
	
	public EjThreadGroup(ThreadGroup g, String n){
		super(g,n);
	}
	public void run(){
		for(int i = 0; i < 10; i++){
			System.out.print(getName());
		}
	}

	public static void listarHilos(ThreadGroup grupoActual){
		int numHilos;
		Thread[] listaDeHilos;

		numHilos = grupoActual.activeCount();
		listaDeHilos = new Thread[numHilos];
		grupoActual.enumerate(listaDeHilos);
		System.out.println("\nNumero de hilos activos = "+numHilos+"\n");
		for(int i = 0; i < numHilos ; i++){
			System.out.println("\nHilo activo "+(i+1)+"= "+listaDeHilos[i].getName());
		}
	}

	public static void main(String[] args){
		ThreadGroup grupoHilos = new ThreadGroup("Grupo con prioridad normal");
		Thread hilo1 = new EjThreadGroup(grupoHilos, "Hilo 1 con prioridad maxima");
		Thread hilo2 = new EjThreadGroup(grupoHilos, "Hilo 2 con prioridad normal");
		Thread hilo3 = new EjThreadGroup(grupoHilos, "Hilo 3 con prioridad normal");
		Thread hilo4 = new EjThreadGroup(grupoHilos, "Hilo 4 con prioridad normal");
		Thread hilo5 = new EjThreadGroup(grupoHilos, "Hilo 5 con prioridad normal");
		hilo1.setPriority(Thread.MAX_PRIORITY);
		grupoHilos.setMaxPriority(Thread.NORM_PRIORITY);
		System.out.println("Prioridad del grupo = "+grupoHilos.getMaxPriority());

		System.out.println("Prioridad del Thread = "+hilo1.getPriority());
		System.out.println("Prioridad del Thread = "+hilo2.getPriority());
		System.out.println("Prioridad del Thread = "+hilo3.getPriority());
		System.out.println("Prioridad del Thread = "+hilo4.getPriority());
		System.out.println("Prioridad del Thread = "+hilo5.getPriority());

		hilo1.start();
		hilo2.start();
		hilo3.start();
		hilo4.start();
		hilo5.start();

		listarHilos(grupoHilos);
	}
}