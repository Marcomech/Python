
def chose(rango):
    nro = -10
    while 0 > nro or rango < nro:
        try:
            nro = int(input("Elija un numero: "))
        except ValueError:
            print ("No fue un numero")
    return nro

nroValido = chose(int(input('Rango: ')))

print(nroValido)