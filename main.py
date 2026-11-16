# Alumno: Mauro Oviedo
# TPI programacion 1

# Este programa permite leer paises desde un archivo csv y los guarda en una lista de diccionarios que son de la siguiente manera (un diccionario por pais, con las claves
#   nombre, poblacion, superficie y continente), desde el menu permite acceder a distitas opciones, agregar, actualizar, buscar, filtrar, odernar y ver en estadistica

#IMPORTANTE !!!
# Requisitos: tener instalado las librerias(questionary y rich) que estan en requirements.txt


# questionary: menus con flechas. rich: colores y tablas en consola.
# Si falta alguna, se captura el error y se explica como instalarla,
# en lugar de que el programa se corte con un error largo.
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

# Objeto de rich que usamos para imprimir con colores y tablas
console = Console()
# Colores que se usan en los menus de questionary.
estilo = Style([
    ("qmark", "fg:#00bcd4 bold"),
    ("question", "bold"),
    ("pointer", "fg:#ff9800 bold"),
    ("highlighted", "fg:#ff9800 bold"),
    ("answer", "fg:#4caf50 bold"),
])
# Estos son los mensajes de colores
# Sirven para cumplir "mensajes claros de exito, error y aviso":
# verde = exito, rojo = error, amarillo = aviso.
# markup=False hace que los corchetes del texto no se interpreten
# como formato de rich.

# Imprime un mensaje de exito en verde
def mostrar_mensaje_exito(mensaje):
    console.print(mensaje, style="bold green", markup=False, highlight=False)
# Imprime un mensaje de error en rojo
def mostrar_mensaje_error(mensaje):
    console.print(mensaje, style="bold red", markup=False, highlight=False)
# Imprime un mensaje de aviso en amarillo (algo no fue tan grave)
def mostrar_mensaje_aviso(mensaje):
    console.print(mensaje, style="yellow", markup=False, highlight=False)
# MENU PRINCIPAL:

#Muestra el menu principal y devuelve la opcion elegida ya sea usando los numeros o las flechitas y enter para confirmar.
def elegir_opcion_menu():
        # Titulo del menu dentro de un recuadro
    console.print(Panel("Gestion de paises", style="bold cyan"))
    
    # Cada Choice tiene el texto que se ve y el value que devuelve la funcion
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
    # Si el usuario cancela con Ctrl + C questionary va a devolver None, lo tomamos como "Salir" para que el programa no se rompa
    if opcion is None:
        return "0"
    return opcion
# ARCHIVO CSV: lee y guarda

# Lee el archivo CSV y devuelve una LISTA (un diccionario por pais).
# Es la funcion que cumple "controlar errores de formato en el CSV".
def cargar_paises(ruta):
    # Lista vacia donde se van guardando los paises validos
    paises = []
    # PASO 1: abrir el archivo controlando los errores posibles.
    # utf-8-sig se encarga de leer UTF-8 e ignora la marca invisible que el Excel agrega.
    try:
        with open(ruta, "r", encoding="utf-8-sig") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        mostrar_mensaje_error(f"Error: no se encontro el archivo {ruta}")
        return paises
    except UnicodeDecodeError:
        mostrar_mensaje_error(f"Error: el archivo {ruta} no esta guardado en formato UTF-8")
        return paises
    
    # PASO 2: si el archivo no tiene ninguna linea, avisamos y devolvemos la lista vacia
    if len(lineas) == 0:
        mostrar_mensaje_error(f"Error: el archivo {ruta} esta vacio")
        return paises
    # PASO 3: controlar la primera linea, que debe ser el encabezado.

    encabezado = lineas[0].strip().lower().replace(" ", "")
    if encabezado != "nombre,poblacion,superficie,continente":
        mostrar_mensaje_aviso("Aviso: la primera linea no es el encabezado esperado (nombre,poblacion,superficie,continente) y se ignora")
    # PASO 4: recorrer las lineas de datos y se empieza en 1 para saltear el encabezado.
    for i in range(1, len(lineas)):
        linea = lineas[i].strip()

        # Las lineas en blanco se saltean sin avisar
        if linea == "":
            continue

        # Control de formato: cada linea debe tener exactamente 4 campos separados por coma
        partes = linea.split(",")
        if len(partes) != 4:
            # i + 1 es el numero de linea real del archivo (empieza a contar en 1)
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: formato incorrecto")
            continue

        # Control de campos vacios en los dos campos de texto
        nombre = partes[0].strip()
        continente = partes[3].strip()
        if nombre == "" or continente == "":
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: hay campos vacios")
            continue
        
        # Poblacion y superficie deben poder convertirse a numero entero y int() lanza ValueError si el texto no es un numero.
        try:
            poblacion = int(partes[1])
            superficie = int(partes[2])
        except ValueError:
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: poblacion o superficie no son numeros")
            continue

        # Ademas deben ser mayores a cero porque como va haber poblacion en negativo.
        if poblacion <= 0 or superficie <= 0:
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: poblacion y superficie deben ser mayores a cero")
            continue

        # No se permiten paises repetidos, busca el nombre en la lista que ya se armo
        if buscar_porcision(paises, nombre) != -1:
            mostrar_mensaje_aviso(f"Linea {i + 1} ignorada: el pais {nombre} esta repetido")
            continue
        
        # Si la linea paso todos los controles, se crea el diccionario del pais y se agrega a la lista
        pais = {
            "nombre": nombre,
            "poblacion": poblacion,
            "superficie": superficie,
            "continente": continente
        }
        
        # Se devuelve la lista de diccionarios con todos los paises validos
        paises.append(pais)
    return paises

