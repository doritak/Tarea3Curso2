import pandas as pd

def cargar_dataset(ruta_dataset: str):
    df = pd.read_csv(ruta_dataset,encoding="latin-1",sep=",")
    print(df.head(5))
    return df

# eliminar aquellas columnas que posean un porcentaje mayor a cantidad_null% de celdas nulas y luego reemplazar
# las celdas nulas restantes con el str 'Sin informaci´on'. Finalmente, debes retornar el dataframe limpio.
def limpiar_dataset(dataframe, cantidad_null: int):
    ValoresSinDatos = {}
    PorcentajeSinDatos = {}
    Columna = list(dataframe.columns.values)
    TotalFilas = dataframe.shape[0]

    dataframe = dataframe.fillna("Sin información")
    
    for col in range(len(Columna)):
        print(Columna[col])
        contador = 0
        for index in range(TotalFilas):
            if dataframe.loc[index][Columna[col]]  == "Sin información":
                contador += 1
        ValoresSinDatos[Columna[col]] = contador
    
    for k,v in ValoresSinDatos.items():
          porcentaje = v / TotalFilas * 100
          PorcentajeSinDatos[k] = porcentaje
          
    for k,v in PorcentajeSinDatos.items():
        if PorcentajeSinDatos[k] > cantidad_null:
            print(f"Se eliminará la columan {k} por tener {v} valores nulos")
            del dataframe[k]
    return dataframe    

def calcular_ingresos_por_pais(dataframe):
    Paises = ["Germany", "Spain", "Chile", "Austria", "United States of America"]
    DataPromedio = []
    
    for i in range(len(Paises)):
        df_pais = dataframe.loc[dataframe['Country'] == Paises[i]]
        contador = 0
        suma = 0
        for index in range(df_pais.shape[0]):
            if df_pais.iloc[index]['ConvertedCompYearly']  != "Sin información":
                contador += 1
                suma += float(df_pais.iloc[index]['ConvertedCompYearly'])

        # print("VER AQUÍ DATOS POR PAÍS :")
        # print(Paises[i], df_pais.shape, contador, suma)
        
        if contador != 0: promedio = suma / contador

        DataPromedio.append([Paises[i] , promedio])  # el promedio por país está dentro de una lista de tuplas
            
    Data_ordenada = sorted(DataPromedio, key=lambda x: x[1], reverse=True) # Retorna una lista ordenada desde el key promedio de la tupla
    #Luego de ordenar la lista, lo formateo a miles "."      
    for i in range(len(Data_ordenada)):
        Data_ordenada[i][1] = '{:,.0f}'.format(Data_ordenada[i][1]).replace(',','.')
    #transpaso la lista ordenada de tuplas a un data frame con las columnas seleccionadas
    df_ordenado_paises = pd.DataFrame(Data_ordenada, columns=["País", "Ingreso promedio"])
    
    return df_ordenado_paises


if __name__ == "__main__":
    df = cargar_dataset("developers_info.csv")
    df_limpios = limpiar_dataset(df,50)
    print(calcular_ingresos_por_pais(df_limpios))
    # print(df.dtypes)