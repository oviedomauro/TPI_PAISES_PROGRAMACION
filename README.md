**Alunno:** Mauro oviedo
**Legajo:** 54287
# Gestion de Datos de Paises

Trabajo Practico Integrador de **Programacion 1**
Tecnicatura Universitaria en Programacion

## Descripcion

Programa de consola en python que gestiona informacion de paises a partir de un archivo csv. Los datos se cargan en una **lista de diccionarios** (un diccionario por pais) y desde un menu se pueden agregar, actualizar, buscar, filtrar y ordenar paises y ademas de ver estadisticas.

Cada pais tiene estos datos:

| Campo | Tipo | Ejemplo |
|---|---|---|
| nombre | texto | Argentina |
| poblacion | entero | 46234830 |
| superficie | entero | 2780400 |
| continente | texto | America |

## Funcionalidades:

1. **Agregar pais:** no se permiten campos vacios, nombres repetidos ni comas y se guarda en el csv.
2. **Actualizar pais:** modifica poblacion y superficie. Se guarda en el CSV.
3. **Buscar por nombre:** coincidencia parcial o exacta.
4. **Filtrar:** por continente, rango de pobalcion o rango de superficie.
5. **Ordenar:** por nombre, poblacion o superficie, de forma ascendente o descendente y usando metodo burbuja.
6. **Estadisticas:** pais con mayor y menor población, promedio de poblacion, promedio de superficie y cantidad de paises por continente.
7. **Mostrar todos los paises.**

### Validaciones:

- Errores de formato en el csv: archivo inexistente, vacio, con otra codificacion, sin encabezado, lineas con cantidad de campos incorrecta, campos vacios, valores no numericos, valores menores o iguales a cero y paises repetidos. Las lineas invalidas se ignoran con un aviso y el programa sigue funcionando con normalidad.

- Entradas del usuario: numeros enteros mayores a cero, textos no vacios y rango con minimo menor o igual al maximo.

- Busquedas y filtros sin resultados muestran un aviso, no un error simple.

- Mensajes de exito (verde), aviso (amarillo) y error (rojo).

## Requisitos:

- **Python 3.10 o superior** (porque se usa el `match`/`case`).

- Librerias `questionary` y `rich`, que están en `requirements.txt`.

## Pasos para instalacion y ejecucion:

1. Descarga el repositorio y abri una terminal en la carpeta del proyecto.
2. Instala las librerias:

    python -m pip install -r requirements.txt

3. Ejecuta el programa (desde la misma carpeta donde esta `paises.csv`) en la terminal:

    python main.py


   En Windows, si `python` no se reconoce, usá `py main.py` (en todos los casi siempre funciona).

Y se navega con las flechas y Enter, o escribiendo el numero de la opcion.

## Estructura del proyecto:


├── main.py            # codigo fuente completo
├── paises.csv         # dataset base
├── requirements.txt   # libreraas necesarias
├── README.md          # este archivo que esta leyendo
└── INFORME.pdf        # documentacion en PDF  


## Ejemplos de uso:

**Carga inicial**

Se cargaron 21 paises

**Buscar pais por nombre** (opción 3), entrada `arg`:

Se han encontrado 1 paises que contienen: arg

| Nombre | Población | Superficie (km2) | Continente |
|---|---:|---:|---|
| Argentina | 46234830 | 2780400 | America |

**Filtrar por continente** (opcion 4 → Continente), entrada `Europa`:

Se han encontrado 5 paises en el continente: Europa

**Busqueda sin resultados**, entrada `xyz`:

No se ha encontrado ningun pais que contenga: xyz

**Rango invalido** (minimo 500, máximo 100):

Error: el minimo (500) no puede ser mayor que el maximo (100)

**Agregar un pais que ya existe**, entrada `chile` cuando ya esta Chile:

Error: el pais chile ya existe en la lista

**Estadisticas** (opcion 6):

Estadisticas de paises
Pais mas poblado: China con 1412914089 habitantes
Pais menos poblado: Costa Rica con 5094114 habitantes
Promedio de poblacion: 158946144.76
Promedio de superficie: 1982832.62 km2
Cantidad de paises por continente:
- America: 6 paises
- Asia: 5 paises
- Europa: 5 paises
- Oceania: 1 paises
- Africa: 4 paises

## Formato del CSV:

nombre,poblacion,superficie,continente
Argentina,46234830,2780400,America
China,1412914089,9596961,Asia

La primera linea es el encabezado. El archivo debe estar guardado en UTF-8 ni el nombre ni el continente pueden contener comas.



## Enlaces

- **Video demostrativo:**  https://youtu.be/4FfXxJNJU6c
- **Documentacion en PDF:** file:///C:/Users/Mauro%20Oviedo/Downloads/tpi,oviedo_mauro.pdf