package Excepciones;

/**
 * Excepcion que se lanza cuando el usuario a ingresado datos invalidos durante su registro en el sistema.
 * 
 */
public class DatosIncorrectos extends Exception{
    
    public DatosIncorrectos() {
    }

    public DatosIncorrectos(String msg) {
        super(msg);
    }
}
