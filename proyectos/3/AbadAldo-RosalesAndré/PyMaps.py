#!/usr/bin/python3
import re
import itertools
import argparse
from colorama import init, Back, Style, Fore
from dataclasses import dataclass

init()

''' Expresión regular para parsear cada línea de /proc/PID/maps'''
RE_MAPS = re.compile(r"""
    (?P<addr_inicio>[0-9a-f]+)-(?P<addr_fin>[0-9a-f]+)\s+ # Direcciones de inicio y final
    (?P<perms>\S+)\s+                                     # Permisos
    (?P<offset>[0-9a-f]+)\s+                              # Offset
    (?P<dev>\S+)\s+                                       # nodo de dispositivo
    (?P<inode>\d+)\s+                                     # inodo
    (?P<ruta>.*)\s+                                       # ruta
""", re.VERBOSE)


''' Conversión de bytes a múltiplos'''
def human_bytes(size):
    modifier = 1
    while size > 1024:
        modifier *= 1024
        size /= 1024
    return "%.1f%s" % (size, {
        1024**0: 'b',
        1024**1: 'k',
        1024**2: 'M',
        1024**3: 'G',
        1024**4: 'T',
    }.get(modifier, " x%d" % modifier))


'''Definición de Registro, estructura que permite organizar cada bloque'''
@dataclass
class Registro:
    uso: str
    inicio: int
    final: int
    perms: str
    ruta: str

    ''' El tamaño del bloque se obtiene de la diferencia entre las direcciones en memoria '''
    @property
    def size(self):
        return self.final - self.inicio
 
    ''' Se asume que cada bloque del kernel = 4096 bytes... Podría sacarse un valor definitivo leyendo /proc/PID/smaps '''
    @property
    def pags(self):
    	return self.size/4096
    	
    @property
    def human_readeable(self):
        return human_bytes(self.size)
 
    '''Parsing del archivo /proc/PID/maps, obteniendo cada bloque como un registro'''
    @classmethod
    def parse(self, pid):
        registros = []
        with open("/proc/%d/maps" % pid) as fd:
            for line in fd:
                m = RE_MAPS.match(line)
                if not m:
                    print("Saltando línea: %s" % line) # Por si hay alguna linea rara en el archivo 
                    continue
                inicio, final, perms, null, null, null, ruta = m.groups()
                inicio = int(inicio, 16)
                final = int(final, 16)
               	perms = perms[0:3]  # Tomando solo los permisos 'rwx' e ignorando 'p'
               	uso = ""
      
                '''Definimos uso del bloque según permisos y características de la ruta'''	
               	if ruta:
               	
               		if "lib" in ruta:
               			uso = "Bib -> "
               		elif '[' in ruta:
               			uso = ruta
               			
               		if uso != ruta:
               			if (perms == 'r--' or perms == 'rw-'):
               				uso = uso + "Datos"
               			elif perms == 'r-x':
               				uso= uso + "Texto"
               			elif perms == '---':
               				uso= uso + "Priv."
                else:
                    ruta = "--- Vacío ---"
                    uso = "Anónimo"
		       
		        		
                '''Se agrega nuevo registro al arreglo, una vez que se ha determinado su uso'''
                registros.append(Registro(
                    uso=uso,
                    inicio=inicio,
                    final=final,
                    perms=perms,
                    ruta=ruta,
                ))
        return registros

    '''Permite cambiar el atributo respecto al cual se ordenarán los registros, así como el sentido'''
    @classmethod
    def reordenar(self, registros, orden, reversa):
        rev = True if reversa == 1 else False
        if orden == 0:
            return list(sorted(itertools.chain(registros), key=lambda r: r.inicio, reverse=rev))
        elif orden == 1:
            return list(sorted(itertools.chain(registros), key=lambda r: r.size, reverse=rev))
    	
      

if __name__ == '__main__':

   '''Definición y recuperación de argumentos de consola'''
   parser = argparse.ArgumentParser()
   parser.add_argument("pid", type=int, help="Process identifier (pid)")
   parser.add_argument("ordenamiento", type=int, help="0 - Por dirección de memoria | 1 - Por tamaño")
   parser.add_argument("sentido", type=int, help="0 - Acomodo de menor a mayor | 1 - Acomodo de mayor a menor")
   args = parser.parse_args()
	
   '''Llamadas para obtener los registros'''
   records = Registro.parse(args.pid)
   records = Registro.reordenar(records, args.ordenamiento, args.sentido)
 
 
   '''Impresión de resultados'''
   print( "\n" + Back.WHITE + Style.BRIGHT + Fore.BLACK + "#### Reporte de memoria para el proceso PID = %d | Total de memoria utilizada: %s ####" %(args.pid ,human_bytes(sum(r.size for r in records))), end="")
   print(Back.RESET + Fore.RESET + Style.RESET_ALL, end="")
   print("\n")
   print("\t".join([
    	"% 8s" % "||   Uso   |",
        "% 8s" % "|  De pág  |",
        "% 8s" % "|  A pág  |",
        "% 6s" % "| Tamaño |",
        "% 2s" % "| Páginas |",
        "% 2s" % "| Permisos |",
        "% 4s" % "| Uso o Mapeo ||",
    ]))
    
    
   '''Cambio de color según tipo de bloque, así como impresión de características'''
   for record in records:
    	
       print(Fore.RESET)
       if "Bib" in record.uso:
           print(Fore.MAGENTA, end="")
       elif "stack" in record.ruta:
    	   print(Fore.GREEN, end="")
       elif "heap" in record.ruta:
    	   print(Fore.YELLOW, end="")
       elif "Datos" in record.uso:
    	   print(Fore.BLUE, end="")
       elif "Vacío" in record.ruta:
    	   print(Fore.RED, end="")
       elif "Texto" in record.uso:
           print(Fore.CYAN, end="")
    	
 
       print("\t".join([
	    "% 8s" % record.uso.strip("[]").capitalize(),
            "%08x" % record.inicio,
            "%08x" % record.final,
            "% 8s" % record.human_readeable,
            "% 4i págs" % record.pags,
            "% 8s" % record.perms,
            "% 8s " % record.ruta
        ]) + Back.RESET,end="")
        
        

    