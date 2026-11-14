try:
    import questionary
    from questionary import Choice, Separator, Style
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
except ImportError:
    print("Faltan librerias para ejecutar el programa.")
    print("Instalalas con este comando y volve a ejecutar:")
    print("python -m pip install -r requirements.txt")
    exit()
    
    
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

def buscar_porcision(paises, nombre):
    for i in range(len(paises)):
        if paises[i]["nombre"].lower() == nombre.lower():
            return i
    return -1

def actualizar_pais(paises):
    print("Actualizar pais")
    nombre=validar_texto("Ingrese el nombre del pais que desea actualizar: ")
    posicion =buscar_porcision(paises, nombre)
    if posicion ==-1:
        print(f"Error; no se encontro el pais ingresado: {nombre}")
        return
    pais=paises[posicion]
    print(f"Datos actuales: {pais['nombre']} | {pais['poblacion']} | {pais['superficie']} | {pais['continente']}")
    nueva_poblacion=validar_numero(f"Ingrese la nueva poblacion de {nombre}: ")
    nueva_superficie=validar_numero(f"Ingrese la nueva superficie de {nombre}: ")
    
    pais["poblacion"] = nueva_poblacion
    pais["superficie"] = nueva_superficie
    print(f"Los datos del pais {pais['nombre']} se actualizaron correctamente")

def buscar_pais_por_nombre(paises):
    print(f"Buscar pais por nombre")
    nombre= validar_texto("Ingrese nombre o parte del nombre del pais que desea buscar: ")
    resultados = []
    for pais in paises:
        if nombre.lower() in pais["nombre"].lower():
            resultados.append(pais)
    if len(resultados) ==0:
        print(f"No se ha encontrado ningun pais que contenga: {nombre}")
    else:
        print(f"Se han encontrado {len(resultados)} paises que contienen: {nombre}")
        mostrar_paises(resultados)
def obtener_continentes(paises):
    continentes=[]
    for pais in paises:
        if pais["continente"] not in continentes:
            continentes.append(pais["continente"])
    return continentes

def mostrar_menu_de_filtro():
    print("Filtrar paises")
    print("1. Filtrar por continente")
    print("2. Filtrar por poblacion")
    print("3. Filtrar por superficie")
    print("0. Volver al menu principal")
    
def filtrar_continente(paises):
    print("Filtrar por continente")
    print("Continentes disponibles:")
    
    for continente in obtener_continentes(paises):
        print(f"- {continente}")
    continente = validar_texto("Ingrese el continente por el que desea filtrar: ")
    resultados= []
    
    for pais in paises:
        if pais["continente"].lower()== continente.lower():
            resultados.append(pais)
            
    if len(resultados)==0:
        print(f"No se han encontrado paises en el continente: {continente}")
    else:
        print(f"Se han encontrado {len(resultados)} paises en el continente: {continente}")
        mostrar_paises(resultados)
        
def filtrar_rango_poblacion_superficie(paises, campo):
    print(f"Filtrar por {campo}")
    min = validar_numero(f"Ingrese el valor minimo de {campo}: ")
    max = validar_numero(f"Ingrese el valor maximo de {campo}: ")
    
    if min > max:
        print(f"Error: el minimo ({min}) no puede ser mayor que el maximo ({max})")
        return
    resultados = []
    
    for pais in paises:
        if pais[campo] >= min and pais[campo]<= max:
            resultados.append(pais)
            
    if len(resultados)==0:
        print(f"No se han encontrado paises con {campo} entre {min} y {max}")
    else:
        print(f"Se han encontrado {len(resultados)} paises con {campo} entre {min} y {max}")
        mostrar_paises(resultados)

def filtrar_paises(paises):
    opcion= ""
    while opcion != "0":
        mostrar_menu_de_filtro()
        opcion= input("Elija una opcion: ")
        match opcion:
            case "1":
                filtrar_continente(paises)
            case "2":
                filtrar_rango_poblacion_superficie(paises, "poblacion")
            case "3":
                filtrar_rango_poblacion_superficie(paises, "superficie")
            case "0":
                print("Volviendo al menu principal")
            case _:
                print("Opcion invalida, vuelva a intentarlo")

def ordernar_lista(paises, campo, decendente):
    lista= []
    for pais in paises:
        lista.append(pais)
    n=len(lista)
    
    for i in range(n - 1):
        for j in range(n - i - 1):
            actual = lista[j][campo]
            siguiente = lista[j+1][campo]
            
            if campo=="nombre":
                actual = actual.lower()
                siguiente = siguiente.lower()
            
            if decendente:
                intercambiar = actual < siguiente
            else:
                intercambiar = actual > siguiente
                
            if intercambiar:
                aux = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = aux
    return lista

