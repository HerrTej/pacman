actions = {"North": 0, "East": 1, "South": 2, "West": 3, "exit": 4, "Stop": 5}
lista = [(0,1),(2,3),(4,5),(6,7)]
print(lista[0][1])
hola = True
adios = False
if adios or hola:
    print(8)
for item in range(1,10,1):
    print(item)

hola = [False,None,False]

if True not in hola:
    print("hola")
