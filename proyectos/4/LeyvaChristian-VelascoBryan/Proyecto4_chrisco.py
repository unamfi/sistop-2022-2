# Proyecto 4: (Micro) sistema de archivos
# Autores: Bryan Velasco & Christian Leyva 

# Imports: -------------------------------------------------------------------------------

# Bibliotecas incluidas en el core de Python
import os,mmap,traceback, math
from datetime import datetime
import shutil

# Bibliotecas que requieren instalación vía pip
from tabulate import tabulate
from termcolor import cprint

# Notas importantes:  ---------------------------------------------------------------------

# - Archivo de longitud fija de 1440 Kilobytes
# - La superficie del disco se divide en sectores de 256 bytes.
# - Cada cluster mide cuatro sectores. Es decir 1 cluster = 4*256 = 1024 bytes.
# ⚠️ IMPORTANTE: Al momento de realizar el programa, notamos que el sistema de archivos no utiliza clusters de 1024 bytes, si no que utiliza clusters de 2048 bytes. Tal vez fue un dedazo del profesor?
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
diskImg = None
DIMap = None
imgFilename = 'copiaSistemaArchivos.img'

# Ahora si, comienza la diversion -----------------------------------------------------------

def verificaCopia():
    OriginalimgFilename = './fiunamfs.img'
    if not os.path.exists(imgFilename):
        shutil.copy(OriginalimgFilename,'./'+imgFilename)
        cprint('Se creo una copia de \'fiunamfs.img\' exitosamente.','blue','on_green')

# Mediante las especificaciones otorgadas por el docente, se obtiene la info del superbloque
def obtenerInfoSuperBloque():
    SuperBloque['nombre'] = DIMap[0:8].decode('utf-8')
    SuperBloque['version'] = DIMap[10:13].decode('utf-8').strip()
    SuperBloque['volumen'] = DIMap[20:35].decode('utf-8')
    SuperBloque['tamanio'] = int(DIMap[40:45].decode('utf-8'))
    SuperBloque['nClustersDir'] = int(DIMap[47:49].decode('utf-8'))
    SuperBloque['nClustersCom'] = int(DIMap[52:60].decode('utf-8'))
    # print(SuperBloque)

def getFecha(fecha):
    fechaObj = datetime.strptime(fecha,'%Y%m%d%H%M%S')
    fechaFormat = fechaObj.strftime('%c')

    return fechaFormat

def getArchivos(FileMap,cont):
    archivo ={}
    archivo['nombre'] = FileMap[0:15].decode('utf-8').rstrip('\x00')
    if archivo['nombre'] != entVacia and archivo['nombre']:
        archivo['tamanio'] = int(FileMap[16:24].decode('utf-8'))
        archivo['clusterInicial'] = int(FileMap[25:30].decode('utf-8'))
        archivo['fechaCreacion'] = getFecha(FileMap[31:45].decode('utf-8'))
        archivo['fechaModificacion'] = getFecha(FileMap[46:60].decode('utf-8'))
        archivo['cont'] = cont
    else:
        archivo = None
    return archivo

def getListadoComp(FileMap,cont):
    archivo ={}
    archivo['nombre'] = FileMap[0:15].decode('utf-8').rstrip('\x00')
    if archivo['nombre'] != entVacia and archivo['nombre']:
        archivo['tamanio'] = int(FileMap[16:24].decode('utf-8'))
        archivo['clusterInicial'] = int(FileMap[25:30].decode('utf-8'))
        archivo['fechaCreacion'] = getFecha(FileMap[31:45].decode('utf-8'))
        archivo['fechaModificacion'] = getFecha(FileMap[46:60].decode('utf-8'))
        archivo['cont'] = cont
    elif archivo['nombre'] == entVacia:
        archivo['tamanio'] = int(FileMap[16:24].decode('utf-8'))
        archivo['clusterInicial'] = int(FileMap[25:30].decode('utf-8'))
        archivo['fechaCreacion'] = '-'
        archivo['fechaModificacion'] = '-'
        archivo['cont'] = cont
    else:
        archivo = None

    return archivo

