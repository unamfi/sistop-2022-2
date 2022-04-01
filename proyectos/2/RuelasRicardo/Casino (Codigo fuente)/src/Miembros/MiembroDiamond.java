
package Miembros;

import java.util.Scanner;
import Excepciones.*;
/**
 * Los Miembros Diamond reciben mayores beneficios en el casino que los miembros Silver y Golden. Son los únicos que tiene acceso al hipódromo.
 * 
 */

public class MiembroDiamond extends Miembro{
    /**
     * Constructor para crear miembros Diamond.
     * @param nombre El nombre del usuario.
     * @param correo El correo electronico con el que se asociara esta membresia.
     * @param usuario El nombre único con el que se reconocera al miembro en el sistema.
     * @param contraseña La clave con la cual se podra acceder a una cuenta.
     */
    public MiembroDiamond(String nombre, String correo, String usuario, String contraseña) {
        try{
            setNombre(nombre);
            setCorreo(correo);
            setUsuario(usuario);
            setContraseña(contraseña);
            this.Membresia = "Diamond";
        }catch(DatosIncorrectos e){
            System.out.println(e.getMessage());
        }
    }
     /**
     * Método de clase que se utiliza para el registro de miembros Diamond en tiempo de ejecucion.
     * @return Un Miembro Diamond con un nombre, corrreo, nombre de usuario y contraseña.
     */
    public static Miembro registrarMiembro(){
        Scanner input = new Scanner(System.in);
        String nombre, correo, usuario, contraseña;
        System.out.print("\nIngresa tu nombre: ");
        nombre = input.nextLine();
        System.out.print("\nIngresa tu correo: ");
        correo = input.nextLine();
        System.out.print("\nIngresa tu usuario: ");
        usuario = input.nextLine();
        System.out.print("\nIngresa tu contraseña: ");
        contraseña = input.nextLine();

        return new MiembroDiamond(nombre, correo, usuario, contraseña);
    }
    
    
}
