# Para instalar las bibliotecas necesarias utilizar los siguientes comandos:
# pip install tabulate
from tabulate import tabulate # ⚠️ Intalacion necesaria - Biblioteca para imprimir en consola de forma tabular.

def crearTrigger(uso,id):
    return f"<a class=\"trigger-modal\" href=\"#{id}\">{uso}</a>"

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
        elif line['uso'] == 'Anónimo':
            line['uso'] = crearTrigger('Anónimo','anonymous')
        elif line['uso'] == "Llamada al Sistema":
            line['uso'] = crearTrigger('Llamada al sistema','syscall')
        elif line['uso'] == 'Var -> Kernel':
            line['uso'] = crearTrigger('Var','var')
    return Pmap_HTML

def remplazarTokens(plantilla:str,PID,Pmap):
    tabla_html = tabulate(Pmap,headers="firstrow",tablefmt='unsafehtml')
    return plantilla.format(PID=PID,TABLA=tabla_html)

def crearHTML(PID,Pmap,filename):
    plantilla = getPlantilla()
    html = remplazarTokens(plantilla,PID,Pmap)
    with open(filename,'w') as file:
        file.write(html)