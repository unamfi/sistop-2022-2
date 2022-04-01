import threading

# Señales para refrescar la pantalla
senalHilos = threading.Semaphore(0)
senalActu = threading.Semaphore(0)

# Torniquete para los colegas
detener = threading.Semaphore(0)

# Visualizacion de la sala de trabajo
escena = [""]*10
escena[0] = "                             "
escena[1] = "°---------------------------°"
escena[2] = "|                           |"
escena[3] = "|                           |"
escena[4] = "|                           |"
escena[5] = "|                           |"
escena[6] = "|                           |"
escena[7] = "°------------   ------------°"
escena[8] = "                             "
escena[9] = "                             "

