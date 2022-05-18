# Proyecto 4: (Micro) sistema de archivos
# Autores: Bryan Velasco & Christian Leyva 

# Imports: -------------------------------------------------------------------------------

# Bibliotecas incluidas en el core de Python
import os,sys,mmap
from datetime import datetime
from attr import has

# Bibliotecas que requieren instalación vía pip
from tabulate import tabulate
from termcolor import cprint

# Notas importantes:  ---------------------------------------------------------------------

# - Archivo de longitud fija de 1440 Kilobytes
# - La superficie del disco se divide en sectores de 256 bytes.
# - Cada cluster mide cuatro sectores. Es decir 1 cluster = 4*256 = 1024 bytes.
# - El primer cluster (#0) del pseudodispositivo es el superbloque. Este contiene información en los siguientes bytes: 
    # 0–8 -> Para identificación, el nombre del sistema de archivos. ¡Debes validar nunca modificar un sistema de archivos que no sea el correcto! Debe ser la cadena FiUnamFS.
    # 10–13 -> Versión de la implementación. Estamos implementando la versión 1.1
    # 20–35 -> Etiqueta del volumen
    # 40–45 -> Tamaño del cluster en bytes
    # 47–49 -> Número de clusters que mide el directorio
    # 52–60 -> Número de clusters que mide la unidad completa 
# - Toda la info se encuentra en el directorio ubicado entre los clusters 1 a 4, donde cada entrada mide 64 bytes y...
    # 0-15: Nombre del archivo
    # 16–24: Tamaño del archivo, en bytes
    # 25–30: Cluster inicial
    # 31–45: Hora y fecha de creación del archivo, especificando AAAAMMDDHHMMSS (p.ej. ‘20220508182600’ para 2022-05-08 18:26:00)
    # 46–60: Hora y fecha de última modificación del archivo, especificando AAAAMMDDHHMMSS (p.ej. ‘20220509182600’)
    # 61–64: Espacio no utilizado (¿reservado para expansión futura?)
# - Las entradas que no se utilizan llevan la cadena '...............'

# Se declaran algunas variables GLOBALES: --------------------------------------------------

entVacia= '...............' # Entrada de directorio no utilizada
nSistemaArch = 'FiUnamFS'
versionSistArch = '1.1'
SuperBloque = {}

# Ahora si, comienza la diversion -----------------------------------------------------------

def abrirImagen(filename):
    diskImg = open(filename,'r+b') # Se lee la imagen de disco con r+b -> 
    DIMap = mmap.mmap(diskImg.fileno(),0,access=mmap.ACCESS_READ)
    return DIMap

# Mediante las especificaciones otorgadas por el docente, se obtiene la info del superbloque
def obtenerInfoSuperBloque(DIMap):
    SuperBloque['nombre'] = DIMap[0:8].decode('utf-8')
    SuperBloque['version'] = DIMap[10:13].decode('utf-8').strip()
    SuperBloque['volumen'] = DIMap[20:35].decode('utf-8')
    SuperBloque['tamanio'] = int(DIMap[40:45].decode('utf-8'))
    SuperBloque['nClustersDir'] = DIMap[47:49].decode('utf-8')
    SuperBloque['nClustersCom'] = DIMap[52:60].decode('utf-8')

def getFecha(fecha):
    fechaObj = datetime.strptime(fecha,'%Y%m%d%H%M%S')
    fechaFormat = fechaObj.strftime('%c')

    return fechaFormat

def getArchivo(FileMap,cont):
    archivo ={}
    archivo['nombre'] = FileMap[0:15].decode('utf-8').rstrip('\x00')
    if archivo['nombre'] != entVacia and archivo['nombre']:
        archivo['tamanio'] = int(FileMap[16:24].decode('utf-8'))
        archivo['clusterInicial'] = int(FileMap[25:30].decode('utf-8'))
        archivo['fechaCreacion'] = getFecha(FileMap[31:45].decode('utf-8'))
        archivo['fechaModificacion'] = getFecha(FileMap[46:60].decode('utf-8'))
        archivo['nDireccion'] = cont
    else:
        archivo = None
    return archivo

