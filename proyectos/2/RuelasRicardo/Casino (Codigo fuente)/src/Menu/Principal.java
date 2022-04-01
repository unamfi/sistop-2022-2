package Menu;

import java.util.*;

/**
 *Clase principal, contiene el menu de inicio de sesión y registro de ususarios, desde esta se hacen todos los llamados a la clase sistema.
 * @author Ricardo Ruelas, Yoav Galdamez, Rodrigo Tapia
 */
public class Principal {
    /**
     * Método main desde aqui se hace los llamados a todos los métodos necesarios para que el usuario pueda registrarse, iniciar sesion y jugar en el casino.
     *
     */
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        Sistema system = new Sistema();
        int opcion = 0;
        int intentos = 3;
        int idUsuario = -1;
        
        do{
            try{
                System.out.println("\n¿Qué deseas realizar?");
                System.out.println("1.- Iniciar sesion");
                System.out.println("2.- Registrarse");
                System.out.println("3.- Salir");
                System.out.print("Opcion: ");
                opcion = Integer.parseInt(input.nextLine());
                
                switch(opcion){
                    case 1:
                        idUsuario = system.ingreso();
                        if(idUsuario == 0){
                            System.out.println("\n-> Bienvenido Admin, entrando al sistema...");
                            try {
                                Thread.sleep(735);
                            } catch (InterruptedException e) {
                                System.out.println("\nError: Ha ocurrido un problema conectando al servidor, verifica que todo este en orden.");
                            }
                            system.menuAdmin();
                        }
                        else if(idUsuario == -1){
                            System.out.println("\nUsuario/Contraseña incorrectos.");
                        }
                        else{
                            try {
                                System.out.println("\nIniciando sesión...");
                                Thread.sleep(1500);
                                system.menuPrincipal(idUsuario);
                            } catch (InterruptedException e) {
                                System.out.println("\nError: Ha ocurrido un problema conectando al servidor, intentalo de nuevo más tarde.");
                            }
                        }
                        break;
                    
                    case 2:
                        idUsuario = system.registro();
                        try {
                            if(idUsuario == -1) {
                                System.out.println("\nVolviendo el menu principal...");
                                Thread.sleep(750);
                                break;
                            }
                            System.out.println("\nIniciando sesión...");
                            Thread.sleep(1500);
                            system.menuPrincipal(idUsuario);
                        } catch (InterruptedException e) {
                            System.out.println("Error: Ha ocurrido un problema conectando al servidor, intentalo de nuevo más tarde.");
                        }
                        break;
                    
                    case 3:
                        try {
                            System.out.println("\nFinalizando...");
                            Thread.sleep(1500);
                            intentos = 0;
                        } catch (InterruptedException e) {
                            System.out.println("\nError: Ha ocurrido un problema, se forzara el cierre del programa.");
                        }
                        break;
                        
                    default:
                        System.out.println("\nError: Ingresa un valor valido. (Opción invalida)\n");
                        break;
                }
            }
            catch(NumberFormatException e){
                intentos--;
                System.out.print("\nError: Ingresa una opción valida. (No se permiten letras)\n-> Te quedan " + intentos + " intentos\n");
            }
        }while(intentos > 0);
        
    }
}