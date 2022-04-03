# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 23:41:59 2022

@author: Correa González Alfredo
"""
import random
import time
import threading
from threading import Thread,Semaphore

personas_generadas = []

tiempo_espera = 0.1
tiempo_espera_2 = 0.05

mutex_crear_lista = Semaphore(1)
mutex_repartir = Semaphore(1)
mutex_monto_1 = Semaphore(1)
mutex_monto_2 = Semaphore(1)
mutex_monto_3 = Semaphore(1)
mutex_monto_4 = Semaphore(1)
mutex_monto_5 = Semaphore(1)

mutex_imprimir_desordenado = Semaphore(1)
mutex_imprimir_ordenado = Semaphore(1)



# Monticulos de documentos
monto_1 = []
monto_2 = []
monto_3 = []
monto_4 = []
monto_5 = []

a = []
b = []
c = []
d = []
e = []
f = []
g = []
h = []
letra_i = []
j = []
k = []
l = []
m = []
n = []
ñ = []
o = []
p = []
q = []
r = []
s = []
t = []
u = []
v = []
w = []
x = []
y = []
z = []

#Creando los hilos que simulan las personas


#Clasificar por letras
#Ordenar los montículos de letras
#Unir los montículos


#Función crear nombres
def crear_Nombres():
    
    
    mutex_crear_lista.acquire()
    
    #Lista de nombres:
        
    nombres = [
    "Mateo",
    "Daniel",
    "Pablo",
    "Alvaro",
    "Adrian",
    "David",
    "Diego",
    "Javier",
    "Mario",
    "Link",
    "Marcos",
    "Manuel",
    "Martin",
    "Nicolas",
    "Ivan",
    "Carlos",
    "Migeul",
    "Lucas",
    "Abdel",
    "Adib",
    "Akram",
    "Bahir",
    "Farid",
    "Habib",
    "Hakim",
    "Hasan",
    "Ibrahim",
    "Jamal",
    "Khalil",
    "Moad",
    "Nader",
    "Rayan",
    "Walid",
    "Zaid",
    "Atticus",
    "Asher",
    "Ezra",
    "Silas",
    "Declan",
    "Wyatt",
    "Oliver",
    "Henrry",
    "Milo",
    "Jude",
    "Liam",
    "Austin",
    "Axel",
    "Alexander",
    "Jacob",
    "Luke",
    "Everett",
    "Matias",
    "Angel",
    "Gabriel",
    "Simon",
    "Thiago",
    "Valentin",
    "Julian",
    "Benjamin",
    "Erick",
    "Sasha",
    "Dante",
    "Enzo",
    "Silas",
    "Marco",
    "Andrea",
    "Ariel",
    "Fabrizo",
    "Santino",
    "Alonzo",
    "Adriano",
    "Carlo",
    "Donato",
    "Giovanni",
    "Lorenzo",
    "Guido",
    "Luigi",
    "Filippo",
    "Geronimo",
    "Flavio",
    "Leonardo",
    "Luciano",
    "Maurizio",
    "Piero",
    "Romeo",
    "Orfeo",
    "Jason",
    "Hector",
    "Aquiles",
    "Adonis",
    "Apolo",
    "Dionisio",
    "Ulises",
    "Hercules",
    "Hipolito",
    "Tristan",
    "Zeus",
    "Sebastian",
    "Alfredo",
    "Sofia",
    "Camila",
    "Valentina",
    "Isabella",
    "Valeria",
    "Daniela",
    "Mariana",
    "Sara",
    "Victoria",
    "Gabriela",
    "Ximena",
    "Andrea",
    "Natalia",
    "Mia",
    "Martina",
    "Lucia",
    "Samantha",
    "Maria",
    "Fernanda",
    "Nicole",
    "Alejandra",
    "Paula",
    "Emily",
    "Marijo",
    "Luciana",
    "Ana",
    "Melanie",
    "Regina",
    "Catalina",
    "Ashley",
    "Renata",
    "Agustina",
    "Abril",
    "Emma",
    "Emmilia",
    "Jazmin",
    "Juanita",
    "Briana",
    "Vanessa",
    "Antonia",
    "Laura",
    "Antonella",
    "Luna",
    "Carla",
    "Allison",
    "Monserrat",
    "Paulina",
    "Isabel",
    "Juliana",
    "Paulin",
    "Valerie",
    "Florencia",
    "Adriana",
    "Naomi",
    "Amanda",
    "Adriana",
    "Zelda",
    "Natalie",
    "Constanza",
    "Lola",
    "Zoe",
    "Carolina",
    "Micaela",
    "Julia",
    "Claudia",
    "Paola",
    "Alexa",
    "Elena",
    "Isidora",
    "Rebeca",
    "Josefina",
    "Abigail",
    "Julieta",
    "Melissa",
    "Michelle",
    "Alba",
    "Camila",
    "Angela",
    "Delfina",
    "Atiana",
    "Stephanie",
    "Fatima",
    "Alexandra",
    "Paloma",
    "Amelia",
    "Clara",
    "Laura",
    "Diana",
    "Guadalupe",
    "Barbara",
    "Bianca",
    "Miranda",
    "Sarina",
    "Pilar",
    "Marta",
    "Helena",
    "Wendy",
    "Violeta",
    "Zaira",
    "Beatriz",
    "Tamara"
            ]
    
    # Lista de apellidos
    
    apellidos = [
    "Hernandez",
    "Garcia",
    "Martinez",
    "Lopez",
    "Gonzalez",
    "Perez",
    "Rodriguez",
    "Sanchez",
    "Ramirez",
    "Cruz",
    "Flores",
    "Gomez",
    "Morales",
    "Vasquez",
    "Reyes",
    "Jimenez",
    "Torres",
    "Diaz",
    "Gutierrez",
    "Ruiz",
    "Mendoza",
    "Aguilar",
    "Ortiz",
    "Moreno",
    "Castillo",
    "Romero",
    "Alvarez",
    "Mendez",
    "Chavez",
    "Rivera",
    "Juarez",
    "Ramos",
    "Dominguez",
    "Herrera",
    "Medina",
    "Castro",
    "Vargas",
    "Guzman",
    "Velazquez",
    "Rojas",
    "Cruz",
    "Contreras",
    "Salazar",
    "Luna",
    "Ortega",
    "Zuñiga",
    "Guerrero",
    "Estrada",
    "Bautista",
    "Correa",
    "Torres",
    "Cortes",
    "Soto",
    "Alvarado",
    "Espinoza",
    "Lara",
    "Avila",
    "Rios",
    "Cervantes",
    "Silva",
    "Delgado",
    "Vega",
    "Marquez",
    "Sandoval",
    "Carrillo",
    "Fernandez",
    "Leon",
    "Mejia",
    "Solis",
    "Rosas",
    "Ibarra",
    "Valdez",
    "Nuez",
    "Campos",
    "Santos",
    "Camacho",
    "Navarro",
    "Mendoza",
    "Maldonado",
    "Rosales",
    "Acosta",
    "Pea",
    "Miranda",
    "Cabrera",
    "Valencia",
    "Nava",
    "Pacheco",
    "Robles",
    "Molina",
    "Fuentes",
    "Rangel",
    "Huerta",
    "Meza",
    "Padilla",
    "Salas",
    "Cardenas",
    "Valenzuela",
    "Ayala",
    "Suaso",
    "Meras"
                ]
    # Creando la lista de personas aleatoriamente (cada persona tiene sus documentos)
    
    
    
    for i in range(300):
        
        persona = apellidos[random.randint(0, 99)] + " " + apellidos[random.randint(0, 99)] + " " + nombres[random.randint(0, 199)]
        personas_generadas.append(persona)
    
    print("----------------------------------")
    print("PERSONAS QUE ENTREGARON DOCUMENTOS")
    print("----------------------------------")
    
    for i in personas_generadas:
        print(i)
    time.sleep(tiempo_espera)
    print("----------------------------------")
    print("PERSONA 1 RECIBIÓ LOS DOCUMENTOS")
    print("----------------------------------")
    mutex_crear_lista.release()
    repartir_monto(personas_generadas)


def repartir_monto(personas_generadas):
    
    mutex_repartir.acquire()
    

    # Reaprtiendo a documentos en cada monto:    
    # Monto 1
    for i in range(300): 
        if len(personas_generadas) > 0:
            documento = personas_generadas.pop()
            monto_1.append(documento)

            print("-------------------------------")    
            print("DOCUMENTOS EN EL MONTO 1:")   
            print("-------------------------------") 
            for i in monto_1:
                print(i)
            time.sleep(tiempo_espera)
            mutex_repartir.release()
            clasificar_letra_monto_1(monto_1)

"""
    # Monto 2    
    for i in range(60):     
        documento = personas_generadas.pop()
        monto_2.append(documento)

    print("-------------------------------")    
    print("DOCUMENTOS EN EL MONTO 2:")   
    print("-------------------------------") 
    for i in monto_2:
        print(i)
    time.sleep(tiempo_espera)
        
    # Monto 3    
    for i in range(60):     
        documento = personas_generadas.pop()
        monto_3.append(documento)

    print("-------------------------------")    
    print("DOCUMENTOS EN EL MONTO 3:")   
    print("-------------------------------") 
    for i in monto_3:
        print(i)   
    time.sleep(tiempo_espera)
        
    # Monto 4    
    for i in range(60):     
        documento = personas_generadas.pop()
        monto_4.append(documento)

    print("-------------------------------")    
    print("DOCUMENTOS EN EL MONTO 4:")   
    print("-------------------------------") 
    for i in monto_4:
        print(i)
    time.sleep(tiempo_espera)    
        
    # Monto 5    
    for i in range(60):     
        documento = personas_generadas.pop()
        monto_5.append(documento)

    print("-------------------------------")    
    print("DOCUMENTOS EN EL MONTO 5:")   
    print("-------------------------------") 
    for i in monto_5:
        print(i)
        """
   
    
    
    
def clasificar_letra_monto_1(monto_1):
    time.sleep(0.2)
    mutex_monto_1.acquire()
    # Separar letra A
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS A EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "A"):
                a.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra A")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra B
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS B EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "B"):
                b.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra B")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra C
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS C EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "C"):
                c.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra C")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)    
            
    # Separar letra D
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS D EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "D"):
                d.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra D")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra E
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS E EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "E"):
                e.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra E")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra F
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS F EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "F"):
                f.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra F")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra G
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS G EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "G"):
                g.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra G")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra H
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS H EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "H"):
                h.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra H")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra I
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS I EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "I"):
                letra_i.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra I")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra J
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS J EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "J"):
                j.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra J")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra K
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS K EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "K"):
                k.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra K")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra L
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS L EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "L"):
                l.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra L")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra M
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS M EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "M"):
                m.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra M")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra N
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS N EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "N"):
                n.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra N")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra Ñ
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS Ñ EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "Ñ"):
                ñ.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra Ñ")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra O
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS O EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "O"):
                o.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra O")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra P
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS P EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "P"):
                p.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra P")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra Q
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS Q EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "Q"):
                q.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra Q")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra R
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS R EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "R"):
                r.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra R")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra S
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS S EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "S"):
                s.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra S")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra T
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS T EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "T"):
                t.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra T")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra U
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS U EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "U"):
                u.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra U")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra V
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS V EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "V"):
                v.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra V")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra W
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS W EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "W"):
                w.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra W")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra X
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS X EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "X"):
                x.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra X")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
            
    # Separar letra Y
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS Y EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "Y"):
                y.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra Y")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
        
    # Separar letra Z
    print("------------------------------------------")
    print("REVISANDO SI HAY LETRAS Z EN EL MONTO 1")
    print("------------------------------------------")
    for i in range(300):
        if len(monto_1) > 0:
            temporal = monto_1.pop(0)
            #print(temporal[0])
            if (temporal[0] == "Z"):
                z.append(temporal)
                print(f"Se agregó {temporal} al monto de la letra Z")
                time.sleep(tiempo_espera_2)
            else:
                monto_1.append(temporal)
    mutex_monto_1.release()
    imprimir_desordenado(monto_1)
    
def imprimir_desordenado(monto_1):
    mutex_imprimir_desordenado.acquire()
    # Imprimir por letras separadas
    print("------------------------------------------")
    print("IMPRIMIENDO POR LETRAS")
    print("------------------------------------------")

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(g)
    print(h)
    print(letra_i)
    print(j)
    print(k)
    print(l)
    print(m)
    print(n)
    print(ñ)
    print(o)
    print(p)
    print(q)
    print(r)
    print(s)
    print(t)
    print(u)
    print(v)
    print(w)
    print(x)
    print(y)
    print(z)
    mutex_imprimir_desordenado.release()
    imprimir_ordenado(monto_1)

def imprimir_ordenado(monto_1):
    mutex_imprimir_ordenado
    
    print("---------------------")   
    print("ORDENADA")  
    print("---------------------")    

    nueva_a =sorted(a, reverse = False)
    print(nueva_a)

    nueva_b =sorted(b, reverse = False)
    print(nueva_b)

    nueva_c =sorted(c, reverse = False)
    print(nueva_c)

    nueva_d =sorted(d, reverse = False)
    print(nueva_d)

    nueva_e =sorted(e, reverse = False)
    print(nueva_e)

    nueva_f =sorted(f, reverse = False)
    print(nueva_f)

    nueva_g =sorted(g, reverse = False)
    print(nueva_g)

    nueva_h =sorted(h, reverse = False)
    print(nueva_h)

    nueva_i =sorted(letra_i, reverse = False)
    print(nueva_i)

    nueva_j =sorted(j, reverse = False)
    print(nueva_j)

    nueva_k =sorted(k, reverse = False)
    print(nueva_k)

    nueva_l =sorted(l, reverse = False)
    print(nueva_l)

    nueva_m =sorted(m, reverse = False)
    print(nueva_m)

    nueva_n =sorted(n, reverse = False)
    print(nueva_n)

    nueva_ñ =sorted(ñ, reverse = False)
    print(nueva_ñ)

    nueva_o =sorted(o, reverse = False)
    print(nueva_o)

    nueva_p =sorted(p, reverse = False)
    print(nueva_p)

    nueva_q =sorted(q, reverse = False)
    print(nueva_q)

    nueva_r =sorted(r, reverse = False)
    print(nueva_r)

    nueva_s =sorted(s, reverse = False)
    print(nueva_s)

    nueva_t =sorted(t, reverse = False)
    print(nueva_t)

    nueva_u =sorted(u, reverse = False)
    print(nueva_u)

    nueva_v =sorted(v, reverse = False)
    print(nueva_v)

    nueva_w =sorted(w, reverse = False)
    print(nueva_w)

    nueva_x =sorted(x, reverse = False)
    print(nueva_x)

    nueva_y =sorted(y, reverse = False)
    print(nueva_y)

    nueva_z =sorted(z, reverse = False)
    print(nueva_z)
    
    mutex_imprimir_ordenado.release()
    
    

persona_1 = threading.Thread(target = crear_Nombres)
persona_1.start()

persona_2 = threading.Thread(target = repartir_monto(personas_generadas))
persona_2.start()

persona_3 = threading.Thread(target = clasificar_letra_monto_1(monto_1))
persona_3.start()

persona_4 = threading.Thread(target = imprimir_desordenado(monto_1))
persona_4.start()

persona_5 = threading.Thread(target = imprimir_ordenado(monto_1))
persona_5.start()





    
    

    
    