# Reescribe el CSV completo con el encabezado y todos los paises de la lista, se usa despues de agregar o actualizar, asi los cambios no se pierden al cerrar.
# Devuelve True si pudo guardar y False si hubo un error.
def guardar_paises(paises, ruta):
    try:
        # Modo "w" se encarga de reemplaza el contenido anterior del archivo
        with open(ruta, "w", encoding="utf-8") as archivo:
                # Primero el encabezado igual al que espera cargar_paises
            archivo.write("nombre,poblacion,superficie,continente\n")
                # Luego una linea por cada pais con los valores separados por coma
            for pais in paises:
                archivo.write(f"{pais['nombre']},{pais['poblacion']},{pais['superficie']},{pais['continente']}\n")
        return True
    
    # Maneja errores del sistema al guardar, notifica el fallo y retorna False
    except OSError as e:
        mostrar_mensaje_error(f"Error al guardar el archivo {ruta}: {e}")
        return False

# MOSTRAR PAISES:
# La usan todas las opciones que listan paises (buscar, filtrar, ordenar, mostrar todos), se muestra todo en la tabla con colores.

def mostrar_paises(paises):
    # Si la lista esta vacia, se avisa y no se arma la tabla
    if len(paises) == 0:
        mostrar_mensaje_aviso("No hay paises para mostrar")
        return
    
    # Se crea la tabla con titulo y, al pie, la cantidad de paises
    tabla = Table(title="Paises", header_style="bold", caption=f"Total: {len(paises)} paises")
    tabla.add_column("Nombre", style="cyan")
    tabla.add_column("Poblacion", justify="right", style="green")
    tabla.add_column("Superficie (km2)", justify="right", style="yellow")
    tabla.add_column("Continente", style="magenta")
    
    # Una fila por cada pais. Los numeros se pasan a texto con str() porque la tabla solo acepta texto.
    for pais in paises:
        tabla.add_row(
            pais["nombre"],
            str(pais["poblacion"]),
            str(pais["superficie"]),
            pais["continente"]
        )

    # Se imprime la tabla terminada
    console.print(tabla)

# VALIDACIONES DE ENTRADA:
# Pedimos los datos al usuario y los volvemos a pedir hasta que sean correctos, asi el programa nunca falla por un dato mal ingresado.

# Pide un texto y lo vuelve a pedir mientras este vacio ("No se permiten campos vacios")
def validar_texto(mensaje):
    texto = input(mensaje).strip()
    while texto == "":
        mostrar_mensaje_error("Error: No puede estar vacio el campo")
        texto = input(mensaje).strip()
    return texto

# Pide un numero entero positivo y repite hasta que el dato sea valido. Devuelve el numero ya convertido a int.
def validar_numero(mensaje):
    while True:
        dato = input(mensaje).strip()

        # Que sea un numero entero (si no int() va a lanza ValueError)
        try:
            numero = int(dato)
        except ValueError:
            mostrar_mensaje_error("Error: Debe ingresar un numero entero")
            continue
        #Que no sea negativo
        if numero < 0:
            mostrar_mensaje_error("Error: Debe ingresar un numero entero positivo")
            continue
        # Que no sea cero
        if numero <= 0:
            mostrar_mensaje_error("Error: Debe ingresar un numero entero mayor a cero")
            continue
        
        # Si paso los tres controles, se devuelve y termina el while
        return numero
    
