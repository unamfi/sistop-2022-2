from sys import argv;

#Poner columnas
#Obtener tamaño con unidades 
#Intentar gráfica

pid = argv[1]

def obtener_uso(permiso, map):
    if map == '- Vacío -' or permiso == '---':
        return ''

    if '/' in map:
        if 'lib' in map:
            resultado = '\u001b[35mBib ->\u001b[0m' #Magenta
        else:
            resultado = ''
        if 'x' in permiso:
            return resultado + '\u001b[32mTexto\u001b[0m'
        elif 'r' in permiso:
            return resultado + '\u001b[32mDatos\u001b[0m'


    if map == '[heap]':
        return '\u001b[34mHeap\u001b[0m' #Blue
    if map == '[stack]':
        return '\u001b[31mStack\u001b[0m' #Red
    if map is '[vvar]':
        return 'vvar'           #cambiar después
    if map is '[vdso]':
        return 'Library'           #cambiar después
    if map is '[vsyscall]':
        return 'Llamada al sistema'  #cambiar después

    
    return '?????'


print("Proceso " + pid)

archivoMaps = open('/proc/'+pid+'/maps', 'r')

print('|  Uso      |De pág.          |A pág.          | Tamaño  |Núm. páginas|Perm| Uso o mapeo')
lectura = archivoMaps.readlines()
for linea in lectura:
    elementos = linea.split()
    paginas = elementos[0].split('-')
    
    pagina_inicial = paginas[0]
    pagina_final = paginas[1]

    permisos = elementos[1]
    permisos = permisos[0:3]
    
    if len(elementos) > 5: mapeo = elementos[5]
    else: mapeo = '- Vacío -'
    
    num_paginas = int(pagina_final,16) - int(pagina_inicial,16)
    
    #tamanio = 
    
    uso = obtener_uso(permisos,mapeo)


    print(f'|{uso:>11}|({pagina_inicial:16}-{pagina_final:16}){num_paginas:7d}|{permisos:4}|{mapeo:50}')

