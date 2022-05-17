archivo = open('fiunamfs.img')

archivo.seek(2048)

lectura = archivo.read(2048*4)

print(lectura)