# Funcion para listar los archivos en la imagen de disco
def ls(param=None):
    # Recordando que el tamaño de cada cluster es 1024 bytes
    # Y que el directorio se encuentra entre el Cluster 1-4, se debe empezar a buscar desde 1024 hasta 4096 
    # Por tanto que cada entrada del directorio mide 64 bytes...
    # Se inicializa el diccionario con los titulos de las columnas para ser mostradas mas adelante en consola
    archivos = []
    temp={}
    temp['cont'] = 'n'
    temp['nombre'] = 'Nombre del archivo'
    temp['tamanio'] = 'Tamaño del archivo'
    temp['clusterInicial'] = 'Cluster inicial'
    temp['fechaCreacion'] = 'Fecha de creación'
    temp['fechaModificacion'] = 'Fecha de modificación'
    archivos.append(temp)

    for i in range(0,96):
        desde = SuperBloque['tamanio'] + i * 64
        hasta = desde + 64
        
        if param is None:
            archivoLeido = getArchivos(DIMap[desde:hasta],i)
        elif param == '-comp':
            archivoLeido = getListadoComp(DIMap[desde:hasta],i)

        if not archivoLeido is None:
            archivos.append(archivoLeido)

    return archivos

# Busca si un archivo se encuentra en el sistema FiUnamFs
def FSgoogle(archivos,filename):
    for archivo in archivos:
        if archivo['nombre'].strip() == filename:
            return archivo
    return None

# Copiar archivo de FiUnamFs a tu sistema
def copy_export(filename:str,ruta:str):
    archivos = ls()
    # Se busca que el archivo exista en el directorio
    archivo = FSgoogle(archivos,filename)
    if not archivo is None:
        if os.path.exists(ruta):
            with open(f"{ruta}/{filename}", "a+b") as export:
                desde = SuperBloque['tamanio'] * archivo['clusterInicial']
                hasta = desde + archivo['tamanio']
                export.write(DIMap[desde:hasta])
        else:
            cprint(f'Error: No se encontro la ruta: \'{ruta}\' en el sistema; Verifica que exista o este bien escrita.','white','on_red')
    else:
        cprint(f'Error: No se encontro el archivo \'{filename}\' en FiUnamFs.','white','on_red')

# Obtiene el archivo con el cluster inicial mas grande
def getMaxInitCluster(archivos):
    # El minimo debe ser 5 para reservar la memoria del directorio
    maxClusterFile = None
    maxInitCluster = 0
    if len(archivos) > 0:
        for archivo in archivos:
            if not archivo['cont'] == 'n':
                if archivo['clusterInicial'] > maxInitCluster:
                    maxInitCluster = archivo['clusterInicial']
                    maxClusterFile = archivo

    return maxClusterFile

# Se crean las meta etiquetas (Info en directorio)
def copyFileInto(maxClusterFile,filename,fileSize,nClusters,contLast):
    # Se obtiene el cluster desde donde el nuevo archivo se escribirá
    # clusterinicial + clustersNecesarios 
    initialCluster = maxClusterFile['clusterInicial'] +  math.ceil(maxClusterFile['tamanio'] / SuperBloque['tamanio'] ) + 1
    finalCluster = initialCluster +  nClusters
    global DIMap
    
    for i in range(contLast + 1,64):
        desde = SuperBloque['tamanio'] + i * 64
        hasta = desde + 64
        apartado = getListadoComp(DIMap[desde:hasta],i)
        # Cuando encuentra el apartado en el directorio vacio
        if entVacia == apartado['nombre']:
            
            # Se escriben las metatags
            fechaActual = datetime.now()
            # Nombre archivo
            DIMap[desde + 0:desde + 15] = filename.rjust(15).encode('ASCII')
            # Tamaño archivo
            DIMap[desde + 16:desde + 24]= str(fileSize).zfill(8).encode('ASCII')
            # Cluster inicial
            DIMap[desde + 25:desde + 30] = str(initialCluster).zfill(5).encode('ASCII')
            # Fecha Creacion
            DIMap[desde + 31:desde + 45] = fechaActual.strftime("%Y%m%d%H%M%S").encode('ASCII')
            # Fecha modificacion
            DIMap[desde + 46:desde + 60] = fechaActual.strftime("%Y%m%d%H%M%S").encode('ASCII')
            
            # Se escribe el archivo
            with open(filename,'rb') as file:
                desdeWrite = SuperBloque['tamanio'] * initialCluster
                hastaWrite = desdeWrite + fileSize
                DIMap[desdeWrite:hastaWrite] = file.read()
            return 

