def mostrar_menu():
    print("")
    print("Gestion de paises")
    print("1. Agregar pais")
    print("2. Actualizar pais")
    print("3. Buscar pais por nombre")
    print("4. Filtrar paises")
    print("5. Ordenar paises")
    print("6. Mostrar estadisticas")
    print("0. Salir")


def cargar_paises(ruta):
    paises = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print("Error: no se encontró el archivo", ruta)
        return paises

    for i in range(1, len(lineas)):
        linea = lineas[i].strip()
        if linea == "":
            continue

        partes = linea.split(",")
        if len(partes) != 4:
            print("Línea", i + 1, "ignorada: formato incorrecto")
            continue
        
        nombre = partes[0].strip()
        continente = partes[3].strip()
        if nombre == "" or continente == "":
            print("Línea", i + 1, "ignorada: hay campos vacíos")
            continue
        try:
            poblacion = int(partes[1])
            superficie = int(partes[2])
        except ValueError:
            print("Línea", i + 1, "ignorada: población o superficie no son números")
            continue
        pais = {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente
        }
        paises.append(pais)
    return paises

def main():
    paises = cargar_paises("paises.csv")
    print("Se cargaron", len(paises), "países")
    opcion = ""
    while opcion != "0":
        mostrar_menu()
        opcion = input("Elegi una opcion: ")
        match opcion:
            case "1":
                pass
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
            case "0":
                print("Saliendo del programa...")
                
            case _:
                print("Opcion invalida , vuelva a intentarlo")
main()