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

def main():
    opcion = ""
    while opcion != "0":
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
                break
            case _:
                print("Opcion invalida , vuelva a intentarlo")
