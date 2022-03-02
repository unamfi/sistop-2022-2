/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package ejercicio4;

import java.util.LinkedList; 
import java.util.Random;


/**
 *
 * @author Ricardo Ruelas
 */

public class ProductorConsumidor { 
    
        // Crea una lista compartida por el productor y el consumidor
        // El tamaño de la lista es de 2
        LinkedList<Integer> lista = new LinkedList<>(); 
        Random rnd = new Random();
        int capacidad = 2; 
  
        // Función llamada por el hilo productor
        public void producir() throws InterruptedException 
        { 
            int valor = 0; 
            while (true) { 
                synchronized (this) 
                { 
                    // el hilo productor espera si la lista
                    // esta llena
                    while (lista.size() == capacidad) 
                        wait(); 
                    
                    valor = rnd.nextInt(100);
                    System.out.println("Producido -> "
                                       + valor); 
  
                    // inserta los datos en la lista 
                    lista.add(valor); 
                    
                    System.out.println("Bufer: " + lista.toString());
                    
                    // notifica al hilo consumidor que ahora
                    // puede comenzar su ejecución
                    notify(); 
  
                    // se pone al hilo en espera para hacer
                    // más facil de entender el programa
                    Thread.sleep(1000); 
                } 
            } 
        } 
  
        // Función llamada por el hilo consumidor
        public void consumir() throws InterruptedException { 
            while (true) { 
                synchronized (this) 
                {
                    // hilo consumidor espera hasta que la lista
                    // este vacía
                    while (lista.isEmpty()) 
                        wait(); 
  
                    // se recupera el primer dato de la lista 
                    int val = lista.removeFirst(); 
  
                    System.out.println("Consumido -> "
                                       + val); 
  
                    System.out.println("Bufer: " + lista.toString());
                    
                    // Despierta al hilo productor
                    notify(); 
  
                    // Pone al hilo en espera
                    Thread.sleep(1000); 
                } 
            } 
        } 
} 