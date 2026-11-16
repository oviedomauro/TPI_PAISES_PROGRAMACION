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
console = Console()

estilo = Style([
    ("qmark", "fg:#00bcd4 bold"),
    ("question", "bold"),
    ("pointer", "fg:#ff9800 bold"),
    ("highlighted", "fg:#ff9800 bold"),
    ("answer", "fg:#4caf50 bold"),
])

def mostrar_mensaje_exito(mensaje):
    console.print(mensaje, style="bold green", markup=False, highlight=False)

def mostrar_mensaje_error(mensaje):
    console.print(mensaje, style="bold red", markup=False, highlight=False)

def mostrar_mensaje_aviso(mensaje):
    console.print(mensaje, style="yellow", markup=False, highlight=False)

def elegir_opcion_menu():
    console.print(Panel("Gestion de paises", style="bold cyan"))

    opcion = questionary.select(
        "Elegi una opcion:",
        choices=[
            Choice("Agregar pais", value="1", shortcut_key="1"),
            Choice("Actualizar pais", value="2", shortcut_key="2"),
            Choice("Buscar pais por nombre", value="3", shortcut_key="3"),
            Choice("Filtrar paises", value="4", shortcut_key="4"),
            Choice("Ordenar paises", value="5", shortcut_key="5"),
            Choice("Mostrar estadisticas", value="6", shortcut_key="6"),
            Choice("Mostrar todos los paises", value="7", shortcut_key="7"),
            Separator(),
            Choice("Salir", value="0", shortcut_key="0"),
        ],
        style=estilo,
        use_shortcuts=True,
        instruction="(flechas o numero, y Enter)",
    ).ask()

    if opcion is None:
        return "0"
    return opcion

def cargar_paises(ruta):
    paises = []
    try:
        with open(ruta, "r", encoding="utf-8-sig") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        mostrar_mensaje_error(f"Error: no se encontro el archivo {ruta}")
        return paises
    except UnicodeDecodeError:
        mostrar_mensaje_error(f"Error: el archivo {ruta} no esta guardado en formato UTF-8")
        return paises

    if len(lineas) == 0:
        mostrar_mensaje_error(f"Error: el archivo {ruta} esta vacio")
        return paises

    encabezado = lineas[0].strip().lower().replace(" ", "")
    if encabezado != "nombre,poblacion,superficie,continente":
        mostrar_mensaje_aviso("Aviso: la primera linea no es el encabezado esperado (nombre,poblacion,superficie,continente) y se ignora")

    for i in range(1, len(lineas)):
        linea = lineas[i].strip()
        if linea == "":
            continue

        partes = linea.split(",")
        if len(partes) != 4:
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: formato incorrecto")
            continue

        nombre = partes[0].strip()
        continente = partes[3].strip()
        if nombre == "" or continente == "":
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: hay campos vacios")
            continue
        try:
            poblacion = int(partes[1])
            superficie = int(partes[2])
        except ValueError:
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: poblacion o superficie no son numeros")
            continue

        if poblacion <= 0 or superficie <= 0:
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: poblacion y superficie deben ser mayores a cero")
            continue

        if buscar_porcision(paises, nombre) != -1:
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: el pais {nombre} esta repetido")
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
        mostrar_mensaje_aviso("No hay paises para mostrar")
        return
    tabla = Table(title="Paises", header_style="bold", caption=f"Total: {len(paises)} paises")

    tabla.add_column("Nombre", style="cyan")
    tabla.add_column("Poblacion", justify="right", style="green")
    tabla.add_column("Superficie (km2)", justify="right", style="yellow")
    tabla.add_column("Continente", style="magenta")
    
    for pais in paises:
        tabla.add_row(
            pais["nombre"],
            str(pais["poblacion"]),
            str(pais["superficie"]),
            pais["continente"]
        )
        
    console.print(tabla)

def validar_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        mostrar_mensaje_error("Error: No puede estar vacio el campo")
        texto = input(mensaje).strip()
    return texto

def validar_numero(mensaje):
    while True:
        dato = input(mensaje).strip()
        try:
            numero = int(dato)
        except ValueError:
            mostrar_mensaje_error("Error: Debe ingresar un numero entero")
            continue
        if numero < 0:
            mostrar_mensaje_error("Error: Debe ingresar un numero entero positivo")
            continue
        if numero <= 0:
            mostrar_mensaje_error("Error: Debe ingresar un numero entero mayor a cero")
            continue
        return numero
    
