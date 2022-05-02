# Proyecto 3 Christian Leyva

import sys

# Obtiene el PID el cual se pasa como argumento
def getArgs():
    return sys.argv[1]

def main():
    try:
        PID = getArgs()
    except:
        print("Por favor ingresa el PID del proceso a leer. \nEjemplo de ejecución:\n\n\tpython3 proyecto3_chrisley.py {PID}\n")
        return

    print("EL PID ES " + PID)

main()