# Funcion para listar los archivos en la imagen de disco
def ls(DIMap):
    # Recordando que el tamaño de cada cluster es 1024 bytes
    # Y que el directorio se encuentra entre el Cluster 1-4, se debe empezar a buscar desde 1024 hasta 4096 
    #  Por tanto considerando las entradas de 64 bytes...
    # Se inicializa el diccionario con los titulos de las columnas para ser mostradas mas adelante en consola
    archivos = []
    temp={}
    temp['nombre'] = 'Nombre del archivo'
    temp['tamanio'] = 'Tamaño del archivo'
    temp['clusterInicial'] = 'Cluster inicial'
    temp['fechaCreacion'] = 'Fecha de creación'
    temp['fechaModificacion'] = 'Fecha de modificación'
    temp['nDireccion'] = 'Bandera dirección de memoria'
    archivos.append(temp)

    for i in range(0,64):
        desde = 1024 + i * 64
        hasta = desde + 64
        
        archivoLeido = getArchivo(DIMap[desde:hasta],i)
        if not archivoLeido is None:
            archivos.append(archivoLeido)

    return archivos

# Copiar archivo de FiUnamFs a tu sistema
def copy_export(DIMap,filename:str,ruta:str):
    archivos = ls(DIMap)
    # print(archivos)
    # Se busca que el archivo exista en el directorio
    for i in archivos:
        if i['nombre'].strip() == filename:
            if os.path.exists(ruta):
                with open(f"{ruta}/{filename}", "a+b") as export:
                    desde = SuperBloque['tamanio'] * i['clusterInicial']
                    hasta = desde + i['tamanio']
                    export.write(DIMap[desde:hasta])
            else:
                cprint(f'Error: No se encontro la ruta: \'{ruta}\' en el sistema; Verifica que exista o este bien escrita.','white','on_red')
            return 
    
    cprint(f'Error: No se encontro el archivo \'{filename}\' en FiUnamFs.','white','on_red')

def copy_import():
    pass
def rm(DIMap,filename:str):
    pass
def defragmentar():
    pass    

def sistemaArchivos(DIMap):
    helpComandos = {'Comando':['ls','export [nombreArchivo] [rutaLocal]','import [nombreArchivo]','del [nombreArchivo]','exit'],'Descripción':['Listar contenidos del directorio FiUnamFs','Copia el archivo ([nombreArchivo]) de FiUnamFs a la ruta ([rutaLocal]) de tu sistema','Copia el archivo ([nombreArchivo]) de tu sistema a FiUnamFs','Elimina el archivo ([nombreArchivo]) de FiUnamFs','Salir del programa.']}
    salir = False
    while not salir:
        entry = input(">>>  ")
        param = entry.split()
        # Se verifica el tipo de operacion que se desea hacer:
        
        if len(param) == 0:
            cprint('Por favor, ingresa un comando.\nEscribe \'help\' para mostrar los comandos disponibles','white','on_red')

        # ls -> Listar contenidos del directorio FiUnamFs
        elif param[0] == 'ls':
            try:
                archivos = ls(DIMap)
                print(tabulate(archivos,headers="firstrow",tablefmt='github'))
            except:
                cprint('Lo siento, sucedio un error al listar los archivos, vuelve a intentarlo y si el error persiste por favor reportalo a: chris@chrisley.dev','white','on_red')

        # Copiar archivo de FiUnamFs a tu sistema
        elif param[0] == 'export':
            try:
                if len(param) > 2:
                    copy_export(DIMap,param[1],param[2])
                else:
                    cprint('Error: Ingresa TODOS los parametros necesarios.\nEjemplo:\n\texport [nombreArchivo] [rutaLocal]','white','on_red')
            except:
                cprint('Lo siento, sucedio un error al exportar el archivo, vuelve a intentarlo y si el error persiste por favor reportalo a: chris@chrisley.dev','white','on_red')
        
        # Copiar archivo de tu sistema a FiUnamFs
        elif param[0] == 'import':
            pass
        
        # Eliminar archivo de FiUnamFs
        elif param[0] == 'del':
            pass
        
        elif param[0] == 'help':
            print(tabulate(helpComandos,headers='keys'))

        elif param[0] == 'exit':
            salir = True
        else:
            cprint('El comando \'' + param[0] + '\' no existe\nEscribe \'help\' para mostrar los comandos disponibles','white','on_red')

def main():
    # Primero se abre y mapea la imagen de memoria
    filename = 'fiunamfs.img'
    # Se abre el archivo
    try:
        DIMap = abrirImagen(filename)
    except:
        cprint('Error: El archivo no se puede abrir. Verifica que su nombre sea \'fiunamfs.img\' y que se encuentre en el directorio','white','on_red')

    obtenerInfoSuperBloque(DIMap)
    # Se verifica que el sistema de archivos sea FiUnamFS para proceder.
    if SuperBloque['nombre'] == nSistemaArch:
        if SuperBloque['version'] == versionSistArch:
            sistemaArchivos(DIMap)
        else:
            cprint('Error: La versión del sistema de archivos no es la 1.1','white','on_red')
    else:
        cprint('Error: El sistema de archivos no es: FiUnamFS','white','on_red')
main()