package Juegos;

import Excepciones.FueraDeRango;
import ManejoArchivos.ManejoArchivos;
import Miembros.Miembro;
import java.util.List;
import java.util.Random;
import java.util.Scanner;

/**
 * Juego exclusivo para los Miembros Diamond. Una simulacion de una carrera de caballos, el usuario apuesta al caballo de su elección
 * y, si este resulta ganador, recibe un premio.
 * 
 */

public class Caballos implements IFichas{
    /**
     * Se utiliza para reprensentar la pista de carreras, cada fila es un carril.
     */
    String[][] tablero;
    /**
     * Sirve para verificar si alguno de los caballos ha terminado la carrera.
     */
    boolean bandera;
    /**
     * Variables enteras que indican la posicion de la pista en la cual se encuentran los caballos.
     */
    int c1, c2, c3, c4;
    /**
     * Generador de números aleatorios para calcular la distancia que avanza cada caballo en cada iteracion.
     */
    Random rnd;
    /**
     * Objeto de tipo scanner que se utilizara para que el usuario pueda ingresar datos en tiempo de ejecucion.
     */
    Scanner input;
    /**
     * Indica el numero de intentos que tiene el usuario para ingresar una opcion válida antes de terminar la ejecucion de algun método.
     */
    int intentos;
    /**
     * El caballo al que el miembro ha decidido apostar.
     */
    int caballo;
    /**
     * El número de fichas que apuesta un usuario en una carrerla.
     */
    double apuesta;
    /**
     * Se encarga del manejo de la base de datos de los miembros, se encarga de guardar los cambios que ocurren despues de cada juego.
     */
    ManejoArchivos gestor;
    
    Thread mover = new Thread(new Runnable() { 
            @Override
            public void run() 
            { 
                try { 
                    moverCaballos();
                } 
                catch (InterruptedException e) { 
                    e.printStackTrace(); 
                } 
            } 
        });
    
    Thread verificar = new Thread(new Runnable() { 
            @Override
            public void run() 
            { 
                try { 
                    verificarCaballos();
                } 
                catch (InterruptedException e) { 
                    e.printStackTrace(); 
                } 
            } 
        });
    
