# Tarea 3 Curso 2 : Pandas y Excepciones
## Objetivos
El objetivo de esta tarea es evaluar el uso de Pandas y Excepciones mediante el manejo de un **dataset** y los posibles errores que pueden surgir.
## Archivos entregados
`developers_info.csv` Este archivo contiene información de desarrolladores alrededor del mundo, tal como su nivel educacional, sus años de experiencia, su estatus laboral, los lenguajes en los han programado, los distintos tipos de tecnologías con las que han trabajado, etc. Este corresponde al **dataset** con el que deberás trabajar en la tarea para extraer la información solicitada.
## Trabajo a realizar
Esta tarea se divide en dos partes: La primera parte consiste en completar funciones que trabajan con el dataset entregado mediante el uso de Pandas, y la segunda parte consiste en crear un menú a prueba de errores utilizando excepciones. A continuación se detalla en que consisten ambas secciones.
 
### Parte 1: Funciones solicitadas
- [x] **def cargar_dataset(ruta_dataset: str) -> df:** Esta función recibe como parámetro un `str` con la ruta del archivo csv que contiene el dataset. Deberás cargar este dataset usando pandas, mostrar las primeras 5 filas para entender su contenido y finalmente retornar el dataset cargado.
- [x] **def limpiar_dataset(dataframe: df, cantidad_null: int) -> df:** En esta función deberás encargarte de limpiar el dataframe cargado anteriormente. En específico, debes eliminar aquellas columnas que posean un porcentaje mayor a **cantidad_null%** de celdas nulas y luego reemplazar las celdas nulas restantes con el `str 'Sin información'`. Finalmente, debes retornar el dataframe limpio.
- [x] **def calcular_ingresos_por_pais(dataframe: df) -> df:** Esta función recibe como argumento el dataframe retornado por la función `limpiar_dataset`. Debes calcular el ingreso promedio de 5 países a tu elección y retornar este **nuevo dataframe** ordenado por ingreso promedio de mayor a menor.<br>
  <img width="203" alt="ingreso_por_pais" src="https://github.com/user-attachments/assets/efa0df6d-80c9-4af6-b9be-12cba676a388">

- [x] **def calcular_ingresos_por_experiencia(dataframe: df) -> df:** Esta función recibe como argumento el dataframe retornado por la función `limpiar_dataset`. Debes calcular el rango de ingresos que poseen los desarrolladores que tienen un rango de años de experiencia. Para esto, el dataframe debe contener **3 columnas**:
  - Años de experiencia: Esta columna debe indicar el rango de años de experiencia de los desarrolladores, los cuales deben ir en intervalos de 5 años, es decir, 0-5, 5-10, 10-15, etc. Para cada rango se debe considerar el **limite inferior** del intervalo, pero no el límite superior, es decir, el intervalo de 0-5 considera a los desarrolladores que tienen 0, 1, 2, 3 y 4 años de experiencia.
  - Ingreso menor: Corresponde al menor ingreso que poseen los desarrolladores que se encuentran en cada rango.
  - Ingreso mayor: Corresponde al mayor ingreso que poseen los desarrolladores que se encuentranen cada rango.<br>
  Finalmente, debes retornar el dataframe generado.
  <img width="534" alt="igreso_years_experience" src="https://github.com/user-attachments/assets/b74ceeae-8fd2-42e6-bbdf-7dd4a7718451">

- [x] **def calcular_empleabilidad(dataframe: df) -> df:** Esta función recibe como argumento el dataframe retornado por la función `limpiar_dataset`. Deberás encontrar el **porcentaje de empleabilidad** basado en la raza y el género de los desarrolladores. Para esto, debes considerar todas las combinaciones posibles de raza y género existentes en el dataset, es decir, todos los posibles pares (raza, genero) sin repeticciones. Debes asegurarte de manejar posibles errores o entradas inesperadas de manera adecuada. Para facilitar considere solamente las siguentes razas/generos:
```
  [
    "Black or of African descent",
    "Hispanic or Latino/a/x",
    "East Asian",
    "I don't know",
    "Indigenous",
    "Middle Eastern",
    "White or of European descent"
  ]
  [
   'Man',
   'Non-binary',
   'genderqueer',
   'gender non-conforming',
   'Woman'
   ]
```
  Suponga que se tiene un **dataset** representado por la siguiente tabla:<br>
  <img width="366" alt="df_por_gender" src="https://github.com/user-attachments/assets/50512845-efff-4e51-a032-581198990077"><br>
  En ese caso, el resultado esperado sería:<br>
  <img width="270" alt="resultado_empleabilidad_x_gender" src="https://github.com/user-attachments/assets/08e80263-986c-415c-9cb3-7d4c38de6c89">

- [x] _(Bonus)_ **def graficar_ingresos_paises(dataframe: df):** En esta función deberás graficar (en formato a tu elección) el ingreso promedio calculado en la función `calcular_ingresos_por_pais` versus los 5 países elegidos. Esta función otorga 1 pto extra al puntaje total.

### Parte 2: Consola con Excepciones
Para esto, es necesario guardar las consultas en forma de un `dict`, donde cada llave corresponda al número de consulta y su valor corresponda a la función a ejecutar.
```
'¡Hola, bienvenido/a!'
'Para continuar ingrese el numero equivalente a la consulta:'
'[1] Limpieza de datos'
'[2] Calcular ingresos por paıs'
'[3] Calcular ingresos por experiencia'
'[4] Calcular empleabilidad'
'[5] Graficar ingresos paises'
'[6] Salir'
# El numero al lado izquierdo corresponde a la llave.
# Esta debe estar asociada a la consulta correspondiente.
# Por ejemplo {1: limpiar_dataset}
```
> [!IMPORTANT]
> El uso de `if/else statements` para el manejo de errores implica **0 puntos** en esta sección. Además, no se considerará correcto el uso de `except` sin argumentos o de `except Exception`, sino que debes identificar los posibles tipos de errores y trabajar con estos.
## Archivos a entregar
Deben entregar un archivo .zip (carpeta comprimida) con los archivos a trabajar: `consultas.py` para la **primera parte** y `consola.py` para la **segunda parte**.

## Puntaje
* (4.0 pts) Parte 1: Pandas.
  * (0.5 pt) Función cargar_dataset.
  * (0.5 pt) Función limpiar_dataset.
  * (1.0 pt) Función calcular_ingresos_por_pais.
  * (1.0 pt) Función calcular_ingresos_por_experiencia.
  * (1.0 pt) Función calcular_empleabilidad.
* (2.0 pts) Parte 2: Excepciones.
* (1.0 pt extra) Función Gráfico de Ingresos por países.
