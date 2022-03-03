public class ThreadEjemplo extends Thread {
    public ThreadEjemplo(String str) {
        super(str);
    }

    public void run() {
        for (int i = 0; i < 10 ; i++) {
            System.out.println(i + " " + getName());
        }
        System.out.println("Termina thread " + getName());
    }

    public static void main (String [] args) {
        new ThreadEjemplo("Aldo").start();
        new ThreadEjemplo("Abad").start();
        System.out.println("Termina thread main");
    }
}