    public Caballos(){
        tablero = new String[4][50];
        rnd = new Random();
        input = new Scanner(System.in);
        gestor = new ManejoArchivos();
    }
    /**
     * Es el menú principal del juego de caballos. Desde aqui el usuario escoge si quiere o no jugar, a qué caballo apuesta, la cantidad de fichas que apuesta.
     * @param miembro El miembro que esta apostando a los caballos.
     * @param listaMiembros La lista con todos los usuarios registrados. 
     */
    public void jugar(Miembro miembro, List<Miembro> listaMiembros){
        System.out.println("\n\t****Bienvenido al juego de carrera de caballos****");
        System.out.println("Reglas:");
        System.out.println("1) Seleccionar un caballo de entre los disponibles");
        System.out.println("2) Se tiene que apostar al menos 100 fichas");
        System.out.println("3) Los miembros Silver tendran 2 veces su apuesta mas un bono adicional del 50% de su apuesta");
        System.out.println("4) Los miembros Golden tendran 3 veces su apuesta mas un bono adicional de 75% de su apuesta");
        System.out.println("5) Los miembros Diamond tendran 5 veces su apuesta mas un bono adicional del 200% de su apuesta");
        System.out.println("-> Disfruta\n");
        
        do{
            // Reiniciando juego
            c1 = c2 = c3 = c4 = 0;
            bandera = true;
            intentos = 3;
            apuesta = 0;
            caballo = 0;
            System.out.println("Caballos disponibles:");
            System.out.println("1.- Duncan: ┼");
            System.out.println("2.- Sardinilla: ╦");
            System.out.println("3.- Rosinante: ╬");
            System.out.println("4.- Spirit: █");
            System.out.println("0.- Volver al menú principal");
            
            try{
                System.out.print("Opcion: ");
                caballo = Integer.parseInt(input.nextLine());
                if(caballo == 0){
                    System.out.println("\nVolviendo al menú principal...");
                    intentos = 0;
                    return;
                }
                if(caballo < 1 || caballo > 4){
                    throw new FueraDeRango();
                }
                
                System.out.print("Apuesta: ");
                apuesta = Double.parseDouble(input.nextLine());
                if(apuesta < 100){
                    throw new FueraDeRango();
                }
                
                apostar(apuesta, miembro);
                gestor.guardarMiembros(listaMiembros);
                try { 
                    correr(caballo, miembro, listaMiembros);
                } 
                catch (InterruptedException e) { 
                    e.printStackTrace(); 
                } 
            }
            catch(NumberFormatException e){
                intentos--;
                System.out.print("\nError: Ingresa una opción valida. (No se permiten letras)\n-> Te quedan " + intentos + " intentos\n");
            }
            catch(FueraDeRango e){
                intentos--;
                System.out.print("\nError: Ingresa un valor valido. (Rango númerico no valido)\n-> Te quedan " + intentos + " intentos\n");
            }
        }while(intentos > 0);
    }
    /**
     * Se encarga de la simulacion de la carrera, cada iteracion se encarga de revisar si algun caballo ha llegado a la linea de meta y de notificar
     * al usuario los resultados de la carrera, asi como pagar los premios si es que el caballo elegido fue el ganador.
     * @param caballo El caballo seleccionado por el miembro.
     * @param miembro El miembro que esta apostando a los caballos.
     * @param listaMiembros La lista con todos los usuarios registrados. 
     */
    private void correr(int caballo, Miembro miembro, List<Miembro> listaMiembros) throws InterruptedException {
        int ganador;
        
        while(bandera){
            llenar();
            moverCaballos();
            ganador = verificarCaballos();
            dibujar();
            try{
                Thread.sleep(500);
            }
            catch(InterruptedException e){
                System.out.println("Error: Sucedio algo con uno de los caballos.");
            }
            
            if(ganador != 0){
                switch(ganador){
                    case 1:
                        System.out.println("\nDuncan gano!");
                        break;
                    
                    case 2:
                        System.out.println("\nSardinilla gano!");
                        break;
                        
                    case 3:
                        System.out.println("\nRosinante gano!");
                        break;
                    
                    case 4:
                        System.out.println("\nSpirit gano!");
                        break;
                }
                
                if(caballo == ganador){
                    System.out.println("\n¡Felicidades!");
                    double fichas;
                    fichas = cobrar(apuesta, miembro.getMembresia()) + calcularBono(miembro, apuesta);
                    System.out.println("\nHas ganado "+fichas+" fichas");
                    miembro.setFichas(miembro.getFichas() + fichas);
                    gestor.guardarMiembros(listaMiembros);
                }else{
                    System.out.println("\nSuerte para la proxima!");
                }
            }
        }
    }
    /**
     * Calcula la cantidad de espacios que se mueve cada caballo en cada iteracion y  revisa si alguno de los caballos ha llegado a la meta, esta cantidad es aleatoria. 
     * @return Un entero que indica al caballo ganador o 0 si la carrera aún no ha terminado.
     */
    private void moverCaballos() throws InterruptedException {
        synchronized (this){
            c1 += rnd.nextInt(2)+1;
            c2 += rnd.nextInt(2)+1;
            c3 += rnd.nextInt(2)+1;
            c4 += rnd.nextInt(2)+1;
            
            tablero[0][c1] = "┼";
            tablero[1][c2] = "╦";
            tablero[2][c3] = "╬";
            tablero[3][c4] = "█";
            
            notify();
        }
    }
    