# Pide un texto no vacio y sin comas.
def texto_sin_coma(mensaje):
    texto = validar_texto(mensaje)
    while "," in texto:
        mostrar_mensaje_error("Error: No puede contener comas")
        texto = validar_texto(mensaje)
    return texto

# OPCION 1: agregar pais
# Pide los datos de un pais nuevo lo agrega a la lista y guarda el CSV y si el pais ya existe, muestra un error y no lo agrega.
def agregar_pais(paises):
    print("")
    print("Agregar pais")
    # Se pide el nombre y se controla que no este repetido antes de pedir el resto
    nombre = texto_sin_coma("ingrese el nombre del pais: ")
    
    if buscar_porcision(paises, nombre) != -1:
        mostrar_mensaje_error(f"Error: el pais {nombre} ya existe en la lista")
        return

    # Se piden los demas datos con sus validaciones ningun campo puede quedar vacio
    poblacion = validar_numero(f"Ingrese la poblacion de {nombre}: ")
    superficie = validar_numero(f"Ingrese la superficie de {nombre}: ")
    continente= texto_sin_coma(f"Ingrese el continente donde se encuentra {nombre}: ")
    
    # Se arma el diccionario del pais nuevo con la misma estructura que los demas
    pais= {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    
    # Se agrega a la lista y se guarda en el csv y el mensaje de exito solo aparece si el guardado funciono.
    paises.append(pais)
    if guardar_paises(paises, "paises.csv"):
        mostrar_mensaje_exito(f"Se agrego el pais {nombre} y se guardo en el archivo")

# Busca un pais por nombre exacto (sin distinguir mayusculas) y devuelve su posicion en la lista o -1 si no existe. Se usa para evitar repetidos y para encontrar el pais a actualizar.
def buscar_porcision(paises, nombre):
    for i in range(len(paises)):
        if paises[i]["nombre"].lower() == nombre.lower():
            return i
    # Si termino el recorrido sin encontrarlo, devuelve -1
    return -1

# OPCION 2: actualizar pais
# Pide el nombre de un pais y actualiza su poblacion y superficie y despues guarda los cambios en el csv.

def actualizar_pais(paises):
    print("Actualizar pais")
    # Se busca el pais; si no existe se muestra un error y se vuelve al menu
    nombre=validar_texto("Ingrese el nombre del pais que desea actualizar: ")
    posicion =buscar_porcision(paises, nombre)
    if posicion ==-1:
        mostrar_mensaje_error(f"Error; no se encontro el pais ingresado: {nombre}")
        return
    
    # pais apunta al mismo diccionario que esta dentro de la lista, por eso al modificarlo se modifica tambien la lista
    pais=paises[posicion]
    print(f"Datos actuales: {pais['nombre']} | {pais['poblacion']} | {pais['superficie']} | {pais['continente']}")
    
    # Se piden los nuevos valores con validacion
    nueva_poblacion=validar_numero(f"Ingrese la nueva poblacion de {nombre}: ")
    nueva_superficie=validar_numero(f"Ingrese la nueva superficie de {nombre}: ")
    
    # Se guarda en el csv y se avisa si salio bien
    pais["poblacion"] = nueva_poblacion
    pais["superficie"] = nueva_superficie
    if guardar_paises(paises, "paises.csv"):
        mostrar_mensaje_exito("Los cambios se guardaron correctamente en el archivo paises.csv")

# OPCION 3: buscar pais por nombre
# Busca paises cuyo nombre contenga el texto ingresado tambien sirve para coincidencia parcial "arg" encuentra Argentina y tambien para exacta (el nombre completo).
def buscar_pais_por_nombre(paises):
    print(f"Buscar pais por nombre")
    nombre= validar_texto("Ingrese nombre o parte del nombre del pais que desea buscar: ")
    # Lista donde se guardan los paises que coinciden
    resultados = []
    for pais in paises:
        if nombre.lower() in pais["nombre"].lower():
            resultados.append(pais)
            
    # Se informa el resultado: aviso si no hay coincidencias, o tabla si las hay
    if len(resultados) ==0:
        mostrar_mensaje_aviso(f"No se ha encontrado ningun pais que contenga: {nombre}")
    else:
        mostrar_mensaje_exito(f"Se han encontrado {len(resultados)} paises que contienen: {nombre}")
        mostrar_paises(resultados)

# OPCION 4: filtrar paises

# Devuelve una lista con los continentes que hay sin repetir se usa para mostrarle al usuario las opciones validas al filtrar.
def obtener_continentes(paises):
    continentes=[]
    for pais in paises:
        # Solo se agrega si todavia no esta en la lista
        if pais["continente"] not in continentes:
            continentes.append(pais["continente"])
    return continentes

# Muestra un submenu de filtros
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
# Para volver al menu principal
    if opcion is None:
        return "0"
    return opcion

# Filtra los paises de un continente y muestra los continentes disponibles
def filtrar_continente(paises):
    print(f"Filtrar por continente")
    print("Continentes disponibles:")
    
    for continente in obtener_continentes(paises):
        print(f"- {continente}")
    continente = validar_texto("Ingrese el continente por el que desea filtrar: ")
    # Se guardan los paises cuyo continente coincide sin distinguir mayusculas
    resultados= []

    for pais in paises:
        if pais["continente"].lower()== continente.lower():
            resultados.append(pais)
    # Si el continente no existe, no falla solo avisa que no hubo resultados
    if len(resultados)==0:
        mostrar_mensaje_aviso(f"No se han encontrado paises en el continente: {continente}")
    else:
        mostrar_mensaje_exito(f"Se han encontrado {len(resultados)} paises en el continente: {continente}")
        mostrar_paises(resultados)

# Filtra por un rango minimo y maximo de un campo de numeros.
# El parametro campo es "poblacion" o "superficie" asi una sola funcion sirve para los dos filtros.
def filtrar_rango_poblacion_superficie(paises, campo):
    print(f"Filtrar por {campo}")
    minimo = validar_numero(f"Ingrese el valor minimo de {campo}: ")
    maximo = validar_numero(f"Ingrese el valor maximo de {campo}: ")

    # Filtro invalido: el minimo no puede ser mayor que el maximo
    if minimo > maximo:
        mostrar_mensaje_error(f"Error: el minimo ({minimo}) no puede ser mayor que el maximo ({maximo})")
        return
    # Se guardan los paises cuyo valor esta dentro del rango
    resultados = []
    for pais in paises:
        if pais[campo] >= minimo and pais[campo]<= maximo:
            resultados.append(pais)
    # Si ninguno entra en el rango se avisa, no es un error.
    if len(resultados)==0:
        mostrar_mensaje_aviso(f"No se han encontrado paises con {campo} entre {minimo} y {maximo}")
    else:
        mostrar_mensaje_exito(f"Se han encontrado {len(resultados)} paises con {campo} entre {minimo} y {maximo}")
        mostrar_paises(resultados)
# Un submenu de filtros se repite hasta que el usuario elija volver al menu principal
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

# OPCION 5: ordernar paises
# Ordena la lista con el metodo de la burbuja.
# Devuelve una lista nueva y  la original queda sin cambios algo asi: "nombre", "poblacion" o "superficie". decendente: True o False.
def ordernar_lista(paises, campo, decendente):
    # Se hace una copia de la lista para no modificar la original
    lista= []
    for pais in paises:
        lista.append(pais)
    n=len(lista)

    # En cada pasada se comparan los pares vecinos y se intercambian
    # y si estan en el orden equivocado despues de cada pasada el mayor (o menor) sube al final y por eso cada vez se recorre un elemento menos.
    for i in range(n - 1):
        for j in range(n - i - 1):
            actual = lista[j][campo]
            siguiente = lista[j+1][campo]
            # Los nombres se comparan en minusculas para que no importe si empiezan con mayuscula o minuscula
            if campo=="nombre":
                actual = actual.lower()
                siguiente = siguiente.lower()
            # Segun el sentido, se decide cuando hay que intercambiar
            if decendente:
                intercambiar = actual < siguiente
            else:
                intercambiar = actual > siguiente

            # Intercambio de posiciones usando una variable auxiliar
            if intercambiar:
                aux = lista[j]
                lista[j] = lista[j + 1]
                lista[j + 1] = aux
    return lista

# Pregunta si el orden es ascendente o descendente
# devuelve true si eligio descendente y false si eligio ascendente.
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
    # La comparacion ya da directamente True o False
    return opcion == "2"

# Muestra el submenu de ordenamiento y devuelve la opcion elegidos
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

# Pregunta el sentido de ordena por el campo indicado y muestra el resultado en una tabla
def mostrar_odernados(paises, campo):
    decendente = elegir_sentido_ordenamiento()
    lista_ordenada = ordernar_lista(paises, campo, decendente)
    
    if decendente:
        sentido = "descendente"
    else:
        sentido= "ascendente"
    print(f"Paises ordenados por {campo} ({sentido})")
    mostrar_paises(lista_ordenada)
    
# Submenu de ordenamiento que repite hasta que el usuario elija volver al menu principal
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

# OPCION 6: estadisticas

# Devuelve el diccionario del pais con mayor poblacion.
# se supone que el primero es el mayor y se compara con cada uno si aparece uno con mas poblacion, pasa a ser el nuevo mayor.
def pais_mas_poblado(paises):
    mayor_poblacion = paises[0]
    for pais in paises:
        if pais["poblacion"] > mayor_poblacion["poblacion"]:
            mayor_poblacion = pais
    return mayor_poblacion

# Devuelve el diccionario del pais con menos poblacion, lo mismo pero al reves
def pais_menos_poblado(paises):
    menor_poblacion = paises[0]
    for pais in paises:
        if pais["poblacion"] < menor_poblacion["poblacion"]:
            menor_poblacion = pais
    return menor_poblacion

# Calcula el promedio de un campo numerico "poblacion" o "superficie" suma todos los valores y divide por la cantidad de paises.
def calcular_promedio(paises, campo):
    total = 0
    for pais in paises:
        total = total + pais[campo]
    return total / len(paises)

# Cuenta cuantos paises hay por continente y devuelve un diccionario
# con la forma continente: cantidad, por ejemplo {"Asia": 5, "Europa": 5}
def contar_paises_por_continente(paises):
    conteo={}
    for pais in paises:
        continente =pais["continente"]
        if continente in conteo:
            # Si el continente ya esta en el diccionario se suma uno
            conteo[continente]= conteo[continente] + 1
        else:
            # Si es la primera vez que aparece, empieza en 1
            conteo[continente] = 1
    return conteo

# Calcula y muestra todas las estadisticas
def mostrar_estadisticas(paises):
    print("Estadisticas de paises")
    
    # Con la lista vacia no se puede calcular nada
    if len(paises)==0:
        mostrar_mensaje_aviso("No hay paises cargados para mostrar estadisticas")
        return

    # Cada calculo lo hace una funcion distinta (una funcion = una responsabilidad)
    mayor_poblado = pais_mas_poblado(paises)
    menor_poblado = pais_menos_poblado(paises)
    promedio_poblacion = calcular_promedio(paises, "poblacion")
    promedio_superficie = calcular_promedio(paises, "superficie")
    conteo_por_continente = contar_paises_por_continente(paises)
    
    # Se muestran los resultados: round y  deja los promedios con 2 decimales
    print(f"Pais mas poblado: {mayor_poblado['nombre']} con {mayor_poblado['poblacion']} habitantes")
    print(f"Pais menos poblado: {menor_poblado['nombre']} con {menor_poblado['poblacion']} habitantes")
    print(f"Promedio de poblacion: {round(promedio_poblacion, 2)}")
    print(f"Promedio de superficie: {round(promedio_superficie, 2)} km2")
    print("Cantidad de paises por continente:")
    for continente in conteo_por_continente:
        print(f"- {continente}: {conteo_por_continente[continente]} paises")

#====================================
# PROGRAMA PRINCIPAL

# Arma el flujo general del menu: carga los datos y repite el menu principal hasta que el usuario elija salir.
def main():
        # 1: leer el cvs y guardar los paises en una lista de diccionarios
    paises = cargar_paises("paises.csv")
    print(f"Se cargaron {len(paises)} países")
    opcion = ""
    # 2: Bucle del menu, se repite hasta que la opcion sea "0" o le salir.
    while opcion != "0":
        opcion = elegir_opcion_menu()
        # 3: Segun la opcion elegida se llama a la funcion 
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
# Donde arranca el programa, se ejecuta el archivo basicamente
main()