package Excepciones;

/**
 *
 * Exception que se lanza cada vez que el usuario ingresa una opcion invalida en alguno de los menús de casino.
 */

public class FueraDeRango extends Exception {

    public FueraDeRango() {
    }

    public FueraDeRango(String msg) {
        super(msg);
    }
}