# Copiar archivo de tu sistema a FiUnamFs
def copy_import(filename):
    if os.path.isfile(filename):
        # El archivo no puede ser mayor a 15 caracteres
            if len(filename) < 15:
                # Se verifica que el archivo NO se encuentre ya en el disco
                archivos = ls()
                if FSgoogle(archivos, filename) is None:
                    # Se obtiene el tamaño del archivo a copiar hacia el sistema de archivos
                    fileSize = os.stat(filename).st_size
                    # Se obtienen los clusters que requiere el archivo (redondeando)
                    nClusters = math.ceil(fileSize/SuperBloque['tamanio']) # nbytes / 2048 bytes (tamaño de los clusters en el sistema de arch.)

                    maxClusterFile = getMaxInitCluster(archivos)

                    # Si hay archivos
                    if not maxClusterFile is None:
                        # Se verifica que exista espacio para el archivo
                        if  nClusters <= (SuperBloque['nClustersCom'] - maxClusterFile['clusterInicial'] +  int(maxClusterFile['tamanio'] / SuperBloque['tamanio'] )):
                            # Se crean las 'meta tags' en el directorio & se escribe el archivo:
                            copyFileInto(maxClusterFile,filename,fileSize,nClusters,maxClusterFile['cont'])
                        else:
                            cprint(f'Error: No hay suficiente espacio para almacenar el archivo \'{filename}\'. Intenta con un archivo mas pequeño :).','white','on_red')
                    # Si no hay archivos
                    else:
                        # Se verifica si hay espacio (clusters) para almacenar el archivo
                        # Total clusters - 4 clusters (Reservados para el directorio)
                        if  nClusters <= (SuperBloque['nClustersCom'] - SuperBloque['nClustersDir']):
                            # Se crea un map con los datos requeridos (fijos) debido a que no hay archivos
                            temp = {'clusterInicial': 5,'tamanio':0}
                            copyFileInto(temp,filename,fileSize,nClusters,0)
                        else:
                            cprint(f'Error: El archivo \'{filename}\' es demasiado GRANDE. Intenta con un archivo mas pequeño :).','white','on_red')
                else:
                    cprint(f'Error: El archivo \'{filename}\' ya se encuentra en FiUnamFs, por favor cambia el nombre del archivo.','white','on_red')
            else:
                cprint(f'Error: El nombre del archivo es mayor o igual a 15 caracteres.','white','on_red')
    else:
        cprint(f'Error: No se encontro el archivo \'{filename}\' en el sistema.','white','on_red')

def rm(filename:str):
    archivos = ls()
    # Se busca que el archivo exista en el directorio
    archivo = FSgoogle(archivos,filename)
    if not archivo is None:
        # Se elimina la informacion en el directorio
        desde = SuperBloque['tamanio'] + 64 * archivo['cont']
        DIMap[desde + 0:desde + 15] = bytes(entVacia, 'ASCII')
        DIMap[desde+16:desde+24] = bytes("".zfill(8), 'ASCII')
        DIMap[desde+25:desde+30] = bytes("".zfill(5), 'ASCII')
        DIMap[desde+31:desde+45] = bytes("".zfill(14), 'ASCII')
        DIMap[desde+46:desde+60] = bytes("".zfill(14), 'ASCII')

        # Se eliminan los datos
        desdeWrite = SuperBloque['tamanio'] * archivo['clusterInicial']
        hastaWrite = desdeWrite + archivo['tamanio']
        DIMap[desdeWrite:hastaWrite] = bytes("".zfill(hastaWrite-desdeWrite), 'ASCII')
    else:
        cprint(f'Error: No se encontro el archivo \'{filename}\' en FiUnamFs.','white','on_red')

# Ya no nos dio tiempo de implementar la desfragmentacion ☹️
def defragmentar():
    pass    