def elegir_sentido_ordenamiento():
    while True:
        print("Elija el sentido de ordenamiento:")
        print("1. Ascendente")
        print("2. Descendente")
        opcion = input("Ingrese una opcion: ")
        match opcion:
            case "1":
                return False
            case "2":
                return True
            case _:
                print("Opcion invalida, vuelva a intentarlo.")

def mostrar_menu_de_ordenamiento():
    print("Ordenar paises por: ")
    print("1. Nombre")
    print("2. Poblacion")
    print("3. Superficie")
    print("0. Volver al menu principal")

def mostrar_odernados(paises, campo):
    decendente = elegir_sentido_ordenamiento()
    lista_ordenada = ordernar_lista(paises, campo, decendente)
    
    if decendente:
        sentido = "descendente"
    else:
        sentido= "ascendente"
    print(f"Paises ordenados por {campo} ({sentido})")
    mostrar_paises(lista_ordenada)

def ordenar_paises(paises):
    opcion = ""
    while opcion != "0":
        mostrar_menu_de_ordenamiento()
        opcion = input("Ingrese una opcion: ")
        match opcion:
            case "1":
                mostrar_odernados(paises, "nombre")
            case "2":
                mostrar_odernados(paises, "poblacion")
            case "3":
                mostrar_odernados(paises, "superficie")
            case "0":
                print("Volviendo al menu principal")
            case _:
                print("Opcion invalida, vuelva a intentarlo.")

def pais_mas_poblado(paises):
    mayor_poblacion = paises[0]
    for pais in paises:
        if pais["poblacion"] > mayor_poblacion["poblacion"]:
            mayor_poblacion = pais
    return mayor_poblacion

def pais_menos_poblado(paises):
    menor_poblacion = paises[0]
    for pais in paises:
        if pais["poblacion"] < menor_poblacion["poblacion"]:
            menor_poblacion = pais
    return menor_poblacion

def pais_mas_poblado(paises):
    mayor_poblacion= paises[0]
    for pais in paises:
        if pais["poblacion"] > mayor_poblacion["poblacion"]:
            mayor_poblacion = pais
    return mayor_poblacion

def pais_menos_poblado(paises):
    menor_poblacion =paises[0]
    for pais in paises:
        if pais["poblacion"] < menor_poblacion["poblacion"]:
            menor_poblacion = pais
    return menor_poblacion

def calcular_promedio(paises, campo):
    total = 0
    for pais in paises:
        total = total + pais[campo]
    return total / len(paises)

def contar_paises_por_continente(paises):
    conteo={}
    for pais in paises:
        continente =pais["continente"]
        if continente in conteo:
            conteo[continente]= conteo[continente] + 1
        else:
            conteo[continente] = 1
    return conteo

def mostrar_estadisticas(paises):
    print("Estadisticas de paises")
    if len(paises)==0:
        print("No hay paises cargados para mostrar estadisticas")
        return
    
    mayor_poblado = pais_mas_poblado(paises)
    menor_poblado = pais_menos_poblado(paises)
    promedio_poblacion = calcular_promedio(paises, "poblacion")
    promedio_superficie = calcular_promedio(paises, "superficie")
    conteo_por_continente = contar_paises_por_continente(paises)
    
    print(f"Pais mas poblado: {mayor_poblado['nombre']} con {mayor_poblado['poblacion']} habitantes")
    print(f"Pais menos poblado: {menor_poblado['nombre']} con {menor_poblado['poblacion']} habitantes")
    print(f"Promedio de poblacion: {round(promedio_poblacion, 2)}")
    print(f"Promedio de superficie: {round(promedio_superficie, 2)} km2")
    print("Cantidad de paises por continente:")
    for continente in conteo_por_continente:
        print(f"- {continente}: {conteo_por_continente[continente]} paises")

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
                actualizar_pais(paises)
            case "3":
                buscar_pais_por_nombre(paises)
            case "4":
                filtrar_paises(paises)
            case "5":
                ordenar_paises(paises)
            case "6":
                mostrar_estadisticas(paises)
            case "7":
                mostrar_paises(paises)
            case "0":
                print("Saliendo del programa...")
                break
            case _:
                print("Opcion invalida , vuelva a intentarlo")
main()