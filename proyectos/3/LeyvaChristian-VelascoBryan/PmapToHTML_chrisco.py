# Para instalar las bibliotecas necesarias utilizar los siguientes comandos:
# pip install tabulate
# pip install w3lib
from tabulate import tabulate # ⚠️ Intalacion necesaria - Biblioteca para imprimir en consola de forma tabular.
from w3lib.html import replace_entities # ⚠️ Intalacion necesaria - Biblioteca para decodificar entidades HTML.

def crearTrigger(uso,id):
    return f"<a href=\"#{id}\">{uso}</a>"

def getPlantilla():
    with open('assets/plantillas/plantilla_proyecto3.html','r') as file:
        plantilla = file.read()
    return plantilla

def createPmapHTML(Pmap:list):
    Pmap_HTML = Pmap.copy()
    for line in Pmap_HTML:
        if line['uso'] == "Stack":
            line['uso'] = crearTrigger('Stack','stack')
        elif line['uso'] ==  "Heap":
            line['uso'] = crearTrigger('Heap','heap')
        elif line['uso'] == 'Anonimo':
            pass
        elif line['uso'] == "Llamada al Sistema":
            pass
        elif line['uso'] == 'Var Kernel':
            pass
        elif line['uso'] == "vacio":
            pass
        elif line['uso'] == "Bib→Texto":
            pass
        elif line['uso'] == "Bib→Datos":
            pass
        elif line['uso'] == "Texto":
            pass
        elif line['uso'] == "Datos":
            pass
    return Pmap_HTML

def remplazarTokens(plantilla:str,PID,Pmap):
    tabla_html = tabulate(Pmap,headers="firstrow",tablefmt='html')
    return replace_entities(plantilla.format(PID=PID,TABLA=tabla_html))

def crearHTML(PID,Pmap,filename):
    plantilla = getPlantilla()
    html = remplazarTokens(plantilla,PID,Pmap)
    with open(filename,'w') as file:
        file.write(html)