def sistemaArchivos():
    helpComandos = {'Comando':['ls [parametroOpcional]','export [nombreArchivo] [rutaLocal]','import [nombreArchivo]','rm [nombreArchivo]','superinfo','exit'],'Descripción':['Listar contenidos del directorio FiUnamFs. El parametro \'-comp\' muestra el listado de archivos incluyendo direcciones vacias.','Copia el archivo ([nombreArchivo]) de FiUnamFs a la ruta ([rutaLocal]) de tu sistema','Copia el archivo ([nombreArchivo]) de tu sistema a FiUnamFs','Elimina el archivo ([nombreArchivo]) de FiUnamFs','Muestra la información almacenada en el superbloque del cluster 0.','Salir del programa.']}
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
                if len(param) == 1: 
                    archivos = ls()
                    print(tabulate(archivos,headers="firstrow",tablefmt='github')+'\n')
                elif param[1] == '-comp':
                    archivos = ls(param=param[1])
                    print(tabulate(archivos,headers="firstrow",tablefmt='github')+'\n')
                else:
                    cprint(f'Error: El parametro \'{param[1]}\' ingresado es incorrecto.\nEscribe \'help\' para ver los comandos y parametros disponibles.','white','on_red')
            except Exception as e:
                # print(e)
                cprint('Lo siento, sucedio un error al listar los archivos, vuelve a intentarlo y si el error persiste por favor reportalo a: chris@chrisley.dev','white','on_red')

        # Copiar archivo de FiUnamFs a tu sistema
        elif param[0] == 'export':
            try:
                if len(param) > 2:
                    copy_export(param[1],param[2])
                else:
                    cprint('Error: Ingresa TODOS los parametros necesarios.\nEjemplo:\n\texport [nombreArchivo] [rutaLocal]','white','on_red')
            except Exception as e:
                print(e)
                cprint('Lo siento, sucedio un error al exportar el archivo, vuelve a intentarlo y si el error persiste por favor reportalo a: chris@chrisley.dev','white','on_red')
                
        
        # Copiar archivo de tu sistema a FiUnamFs
        elif param[0] == 'import':
            try:
                if len(param) > 1:
                    copy_import(param[1])
                else:
                    cprint('Error: Ingresa la ruta del archivo a copiar al sistema de archivos.\nEjemplo:\n\import [rutaArchivo]','white','on_red')
            except Exception:
                print(traceback.format_exc())
                cprint('Lo siento, sucedio un error al importar el archivo, vuelve a intentarlo y si el error persiste por favor reportalo a: chris@chrisley.dev','white','on_red')

        elif param[0] == 'superinfo':
            print('Nombre del sistema de archivos: {}'.format(SuperBloque['nombre']))
            print('Version del sistema de archivos: {}'.format(SuperBloque['version'] ))
            print('Etiqueta del volumen: {}'.format(SuperBloque['volumen']))
            print('Tamaño del cluster: {} bytes'.format(SuperBloque['tamanio']))
            print('Número de clusters que mide el directorio: {}'.format(SuperBloque['nClustersDir']))
            print('Número de clusters que mide la unidad completa: {}\n'.format(SuperBloque['nClustersCom']))
        
        # Eliminar archivo de FiUnamFs
        elif param[0] == 'rm':
            if len(param)>1:
                try:
                    rm(param[1])
                except:
                    cprint('Lo siento, sucedio un error al eliminar el archivo, vuelve a intentarlo y si el error persiste por favor reportalo a: chris@chrisley.dev','white','on_red')
            else:
                cprint('Error: Ingresa el nombre del archivo a eliminar.\nEjemplo:\n\rm [nombreArchivo]','white','on_red')

        
        elif param[0] == 'help':
            print(tabulate(helpComandos,headers='keys')+'\n')

        elif param[0] == 'exit':
            salir = True
        else:
            cprint('El comando \'' + param[0] + '\' no existe\nEscribe \'help\' para mostrar los comandos disponibles','white','on_red')

def main():
    try:
        # El programa trabajara con una copia de fiunamfs.img para asi los cambios no afecten al original y si se quiere regresar al punto anterior se pueda hacer de facil manera:

        # Primero se verifica que este exista, en caso contrario se crea la copia:
        verificaCopia()

        # Ahora se abre la copia y mapea la imagen de memoria
        with open(imgFilename,'a+b') as diskImg:# Se abre la imagen de disco con ACCESS_WRITE
            global DIMap
            DIMap = mmap.mmap(diskImg.fileno(),0,access=mmap.ACCESS_WRITE)
            obtenerInfoSuperBloque()
            # Se verifica que el sistema de archivos sea FiUnamFS para proceder.
            if SuperBloque['nombre'] == nSistemaArch:
                if SuperBloque['version'] == versionSistArch:
                    sistemaArchivos()
                else:
                    cprint('Error: La versión del sistema de archivos no es la 1.1','white','on_red')
            else:
                cprint('Error: El sistema de archivos no es: FiUnamFS','white','on_red')
    except:
        cprint('Error: El archivo no se puede abrir. Verifica que su nombre sea \'fiunamfs.img\' y que se encuentre en el directorio','white','on_red')
        return

    
main()