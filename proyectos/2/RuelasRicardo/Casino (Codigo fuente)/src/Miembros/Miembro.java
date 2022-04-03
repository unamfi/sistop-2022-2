package Miembros;
import Excepciones.*;
import java.io.Serializable;
import java.util.Scanner;
import java.util.HashSet;

/**
 * Es la Clase abstracta que contiene todos los elementos basicos y operaciones que pueden ser realizados por cualquier usuario que se ha registrado.
 * 
 */
public abstract class Miembro implements Serializable{
    /**
     * Contiene todos los nombres de los usuarios que ya han sido registrados, con esta estructura garantizamos que no haya dos usuarios con un mismo nombre.
     */
    public static HashSet<String> usuarios = new HashSet<>();
    /**
     * El nombre completo del usuario que estará asociado con esta memebresía.
    */
    protected String nombre;
    /**
     * El correo electrónico del miembro.
     */
    protected String correo;
    /**
     * Tipo de membresia con la cual se registro el usuario.
     */
    protected String Membresia;
    /**
     * Numero de fichas que tiene el usuario. Las fichas son necesaria para poder tomar parte en cualquiera de los juegos.
     */
    protected double Fichas;
    /**
     * Nombre único con el cual se identificara a este miembro.
     */
    protected String usuario;
    /**
     * La contraseña del usuario, que debera ser ingresada cada vez que el usuario inicia sesion.
     */
    protected String contraseña;
       
    /**
     * Método utilizado para saber el número de Fichas del Usuario
     * @return El numero de fichas que posee el usuario.
     */
    public double getFichas() {
        return Fichas;
    }
    /**
     * Tiene como funcion asignar un numero determiado de fichas al usuario.
     * @param Fichas El numero de fichas que se asignan.
     */
    public void setFichas(double Fichas) {
        if(Fichas >= 0)
            this.Fichas = Fichas;
        else{
            System.out.print("\nError: No puedes tener fichas negativas.");
        }
    }
    /**
     * Devuelve el tipo de membresia de este usuario.
     * @return El tipo de membresia ya sea silver, golden o diamond
     */
    public String getMembresia() {
        return Membresia;
    }
    /**
     * Se asigna una cadena que representa el tipo de membresia que posee este usuario.
     * @param Membresia El tipo de membresia con la cual se regristrara al usuario.
     * @throws DatosIncorrectos Si la membresia no tiene la longitud mínima solicitada.
     */
    public void setMembresia(String Membresia) throws DatosIncorrectos {
        if(Membresia.length() > 3)
            this.Membresia = Membresia;
        else{
            throw new DatosIncorrectos("\nError: Una membresia tiene que tener mas de 3 caracteres, intenta de nuevo");
        }
    }
    /**
     * Devuelve el nombre del usuario asociado con esta membresia.
     * @return El nombre con el que se registro el usuario.
     */
    public String getNombre() {
        return nombre;
    }
    /**
     * Designa el nombre del usuario asociado con esta membresia.
     * @param nombre El nombre completo del usuario.
     * @throws DatosIncorrectos Si el nombre con el cual se intenta registrar es muy corto.
     */
    public void setNombre(String nombre) throws DatosIncorrectos {
        if(nombre.length() > 3)
            this.nombre = nombre;
        else{
            throw new DatosIncorrectos("\nError: Un nombre tiene que tener mas de 3 caracteres, intenta de nuevo");
        }
    }
    /**
     * Devuelve el correo de este miembro
     * @return El correo con el que se registro este miembro.
     */
    public String getCorreo() {
        return correo;
    }
    /**
     * Sirve para asignar el correo al cual esta ligado este miembro.
     * @param correo El correo electrónico del miembro.
     * @throws DatosIncorrectos Si el correro electronico no tiene la longitud mínima requerida.
     */
    public void setCorreo(String correo) throws DatosIncorrectos{
        if(correo.length() > 7)
            this.correo = correo;
        else{
            throw new DatosIncorrectos("\nError: Un correo tiene que tener mas de 7 caracteres, intenta de nuevo");
        }
    }
    /**
     * Devuelve el nombre de usuario este miembro.
     * @return El nombre del  miembro.
     */
    public String getUsuario() {
        return usuario;
    }
    /**
     * Sirve para asignar el nombre de usuario con que se identifica a este miembro. El nombre de usuario debe ser único de lo contrario el proceso arrojará un error.
     * @param usuario El nombre único con el que se identificara al miembro.
     * @throws DatosIncorrectos Si el nombre de usuario propoc
     */
    public void setUsuario(String usuario)throws DatosIncorrectos {
        if(usuarios.contains(usuario)){
            throw new DatosIncorrectos("\nError: Nombre de usuario no disponible.");
        }
        else{
            this.usuario = usuario;
        }
    }
    /**
     * Devuelve la contrasea relacionada con esta membresia.
     * @return La contraseña de este miembro.
     */
    public String getContraseña() {
        return contraseña;
    }
    /**
     * Sirve para asignar una contraseña a los miembros del casino.
     * @param contraseña La contraseña que será utilizada para el inicio de sesion.
     * @throws DatosIncorrectos Si la contraseña no tiene la longitud mínima solicitada.
     */
    public void setContraseña(String contraseña)throws DatosIncorrectos {
        if(contraseña.length() > 5){
            this.contraseña = contraseña;
        }
        else{
            throw new DatosIncorrectos("\nError: Contraseña muy corta, ingresa una contraseña apropiada.");
        }
    }
    /**
     * Sirve para asignar (inicializar) el Set de usuarios, de tal forma que en toda ejecución se tomen en cuenta los usuarios creados hasta el momento.
     * @param usuarios Set que contiene los diferentes nombres de usuario.
     */
    public static void setUsuarios(HashSet<String> usuarios) {
        Miembro.usuarios = usuarios;
    }
    
    /**
     * Permite al usuario la adquisicion de fichas en tiempo de ejecucion.
     */
    public void depositarF(){
        Scanner input = new Scanner(System.in);
        double deposito;
        
        try{
            System.out.print("\nIngresa la cantidad de fichas a depositar: ");
            deposito = Integer.parseInt(input.nextLine());
            if(deposito <= 0){
                throw new FueraDeRango();
            }
            this.Fichas += deposito;
        }
        catch(NumberFormatException e){
            System.out.print("\nError: Ingresa una opción valida. (No se permiten letras)\n\n");
        }
        catch(FueraDeRango e){
            System.out.println("\nError: Ingresa una opción valida. (No se permiten depositos negativos o nulos)\n\n");
        }
    }
}
