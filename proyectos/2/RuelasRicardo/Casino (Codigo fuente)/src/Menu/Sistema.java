package Menu;

import Excepciones.FueraDeRango;
import Juegos.Caballos;
import ManejoArchivos.ManejoArchivos;
import Miembros.*;
import java.util.*;

/**
 *La siguiente clase se encarga de la autentificacion y registro de usuarios. Contiene los  menús de registro y de juegos, asi como acceso a las
 * estructuras donde se encuentran almacenados los datos de los usuarios.
 * 
 */

public class Sistema {
    /**
     * La lista donde están todos los miembros que ya se han registrado en el casino.
     */
    List<Miembro> listaMiembros;
    /**
     * Objeto de tipo scanner que se utilizara para que el usuario pueda ingresar datos en tiempo de ejecucion.
     */
    Scanner input;
    /**
     * El gestor se encarga del manejo de la base de datos. Es el responsable directo de cargar los usuarios al sistema y guardar los usuarios en memoria secundaria.
     */
    ManejoArchivos gestor;
    
    /**
     * Constructor de sistema, inicializa todos las estructuras necesarias para su funcionamiento y carga a la lista a todos los miembros de la base de datos. 
     */
    public Sistema(){
        listaMiembros = new LinkedList<>();
        
        gestor = new ManejoArchivos(); 
        input = new Scanner(System.in);
        
        // Inicialización de los datos del administrador (solamente ejecutar si no se tiene un archivo de datos previo)
        /*
        usuarios = new HashSet<>();
        listaMiembros.add(new MiembroDiamond("admin", "admin@admin", "admin", "cs2021-01"));
        listaMiembros.get(0).setFichas(1_000_000_000);
        usuarios.add("admin");
        gestor.guardarMiembros(listaMiembros);
        gestor.guardarUsuarios(usuarios);
        */
        
        listaMiembros.addAll(gestor.cargarMiembros());
        Miembro.setUsuarios(gestor.cargarUsuarios());
    }
    /**
     * El inicio de sesion del usuario. Revisa que tanto el nombre de usuario como la contraseña sean correctas,
     * @return -1 Si el nombre de usuario y/o contraseña ingresados son incorrectos O el indice de la posicion en la lista en la cual se encuentra el usuario.
     */
    public int ingreso(){
        // Formulario
        System.out.print("\nUsuario: ");
        String usuario = input.nextLine();
        System.out.print("Contraseña: ");
        String contraseña = input.nextLine();
        
        // Autentificacion
        for(int i = 0; i < listaMiembros.size(); i++){
            Miembro miembro = listaMiembros.get(i);
            
            if(miembro.getUsuario().equals(usuario)){
                if (miembro.getContraseña().equals(contraseña))
                    return i;
            }
        }
        
        return -1;
    }
    /**
     * El registro de los usuarios,aqui es donde el usuario escoge el tipo de membresia y registra todos sus datos.
     * @return El id del usuario.
     */
    public int registro(){
        int intentos = 3;
        int opcion;
        Miembro miembroAux;
        
        System.out.println("\nMembresias disponibles:");
        System.out.println("1) Diamond: \n\tAcceso a todos los juegos.\n\tBonificación del 200% del total de las apuestas hechas.\n\tApuesta máxima del 100% de tus fichas.");
        do{
            try{
                System.out.print("Ingresa la opción deseada: ");
                opcion  = Integer.parseInt(input.nextLine());
                if(opcion < 1 || opcion > 3){
                    throw new FueraDeRango();
                }
                intentos = 0;
                try {
                    System.out.println("\nCreando tu cuenta, por favor espere...");
                    switch(opcion){
                        case 1:
                            miembroAux = MiembroDiamond.registrarMiembro();
                            if(miembroAux.getMembresia() == null){
                                return -1;
                            }
                            listaMiembros.add(miembroAux);
                            Miembro.usuarios.add(miembroAux.getUsuario());
                            Thread.sleep(2500);
                            break;
                    }
                    System.out.println("\nCuenta creada satisfactoriamente!");
                } 
                catch (InterruptedException e) {
                    System.out.println("\nError: Ha ocurrido un problema conectando al servidor, intentalo de nuevo más tarde.");
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
        
        gestor.guardarMiembros(listaMiembros); // Al registrar un miembro, se realiza el guardado en el archivo de objetos.
        
        return listaMiembros.size()-1; 
    }
    /**
     * Desde este menu el usuario puede realizar diversas acciones como entrar a los juegos, comprar más fichas o cerrar sesion.
     * @param idUsuario El indice de la lista de miembros en la cual se encuentra el usuario.
     */
    public void menuPrincipal(int idUsuario){
        Miembro activo = listaMiembros.get(idUsuario);
        Caballos caballos = new Caballos();
        
        int opcion = 0;
        
        do{
            try{
                System.out.println("\nBienvenido, " + activo.getNombre());
                System.out.println("1.- Apostar a caballos");
                System.out.println("2.- Mostrar fichas");
                System.out.println("3.- Depositar fichas");
                System.out.println("4.- Salir");
                System.out.print("Opcion: ");
                opcion  = Integer.parseInt(input.nextLine());
                if(opcion < 1 || opcion > 4){
                    throw new FueraDeRango();
                }

                switch(opcion){
                    case 1:
                        if(activo.getMembresia().equals("Diamond")){
                            if(activo.getFichas() < 100){
                                System.out.println("\nError: Necesitas al menos 100 fichas.");
                                break;
                            }
                            caballos.jugar(activo, listaMiembros);
                        }
                        else{
                            System.out.println("\nError: Necesitas una membresía Diamond para entrar al hipodromo.");
                        }
                        break;

                    case 2:
                        System.out.println("\nFichas totales: " + activo.getFichas());
                        break;

                    case 3:
                        activo.depositarF();
                        gestor.guardarMiembros(listaMiembros);
                        break;

                    case 4:
                        gestor.guardarMiembros(listaMiembros);
                        System.out.println("\nCerrando sesión...");
                        try {
                            Thread.sleep(800);
                            System.out.println("\nVuelve pronto!");
                        } catch (InterruptedException e) {
                            System.out.println("Error: Ha ocurrido un problema conectando al servidor, finalizando sesión.");
                        }
                        break;

                    default:
                        System.out.println("\nOpcion invalida, intentalo de nuevo");
                        break;
                }
            }
            catch(NumberFormatException e){
                System.out.print("\nError: Ingresa una opción valida. (No se permiten letras)\n\n");
            }
            catch(FueraDeRango e){
                System.out.println("\nError: Ingresa un valor valido. (Rango númerico no valido)\n");
            }            
        }while(opcion != 4);
    }
    /**
     * Desde este menu el administrador del casino puede realizar diversas acciones como modificar a los usuarios, manejar el sistema e incluso probar los diferentes juegos.
     * 
     */
    public void menuAdmin(){
        Miembro activo = listaMiembros.get(0);
        
        Caballos caballos = new Caballos();
        
        int opcion = 0;
        
        do{
            try{
                activo.setFichas(1_000_000_000); // El administrador siempre tendra fichas
                int i = 0;
                System.out.println("\nCentro de control");
                System.out.println("1.- Caballos");
                System.out.println("2.- Administrar miembros");
                System.out.println("3.- Salir");
                System.out.print("Opcion: ");
                opcion  = Integer.parseInt(input.nextLine());
                if(opcion < 1 || opcion > 3){
                    throw new FueraDeRango();
                }

                switch(opcion){
                    case 1:
                        caballos.jugar(activo, listaMiembros);
                        break;

                    case 2:
                        System.out.println("");
                        for (Miembro miembro : listaMiembros) {
                            System.out.println("ID: " + i++ + "\t\tUsuario: " + miembro.getUsuario() + "\t\tMembresia: " + miembro.getMembresia() + "\t\tFichas: " + miembro.getFichas());
                        }
                        System.out.println("\nElige que deseas realizar:\n1)Eliminar miembro\n2)Volver al menú");
                        System.out.print("Opcion: ");
                        int opcAdmin = Integer.parseInt(input.nextLine());
                        
                        switch(opcAdmin){
                            case 1:
                                System.out.print("\nIngresa el ID del usuario: ");
                                int idEliminar = Integer.parseInt(input.nextLine());
                                if(idEliminar == 0){
                                    System.out.println("\nError: No puedes eliminar al administrador, reiniciando sistema...");
                                    try {
                                        Thread.sleep(1500);
                                    } catch (InterruptedException e) {
                                        System.out.println("Error: Ha ocurrido un problema conectando al servidor, intentalo de nuevo.");
                                    }
                                    return;
                                }
                                else if(idEliminar < 0 || idEliminar > listaMiembros.size() - 1){
                                    System.out.println("\nError: El usuario indicado no existe, intentalo de nuevo.");
                                    break;
                                }
                                System.out.println("\nEstas seguro de que deseas eliminar al usuario " + listaMiembros.get(idEliminar).getUsuario() + "?\n1)Si\n2)No");
                                System.out.print("Opcion: ");
                                if(Integer.parseInt(input.nextLine()) == 1){
                                    try {
                                        Thread.sleep(1300);
                                        listaMiembros.remove(idEliminar);
                                    } catch (InterruptedException e) {
                                        System.out.println("Error: Ha ocurrido un problema conectando al servidor, intentalo de nuevo.");
                                    }
                                    System.out.println("\nUsuario eliminado correctamente!");
                                }
                                gestor.guardarMiembros(listaMiembros);
                                break;
                                
                            case 2:
                                System.out.println("\nVolviendo...");
                                break;
                        }
                        break;

                    case 3:
                        gestor.guardarMiembros(listaMiembros);
                        System.out.println("\nFinalizando sesión...");
                        try {
                            Thread.sleep(800);
                        } catch (InterruptedException e) {
                            System.out.println("Error: Ha ocurrido un problema conectando al servidor, finalizando sesión.");
                        }
                        break;

                    default:
                        System.out.println("\nOpcion invalida, intentalo de nuevo");
                        break;
                }
            }
            catch(NumberFormatException e){
                System.out.print("\nError: Ingresa una opción valida. (No se permiten letras)\n\n");
            }
            catch(FueraDeRango e){
                System.out.println("\nError: Ingresa un valor valido. (Rango númerico no valido)\n");
            }            
        }while(opcion != 3);
    }
}