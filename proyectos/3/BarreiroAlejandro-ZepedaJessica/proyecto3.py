from sys import argv

#Función que determina la sección de memoria dependiendo sus permisos o dirección
def obtener_uso(permiso, map):
    #Cuando no se cuenta con mapeo o permisos
    if map == '- Vacío -' or permiso == '---':
        return ''

    #Para datos, texto y bibliotecas
    if '/' in map:
        if 'lib' in map:
            resultado = '\u001b[35mBib ->\u001b[0m' #Magenta
            if 'x' in permiso:
                return resultado + '\u001b[32mTexto\u001b[0m'   #Green
            elif 'r' in permiso:
                return resultado + '\u001b[32mDatos\u001b[0m'   #Green
        else:
            if 'x' in permiso:
                return '\u001b[32mTexto\u001b[0m      '
            elif 'r' in permiso:
                return '\u001b[32mDatos\u001b[0m      '

    #Para el Heap, Stack y Llamadas al sistema
    if map == '[heap]':
        return '\u001b[34mHeap\u001b[0m       ' #Blue
    if map == '[stack]':
        return '\u001b[31mStack\u001b[0m      ' #Red 
    if map == '[vvar]' or map == '[vdso]' or map == '[vsyscall]':
        return '\u001b[36mLlam. Sist.\u001b[0m' #Cyan

    return '?????'

#Función que obtiene el tamaño de la sección de memoria basado en las páginas que ocupa
def obtener_tamanio(num_paginas):
    tamanio = 4*num_paginas
    i = 0
    unidades = ('KB', 'MB', 'GB', 'TB', 'PB') #Tupla con unidades
    if tamanio < 1024:
        return str(tamanio) + unidades[i]
    else: 
        while tamanio >= 1024:
            tamanio = round(tamanio/1024,2)
            i += 1
        return str(tamanio) + unidades[i]


#Función que calcula el las líneas a colorear en la gráfica para cada sección
def calcula_grafica(uso, num_paginas):
    if uso == '\u001b[32mTexto\u001b[0m      ' or uso == '\u001b[32mDatos\u001b[0m      ':
        grafica_suma[0] += num_paginas
    elif uso == '\u001b[34mHeap\u001b[0m       ':
        grafica_suma[1] += num_paginas
    elif uso == '\u001b[35mBib ->\u001b[0m\u001b[32mTexto\u001b[0m' or uso == '\u001b[35mBib ->\u001b[0m\u001b[32mDatos\u001b[0m':
        grafica_suma[2] += num_paginas
    elif uso == '\u001b[31mStack\u001b[0m      ':
        grafica_suma[3] += num_paginas
    elif uso == '\u001b[36mLlam. Sist.\u001b[0m':
        grafica_suma[4] += num_paginas  


#Función que forma la cadena que representa la gráfica
def genera_grafica():
    suma = sum(grafica_suma)
    grafica = '['

    for i in range(int((grafica_suma[0]*100)/suma)):
        grafica = grafica + '\u001b[32m|\u001b[0m'
    for i in range(int((grafica_suma[1]*100)/suma)):
        grafica = grafica + '\u001b[34m|\u001b[0m'
    for i in range(int((grafica_suma[2]*100)/suma)):
        grafica = grafica + '\u001b[35m|\u001b[0m'
    for i in range(int((grafica_suma[3]*100)/suma)):
        grafica = grafica + '\u001b[31m|\u001b[0m'
    for i in range(int((grafica_suma[4]*100)/suma)):
        grafica = grafica + '|'

    return grafica + ']'

#Se inicia el proceso de lectura e impresión
pid = argv[1]
print("\033[1mProceso:\033[0m    " + pid)
print()

#Se abre el archivo
archivoMaps = open('/proc/'+pid+'/maps', 'r')

#Impresión del encabezado
print('\033[1m|{:<11}|{:16}|{:16}|{:<9}|{:<12}|{:<8}|{:50}'.format(
    'Uso', 'De página', 'A página', 'Tamaño', 'Núm. páginas', 'Permisos', 'Uso o Mapeo\033[0m'))

grafica = 0
lectura = archivoMaps.readlines()
grafica_suma = [0, 0, 0, 0 ,0, 0]

#Imprsión de la tabla
for linea in lectura:
    #Lectura de elementos
    elementos = linea.split()

    #Lectura de páginas
    paginas = elementos[0].split('-')
    pagina_inicial = paginas[0]
    pagina_final = paginas[1]

    #Lectura de permisos
    permisos = elementos[1]
    permisos = '  ' + permisos[0:3]
    
    #Lectura de mapeo
    if len(elementos) > 5: mapeo = elementos[5]
    else: mapeo = '- Vacío -'
    
    #Cálculo número de páginas
    num_paginas = int(pagina_final,16) - int(pagina_inicial,16)
    
    #Cálculo del tamaño
    tamanio = ' ' + obtener_tamanio(num_paginas)
    
    #Se determina el uso
    uso = obtener_uso(permisos,mapeo)
    
    #Se genera la gráfica
    calcula_grafica(uso, num_paginas)
    
    #Impresión de la fila
    print('|{:<11}|{:16}-{:16}|{:<9}|{:<12}|{:<8}|{:50}'.format(
        uso, pagina_inicial, pagina_final, tamanio, num_paginas, permisos, mapeo))

#Impresión de la gráfica
print()
print('\033[1mRepresentación del uso de memoria del proceso\033[0m')
print(genera_grafica())

archivoMaps.close()