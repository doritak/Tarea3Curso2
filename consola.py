import pandas as pd
from consultas import cargar_dataset, limpiar_dataset, calcular_ingresos_por_pais, calcular_ingresos_por_experiencia, calcular_empleabilidad, graficar_ingresos_paises


def cargar_menu():
    print('Para continuar ingrese el número equivalente a la consulta:')
    print('[1] Limpieza de datos')
    print('[2] Calcular ingresos por país')
    print('[3] Calcular ingresos por experiencia')
    print('[4] Calcular empleabilidad')
    print('[5] Graficar ingresos paises')
    print('[6] Salir')

def validar_ingreso(cota_superior: int):
    if cota_superior == 6: cargar_menu()
    # las opciones lo puse en una lista, porque tambien lo uso cuando el usuario ingresa un nro. de 1 al 100 para el porcentaje no nulos admitido   
    Opcion = [i+1 for i in range(cota_superior)]
    while True:
        try:
            sel = int(input("Ingrese aquí: "))
            num = Opcion[sel-1]  #si es un número pero esta fuera de la lista de opciones válidas
            if (sel < 0): raise NameError('NumNegativo')  # si es un número negativo, pq cómo usé lista, me aceptaba los num. neg. del 1 al 5
        except ValueError as e:
            print(f"Favor ingresar un número sólo un número. Tipo de Error: {e}"),
        except IndexError as e:
            print(f"Valor del número incorrecto, selecciona sólo del 1 al {cota_superior}. Tipo de Error: {e}")
        except NameError: 
            print("Favor ingresar sólo números positivos.")
        else:
            return num
        
#funcion de impresion de nombre de la funcion seleccionada        
def imprimir_nombre_funcion(titulo):
    print("\033[35m"+"="*20+f" Selección {titulo} "+"="*20+"\033[39m")
    
    
if __name__== "__main__":
    
    seleccion = {}
    matriz_Seleccion = {
        1: limpiar_dataset,
        2: calcular_ingresos_por_pais,
        3: calcular_ingresos_por_experiencia,
        4: calcular_empleabilidad,
        5: graficar_ingresos_paises
    }
    
    df = cargar_dataset("developers_info.csv")
    df_limpio = pd.DataFrame()
    print('¡Hola, bienvenido/a!')
    numero = validar_ingreso(6)
    cont = 0  # cuenta la cantidad de veces que ha seleccionado el usuario
    
    while numero != 6:
        seleccion[cont] = matriz_Seleccion[numero].__name__  # la selección que haya realizado el user lo dejo en un dict con el nombre de la funcion en str
        funcion = matriz_Seleccion[numero]
        
        if numero == 1:
            print("Ingrese un número máximo de nulos, en porcentaje del 1 al 100, para eliminar columnas que no cumplan esta condición.")
            num_max_null = validar_ingreso(100)
            df_limpio = funcion(df, num_max_null)
            imprimir_nombre_funcion(seleccion[cont])
            print(df_limpio)
            cont+=1
        else:
            if 1 in seleccion:  #si ya ingresó la opcion nro. 1 para tener un df_limpio para las otras opciones
                imprimir_nombre_funcion(seleccion[cont])
                df_funcion = funcion(df_limpio)
                if numero != 5: print(df_funcion) # cuando elige el gráfico
                cont+=1
            else:
                print("Primero debes seleccionar limpiar el Dataframe, para llegar a las otras opciones.")
        if cont >0: 
            print("\033[35m"+f"Hasta ahora haz seleccionado estas opciones {' - '.join(list(seleccion.values()))}"+"\033[39m")  # uso el join y por eso lo tengo que pasar a list pero de sólo los nombres de las funciones
        numero = validar_ingreso(6)
    print("\033[35m"+"Gracias por participar!"+"\033[39m")
    

    