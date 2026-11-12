def mostrar_menu():
    print("")
    print("Gestion de paises")
    print("1. Agregar pais")
    print("2. Actualizar pais")
    print("3. Buscar pais por nombre")
    print("4. Filtrar paises")
    print("5. Ordenar paises")
    print("6. Mostrar estadisticas")
    print("7. Mostrar todos los paises")
    print("0. Salir")


def cargar_paises(ruta):
    paises = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo {ruta}")
        return paises

    for i in range(1, len(lineas)):
        linea = lineas[i].strip()
        if linea == "":
            continue

        partes = linea.split(",")
        if len(partes) != 4:
            print(f"Linea {i + 1} ignorada: formato incorrecto")
            continue
        
        nombre = partes[0].strip()
        continente = partes[3].strip()
        if nombre == "" or continente == "":
            print(f"Línea {i + 1} ignorada: hay campos vacíos")
            continue
        try:
            poblacion = int(partes[1])
            superficie = int(partes[2])
        except ValueError:
            print(f"Línea {i + 1} ignorada: población o superficie no son números")
            continue
        pais = {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente
        }
        paises.append(pais)
    return paises

def mostrar_paises(paises):
    if len(paises) == 0:
        print("No hay paises para mostrar")
        return
    print("Nombre | Poblacion | Superficie | Continente")
    for pais in paises:
        print(f"{pais['nombre']} | {pais['poblacion']} | {pais['superficie']} | {pais['continente']}")

def validar_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        print("Error: No puede estar vacio el campo")
        texto = input(mensaje).strip()
    return texto

def validar_numero(mensaje):
    while True:
        dato = input(mensaje).strip()
        try:
            numero = int(dato)
        except ValueError:
            print("Error: Debe ingresar un numero entero")
            continue
        if numero < 0:
            print("Error: Debe ingresar un numero entero positivo")
            continue
        if numero <= 0:
            print("Error: Debe ingresar un numero entero mayor a cero")
            continue
        return numero
    
def agregar_pais(paises):
    print("")
    print("Agregar pais")
    nombre = validar_texto("ingrese el nombre del pais: ")
    poblacion = validar_numero(f"Ingrese la poblacion de {nombre}: ")
    superficie = validar_numero(f"Ingrese la superficie de {nombre}: ")
    continente= validar_texto(f"Ingrese el continente donde se encuentra {nombre}")
    
    pais= {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(pais)
    print(f"Se agrego el pais: {nombre} correctamente")
    
def main():
    paises = cargar_paises("paises.csv")
    print(f"Se cargaron {len(paises)} países")
    opcion = ""
    while opcion != "0":
        mostrar_menu()
        opcion = input("Elegi una opcion: ")
        match opcion:
            case "1":
                agregar_pais(paises)
            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "5":
                pass
            case "6":
                pass
            case "7":
                mostrar_paises(paises)
            case "0":
                print("Saliendo del programa...")
                break
            case _:
                print("Opcion invalida , vuelva a intentarlo")
main()