    /**
     *
     * Por medio de los hilos, fungiendo como un mutex garantizamos que todos los caballos se hayan movido para poder verificar si alguno ha ganado.
     * @return Un entero que indica al caballo ganador o 0 si la carrera aún no ha terminado.
     */
    private int verificarCaballos() throws InterruptedException {
        synchronized (this){
            // Se verifica si algún caballo ha llegado a la meta
            if(c1 >= 47){
                bandera = false;
                return 1;   
            }
            else if(c2 >= 47){
                bandera = false;
                return 2;
            }
            else if(c3 >= 47){
                bandera = false;
                return 3;
            }
            else if(c4 >= 47){
                bandera = false;
                return 4;
            }
        
            return 0;
        }
    }
    /**
     * Inicializa cada una de las filas de la pista de carreras en cada iteracion.
     */
    private void llenar(){
        for(int y = 0; y < 4; y++){
            for(int x = 0; x < 50; x++)
                tablero[y][x] = " ";
            tablero[y][47] = "░"; // linea de meta
        }
    }
    /**
     * Imprime en pantalla el estado actual de la pista de carreras en cada iteracion.
     */
    private void dibujar(){
        System.out.println("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"); // limpiar pantalla (programación cochina)
        String[] caballos = {"Duncan", "Sardinilla", "Rosinante", "Spirit"};
        
        for(int y = 0; y < 4; y++){
            System.out.print(caballos[y] + " ->\t░");
            for(int x = 0; x < 50; x++){
                System.out.print(tablero[y][x]);
            }
            System.out.println("");
        }
    }
    /**
     * Por medio de este método se retiran el numero de fichas correspondientes al usuario que esta jugando.
     * @param apuesta La cantidad de fichas que apuesta el usuario para poder jugar.
     * @param miembro El miembro que esta jugando.
     */
    @Override
    public void apostar(double apuesta, Miembro miembro){
        int intentos = 3;
        
        if(apuesta <= miembro.getFichas()){
            if(miembro.getMembresia().equals("Silver") && apuesta <= (miembro.getFichas()*0.5)){
                miembro.setFichas(miembro.getFichas()-apuesta);
            }
            else if(miembro.getMembresia().equals("Golden") && apuesta <= (miembro.getFichas()*0.75)){
                miembro.setFichas(miembro.getFichas()-apuesta);
            }
            else if(miembro.getMembresia().equals("Diamond")){
                miembro.setFichas(miembro.getFichas()-apuesta);
            }
            else{
                System.out.println("\nError: Tu membresía no puede apostar esa cantidad.");
            }
        }
        else{
            do{
                try{
                    System.out.print("\nNo tienes suficientes fichas, intenta de nuevo: ");
                    apuesta = Double.parseDouble(input.nextLine());
                    intentos = 0;
                }
                catch(NumberFormatException e){
                    intentos--;
                    System.out.print("\nError: Ingresa una opción valida. (No se permiten letras)\n-> Te quedan " + intentos + " intentos\n");
                }
            }while(intentos > 0);
            apostar(apuesta, miembro);
        }
    }
    /**
     * Calcula el bono al cual es acreedor el usuario segun el tipo de membresia con la que se registró.
     * @param miembro El miembro que esta jugando.
     * @param apuesta La cantidad de dinero ganada en el juego.
     * @return El bono correspondiente según el premio ganado y el tipo de membresia.
     */
    
    @Override
    public double calcularBono(Miembro miembro, double apuesta){
        if(miembro.getMembresia().equals("Silver")){
            System.out.print("El bono por ser miembro "+miembro.getMembresia()+" es de: "+(apuesta*.5));
            return (apuesta*.5);
        }
        if(miembro.getMembresia().equals("Golden")){
            System.out.print("El bono por ser miembro "+miembro.getMembresia()+" es de: "+(apuesta*0.75));
            return (apuesta*0.75);
        }
        if(miembro.getMembresia().equals("Diamond")){
            System.out.print("El bono por ser miembro "+miembro.getMembresia()+" es de: "+(apuesta*2));
            return (apuesta*2);
        }
        return 0;
    }
    /**
     * Devuelve el número de fichas que recibira el miembro por haber ganado; este se calcula en funcion de la apuesta realizada y el tipo de membresia.
     * @param apuesta El numero de fichas que apostó el usuario.
     * @param membresia El tipo de membresia. 
     * @return El total de fichas ganadas.
     */
    @Override
    public double cobrar(double apuesta, String membresia){
        if(membresia.equals("Silver")) {
            return (apuesta * 2);
        }
        if(membresia.equals("Golden")) {
            return (apuesta * 3);
        }
        if(membresia.equals("Diamond")) {
            return (apuesta * 5);
        }
        return 0;
    }
    
}