def agregar_pais(paises):
    print("")
    print("Agregar pais")
    nombre = validar_texto("ingrese el nombre del pais: ")
    if buscar_porcision(paises, nombre) != -1:
        mostrar_mensaje_error(f"Error: el pais {nombre} ya existe en la lista")
        return
    poblacion = validar_numero(f"Ingrese la poblacion de {nombre}: ")
    superficie = validar_numero(f"Ingrese la superficie de {nombre}: ")
    continente= validar_texto(f"Ingrese el continente donde se encuentra {nombre}: ")
    
    pais= {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(pais)
    mostrar_mensaje_exito(f"Se agrego el pais: {nombre} correctamente")

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
        mostrar_mensaje_error(f"Error; no se encontro el pais ingresado: {nombre}")
        return
    pais=paises[posicion]
    print(f"Datos actuales: {pais['nombre']} | {pais['poblacion']} | {pais['superficie']} | {pais['continente']}")
    nueva_poblacion=validar_numero(f"Ingrese la nueva poblacion de {nombre}: ")
    nueva_superficie=validar_numero(f"Ingrese la nueva superficie de {nombre}: ")
    
    pais["poblacion"] = nueva_poblacion
    pais["superficie"] = nueva_superficie
    mostrar_mensaje_exito(f"Los datos del pais {pais['nombre']} se actualizaron correctamente")

def buscar_pais_por_nombre(paises):
    print(f"Buscar pais por nombre")
    nombre= validar_texto("Ingrese nombre o parte del nombre del pais que desea buscar: ")
    resultados = []
    for pais in paises:
        if nombre.lower() in pais["nombre"].lower():
            resultados.append(pais)
    if len(resultados) ==0:
        mostrar_mensaje_aviso(f"No se ha encontrado ningun pais que contenga: {nombre}")
    else:
        mostrar_mensaje_exito(f"Se han encontrado {len(resultados)} paises que contienen: {nombre}")
        mostrar_paises(resultados)

def obtener_continentes(paises):
    continentes=[]
    for pais in paises:
        if pais["continente"] not in continentes:
            continentes.append(pais["continente"])
    return continentes

def elegir_opcion_filtro():
    console.print(Panel("Filtrar paises", style="bold cyan"))

    opcion = questionary.select(
        "Filtrar paises por:",
        choices=[
            Choice("Continente", value="1", shortcut_key="1"),
            Choice("Rango de poblacion", value="2", shortcut_key="2"),
            Choice("Rango de superficie", value="3", shortcut_key="3"),
            Separator(),
            Choice("Volver al menu principal", value="0", shortcut_key="0"),
        ],
        style=estilo,
        use_shortcuts=True,
        instruction="(flechas o numero, y Enter)",
    ).ask()

    if opcion is None:
        return "0"
    return opcion
    
def filtrar_continente(paises):
    print(f"Filtrar por continente")
    print("Continentes disponibles:")
    
    for continente in obtener_continentes(paises):
        print(f"- {continente}")
    continente = validar_texto("Ingrese el continente por el que desea filtrar: ")
    resultados= []
    
    for pais in paises:
        if pais["continente"].lower()== continente.lower():
            resultados.append(pais)
            
    if len(resultados)==0:
        mostrar_mensaje_aviso(f"No se han encontrado paises en el continente: {continente}")
    else:
        mostrar_mensaje_exito(f"Se han encontrado {len(resultados)} paises en el continente: {continente}")
        mostrar_paises(resultados)
        
def filtrar_rango_poblacion_superficie(paises, campo):
    print(f"Filtrar por {campo}")
    minimo = validar_numero(f"Ingrese el valor minimo de {campo}: ")
    maximo = validar_numero(f"Ingrese el valor maximo de {campo}: ")
    
    if minimo > maximo:
        mostrar_mensaje_error(f"Error: el minimo ({minimo}) no puede ser mayor que el maximo ({maximo})")
        return
    resultados = []
    
    for pais in paises:
        if pais[campo] >= minimo and pais[campo]<= maximo:
            resultados.append(pais)
            
    if len(resultados)==0:
        mostrar_mensaje_aviso(f"No se han encontrado paises con {campo} entre {minimo} y {maximo}")
    else:
        mostrar_mensaje_exito(f"Se han encontrado {len(resultados)} paises con {campo} entre {minimo} y {maximo}")
        mostrar_paises(resultados)

def filtrar_paises(paises):
    opcion= ""
    while opcion != "0":
        opcion = elegir_opcion_filtro()
        match opcion:
            case "1":
                filtrar_continente(paises)
            case "2":
                filtrar_rango_poblacion_superficie(paises, "poblacion")
            case "3":
                filtrar_rango_poblacion_superficie(paises, "superficie")
            case "0":
                mostrar_mensaje_exito("Volviendo al menu principal")
            case _:
                mostrar_mensaje_error("Opcion invalida, vuelva a intentarlo")

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
    opcion = questionary.select(
        "Elija el sentido de ordenamiento:",
        choices=[
            Choice("Ascendente (de menor a mayor o de la A a la Z)", value="1", shortcut_key="1"),
            Choice("Descendente (de mayor a menor o de la Z a la A)", value="2", shortcut_key="2"),
        ],
        style=estilo,
        use_shortcuts=True,
        instruction="(flechas o numero, y Enter)",
    ).ask()

    return opcion == "2"

def elegir_opcion_ordenamiento():
    console.print(Panel("Ordenar paises", style="bold cyan"))

    opcion = questionary.select(
        "Ordenar paises por:",
        choices=[
            Choice("Nombre", value="1", shortcut_key="1"),
            Choice("Poblacion", value="2", shortcut_key="2"),
            Choice("Superficie", value="3", shortcut_key="3"),
            Separator(),
            Choice("Volver al menu principal", value="0", shortcut_key="0"),
        ],
        style=estilo,
        use_shortcuts=True,
        instruction="(flechas o numero, y Enter)",
    ).ask()

    if opcion is None:
        return "0"
    return opcion

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
        opcion = elegir_opcion_ordenamiento()
        match opcion:
            case "1":
                mostrar_odernados(paises, "nombre")
            case "2":
                mostrar_odernados(paises, "poblacion")
            case "3":
                mostrar_odernados(paises, "superficie")
            case "0":
                mostrar_mensaje_exito("Volviendo al menu principal")
            case _:
                mostrar_mensaje_error("Opcion invalida, vuelva a intentarlo.")

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
        mostrar_mensaje_aviso("No hay paises cargados para mostrar estadisticas")
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
        opcion = elegir_opcion_menu()
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
                mostrar_mensaje_error("Opcion invalida , vuelva a intentarlo")
main()