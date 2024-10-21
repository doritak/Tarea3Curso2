import pandas as pd
from consultas import cargar_dataset, limpiar_dataset, calcular_ingresos_por_pais, calcular_ingresos_por_experiencia, calcular_empleabilidad, graficar_ingresos_paises


def cargar_menu():
    print('Para continuar ingrese el número equivalente a la consulta:')
    print('¡Hola, bienvenido/a!')
    print('[1] Limpieza de datos')
    print('[2] Calcular ingresos por país')
    print('[3] Calcular ingresos por experiencia')
    print('[4] Calcular empleabilidad')
    print('[5] Graficar ingresos paises')
    print('[6] Salir')

def validar_ingreso(cota_superior: int):
    if cota_superior == 6: cargar_menu()
    Opcion = [i+1 for i in range(cota_superior)]
    while True:
        try:
            sel = int(input("Ingrese aquí:"))
            num = Opcion[sel-1]
        except ValueError as e:
            print(f"Favor ingresar un número sólo un número. Tipo de Error: {e}"),
        except IndexError as e:
            print(f"Valor del número incorrecto, selecciona sólo del 1 al {cota_superior}. Tipo de Error: {e}")
        else:
            if (sel < 0):
                print("Favor ingresar sólo números positivos.")
            else:
                return num

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
    numero = validar_ingreso(6)

    while numero != 6:
        seleccion[numero] = matriz_Seleccion[numero]
        funcion = seleccion[numero]
        if numero == 1:
            print("Ingrese un número máximo de nulos, en porcentaje del 1 al 100, para eliminar columnas que no cumplan esta condición.")
            num_max_null = validar_ingreso(100)
            df_limpio = funcion(df, num_max_null)
        else:
            if 1 in seleccion:  #si ya ingresó la opcion nro. 1 para tener un df_limpio no vacío
                if numero != 5:
                    print(funcion(df_limpio))
                else: # sólo para cuando entres a la opción 5 gráfico, debes tener primero los datos de calcular ingresos por pais
                    df_p = calcular_ingresos_por_pais(df_limpio)
                    graficar_ingresos_paises(df_p)
            else:
                print("Primero debes seleccionar limpiar el Dataframe, para llegar a las otras opciones.")
        numero = validar_ingreso(6)
    print("Gracias por participar!")

    