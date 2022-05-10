#Método de uso: python3 ${nombre del archivo} ${PID}

import sys
arch=sys.argv[1]#El programa trabaja por medio de argumentos dados por consola
archivo=open("/proc/"+arch+"/maps")#Se busca la ruta que contiene la informacion del proceso
print('|'.ljust(5)+"Direccion de memoria".ljust(30)+'|'.ljust(3)+"Seccion".ljust(11)+'|'.ljust(3)+"Tamaño".ljust(7)+'|'.ljust(3)+"Páginas".ljust(9)+'|'.ljust(1)+"Permisos".ljust(6)+'|'.ljust(2)+"Directorio")
print('_'*136)
b=0#Bandera para la primer línea del archivo
for linea in archivo:
    proc=[]
    sec=''
    proc=linea.split(' ')#Se opera con la linea, dividiendo en subcadenas la informacion
    memp=proc[0].split('-')
    tam=int(memp[1],16)-int(memp[0],16)#Se obtiene el tamaño restando las direcciones en las que se encuentra
    pag=str((tam//4000))#Se obtiene el número de páginas haciendo una división de la memoria
    tam=str(int(pag)*4000)
    pag=pag+' pág'
    tam=tam[:-3]+'k'
    if(len(proc[-1])==1):
        proc[-1]='-Vacío--'#Si no se tiene un directorio se agrega Vacio
    if ('r-x' in proc[1])and('/usr/bin'in proc[-1])or b==0:#Se determina la seccion de memoria en la que se encuentra
        sec='Texto'
        b=b+1#Se inutiliza la bandera después del primer uso
        color="\x1b[0;31m"#Se determina un color de acuerdo a la seccion a la que pertenece
    elif('r'in proc[1]and'x'not in proc[1])and('/usr/bin'in proc[-1]):
        sec='Datos'
        color="\x1b[0;32m"
    elif('heap'in proc[-1]):
        sec='Heap'
        color="\x1b[0;34m"
    elif('r-x' in proc[1])and('/usr/lib/'in proc[-1]):
        sec='Bib→Texto'
        color="\x1b[0;36m"
    elif('r'in proc[1]and'x'not in proc[1])and('/usr/lib/'in proc[-1]):
        sec='Bib→Datos'
        color="\x1b[0;35m"
    elif('stack'in proc[-1]):
        sec='Stack'
        color="\x1b[0;33m"
    else:
        sec='-----'
        color="\x1b[0;37m"
    print(color+'|'.ljust(5)+proc[0].ljust(30)+'|'.ljust(5)+sec.ljust(9)+'|'.ljust(5)+tam.rjust(5)+'|'.ljust(5)+pag.rjust(7)+'|'.ljust(3)+proc[1].ljust(6)+'|'.ljust(2)+proc[-1][:-1].ljust(5))#Impresion de la informacíon con el color determinado y uso de padding para formato
    print('_'*136)
archivo.close()