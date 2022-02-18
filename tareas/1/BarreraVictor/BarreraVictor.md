​            

# Tarea 1: ¿Cuándo es una llamada al sistema?

```
Tarea creada: 2022.02.10
Entrega: 2022.02.17
Barrera Peña Victor Miguel  
```

# Código

```python
import re # Llamada al sistema para importaci
from Error import Error4,Error6,Error9 # Llamada al sistema para importaci
from DataBase import BaseDatos # Llamada al sistema para importacion

def q0(linea:str):
    pattern='^\s+'
    busqueda=re.search(pattern,linea)
    
    if busqueda:
        inicioSiguiente =busqueda.end() 
        return q1(linea[inicioSiguiente:]) #Llamada al sistema para regresar parametros en pila de ejecucion
    else:
        
        busqueda=re.search(pattern,' '+linea)
        if busqueda:
            inicioSiguiente =busqueda.end()-1 
            if q1(linea[inicioSiguiente:]) =='true':
                raise Error9.Error9('') #Llamada al sistema por interrupcion
            else:
                return 'false' #Llamada al sistema para regresar parametros en pila de ejecucion
        else:
            return 'false' #Llamada al sistema para regresar parametros en pila de ejecucion

def  q1(linea:str):
    pattern='^[a-zA-Z]+'
    busqueda=re.search(pattern, linea)
    
    if busqueda:
        return q2(linea) #Llamada al sistema para regresar parametros en pila de ejecucion
    else:
        return 'false' #Llamada al sistema para regresar parametros en pila de ejecucion
    
def q2(linea:str):
    pattern='^[a-zA-Z]+'
    busqueda=re.search(pattern, linea)
    
    if busqueda:
        finalActual =busqueda.end()
        inicioActual=busqueda.start()
        instruccion=linea[inicioActual:finalActual]
        instruccion=instruccion.lower()
        
        if BaseDatos.bdSearch(instruccion,1)!=None:
            return q5(linea[finalActual:])
        else:
            raise Error4.Error4('') #Llamada al sistema por interrupcion
    else:
        raise Error4.Error4('') #Llamada al sistema por interrupcion
    
def q5(linea:str):
    
    pattern='$'
    busqueda=re.search(pattern,linea)
    
    if busqueda:
        return 'true' #Llamada al sistema para regresar parametros en pila de ejecucion
    else:
        raise Error6.Error6('') # Llamada al sistema por interrupcion
    
    
def detectar(linea:str):
    try:
        resultado=q0(linea)
        return resultado 
    except Error4.Error4: #Llamada al sistema para atrapar interrupcion
        return 'e04' #Llamada al sistema para regresar parametros en pila de ejecucion
        
    except Error6.Error6:
        return 'e06' #Llamada al sistema para regresar parametros en pila de ejecucion
        
    except Error9.Error9:
        return 'e09' #Llamada al sistema para regresar parametros en pila de ejecucion
        
    except Exception as e: 
        print ("This is an error message!{}".format(e)) #Llamada al sistema para imprimir caracteres
        
```

  Para poder decir las llamadas la sistema ,copie un programa escrito en Python,borre todos los comentarios, y con los comentarios puse todas las llamadas al sistema que creí que existían.

- También tener en consideración que en python los comentarios son con `#`. 

-  La practica la realize desde un dispositivo Android donde dentro tiene ubuntu instalado pero sin interfaz gráfica, esto con el motivo de ver la posibilidad de desarrollar proyectos usando un celular, yo pienso que tenmos tanta potencia en nuestros bolsillos no aprovechada y por ello realize de esta manera la práctica, es duro, pero factible.                                                                                        - 

  

  > Herramientas > neovim, git, Ubuntu terminal para Android y un navegador web como Firefox. El problema es que no puedes subir el repo, pronto lo solucionaré.
