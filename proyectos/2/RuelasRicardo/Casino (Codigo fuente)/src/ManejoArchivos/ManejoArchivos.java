package ManejoArchivos;

import Miembros.*;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

/**
 *Esta clase tiene como proposito el almacenamiento y carga de usuarios en memoria secundaria mediante el manejo de archivos de objetos. 
 * 
 */

public class ManejoArchivos {
    /**
     * Objeto de tipo scanner que se utilizara para que el usuario pueda ingresar datos en tiempo de ejecucion.
     */
    Scanner input;
    /**
     * Para la lectura de objetos del archivo en donde se almacenan los miembros.
     */
    ObjectInputStream entrada;
    /**
     * Para la escritura de la lista de miembros en el archivo de miembros.
     */
    ObjectOutputStream salida;
    /**
     * La ruta en la cual se encuentra el registro de los usuarios.
     */
    String rutaArchivo;
    /**
     * Constructor de la clase, inicializa el Scanner y se asigna la ruta predeterminada al archivo de usuarios.
     */
    public ManejoArchivos() {
        input = new Scanner(System.in);
        rutaArchivo = "save/";
    }
    /**
     * Almacena la lista de miembros en su estado actual en el archivo de objetos. El contenido original del archivo se sobreescribe con la nueva lista.
     * @param listaMiembros La lista que contiene a todos los miembros registrados.
     */
    public void guardarMiembros(List<Miembro> listaMiembros){
        //ubicarArchivo();
        
        try {
            salida = new ObjectOutputStream(new FileOutputStream(rutaArchivo + "mbr.obj"));
            
            salida.writeObject(listaMiembros);
            
            // System.out.println("Archivo generado exitosamente en: <" + rutaArchivo + ".obj" + ">");
            
            salida.close();
        }
        catch(IOException e) {
            System.out.println("Error: no se pudo actualizar la base de datos, intentalo de nuevo.");
        }
    }
    /**
     * Almacena el Set de usuarios en su estado actual en el archivo de objetos. El contenido original del archivo se sobreescribe con el nuevo Set.
     * @param usuarios El Set que contiene los nombres de usuario de todos los miembros.
     */
    public void guardarUsuarios(HashSet<String> usuarios){
        //ubicarArchivo();
        
        try {
            salida = new ObjectOutputStream(new FileOutputStream(rutaArchivo + "usr.obj"));
            
            salida.writeObject(usuarios);
            
            // System.out.println("Archivo generado exitosamente en: <" + rutaArchivo + ".obj" + ">");
            
            salida.close();
        }
        catch(IOException e) {
            System.out.println("Error: no se pudo actualizar la base de datos, intentalo de nuevo.");
        }
    }    
    /**
     * Lee y carga en el programa la lista de miembros que esta almacenada en el archivo. Pueden llegar a ocurrir varias excepciones si por alguna razon no se encuentra el archivo o hay algun 
     * problema al intentar leer datos de este o bien si no se encuentra la clase miembro.
     * @return 
     */
    public List<Miembro> cargarMiembros(){
        List<Miembro> listaMiembros = new LinkedList<>();
        
        try{
            entrada = new ObjectInputStream(new FileInputStream(rutaArchivo + "mbr.obj"));
            
            listaMiembros = (List<Miembro>) entrada.readObject();
            
            entrada.close();
        }
        catch(FileNotFoundException e){
            System.out.println("Error: no se pudo conectar/encontrar la base de datos, intentalo de nuevo.");
        }
        catch(IOException e){
            System.out.println("Error: ocurrio un problema con la carga de datos, intentalo de nuevo.");
        }
        catch (ClassNotFoundException e) {
            System.out.println("Error: no se pudo encontrar la clase de los objetos, intenta de nuevo.");
        }
        
        return listaMiembros;
    }
    /**
     * Lee y carga en el programa el Set de nombres de usuarios que esta almacenada en el archivo. Pueden llegar a ocurrir varias excepciones si por alguna razon no se encuentra el archivo o hay algun 
     * problema al intentar leer datos de este o bien si no se encuentra la clase.
     * @return 
     */
    public HashSet<String> cargarUsuarios(){
        HashSet<String> usuarios = new HashSet<>();
        
        try{
            entrada = new ObjectInputStream(new FileInputStream(rutaArchivo + "usr.obj"));
          
            usuarios = (HashSet<String>) entrada.readObject();
            
            entrada.close();
        }
        catch(FileNotFoundException e){
            System.out.println("Error: no se pudo conectar con la base de datos, intentalo de nuevo.");
        }
        catch(IOException e){
            System.out.println("Error: ocurrio un problema con la carga de datos, intentalo de nuevo.");
        } 
        catch (ClassNotFoundException e) {
            System.out.println("Error: no se pudo encontrar la clase de los objetos, intenta de nuevo.");
        }
        
        return usuarios;
    }
    /**
     * Se utiliza para buscar el archivo en la ruta especificada por el usuario. Este método no se implementa en ninguna parte del programa ya que el sistema de guardado es una abstracción que no corresponde al usuario.
     */
    private void ubicarArchivo(){
        System.out.print("\nRuta del archivo (con antidiagonales): ");
        rutaArchivo = input.nextLine();
        rutaArchivo += "\\";
        System.out.print("Nombre del archivo: ");
        rutaArchivo += input.nextLine();
    }
}
