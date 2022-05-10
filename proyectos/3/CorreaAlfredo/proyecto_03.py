import subprocess

proceso = input("Escribe el PID: ")

proc = subprocess.getoutput("pmap $$" + proceso)
dash = subprocess.getoutput("pmap $$ | grep \"dash\"")
bash = subprocess.getoutput("pmap $$ | grep \"bash\"")
pila = subprocess.getoutput("pmap $$ | grep \"pila\"")
anon = subprocess.getoutput("pmap $$ | grep \"anon\"")
lib = subprocess.getoutput("pmap $$ | grep \"lib\"")
ld = subprocess.getoutput("pmap $$ | grep \"id\"")

print("-------------------------------------------")
print("\tpmap\n")
print("-------------------------------------------")
print("\nproc")
print(proc)
print("-------------------------------------------")
print("\ndash")
print(dash)
print("-------------------------------------------")
print("\nbash")
print(bash)
print("-------------------------------------------")
print("\npila")
print(pila)
print("-------------------------------------------")
print("\nanon")
print(anon)
print("-------------------------------------------")
print("\nlib")
print(lib)
print("-------------------------------------------")
print("\nid")
print(ld)
print("-------------------------------------------")













