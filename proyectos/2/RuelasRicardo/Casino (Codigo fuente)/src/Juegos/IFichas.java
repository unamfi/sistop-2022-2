package Juegos;
import Miembros.*;
/**
 * Interfaz para todos los juegos del casino, contiene los métodos que todo juego debe tener para el manejo de las fichas.
 * 
 */
public interface IFichas {
	double cobrar(double apuesta, String membresia);
	void apostar(double apuesta, Miembro mbr);
	double calcularBono(Miembro mbr, double apuesta);
}