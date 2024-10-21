import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
            print(f"Se eliminará la columna {k} por tener {v} valores nulos") #eliminar este promt de pantalla al eliminar columnas
            del dataframe[k]
    return dataframe    

def calcular_ingresos_por_pais(dataframe):
    Paises = ["Germany", "Spain", "Chile", "Austria", "United States of America"]
    DataPromedio = []
    
    for i in range(len(Paises)):
        df_pais = dataframe.loc[dataframe['Country'] == Paises[i]]
        # print(Paises[i], df_pais, df_pais.shape)
        contador = 0
        suma = 0
        for index in range(df_pais.shape[0]):
            if df_pais.iloc[index]['ConvertedCompYearly']  != "Sin información":
                contador += 1
                suma += float(df_pais.iloc[index]['ConvertedCompYearly'])
        
        if contador != 0: promedio = suma / contador

        DataPromedio.append([Paises[i] , promedio])  # el promedio por país está dentro de una lista de tuplas
            
    Data_ordenada = sorted(DataPromedio, key=lambda x: x[1], reverse=True) # Retorna una lista ordenada desde el key promedio de la tupla
    #Luego de ordenar la lista, lo formateo a miles "."      
    for i in range(len(Data_ordenada)):
        Data_ordenada[i][1] = '{:,.0f}'.format(Data_ordenada[i][1]).replace(',','.')
    #transpaso la lista ordenada de tuplas a un data frame con las columnas seleccionadas
    df_ordenado_paises = pd.DataFrame(Data_ordenada, columns=["Pais", "Ingreso promedio"])
    
    return df_ordenado_paises

def calcular_ingresos_por_experiencia(dataframe):
    df = dataframe.loc[:, ["YearsCode","YearsCodePro", "ConvertedCompYearly"]]  # realizo un dataframe con tres columnas 
    # df["Age"] = df["Age"].str.split(" ",expand=True)[0]    
    df["YearsCode"] = np.where(df["YearsCode"]=="Sin información", "0", df["YearsCode"])
    df["YearsCode"] = np.where(df["YearsCode"]=="Less than 1 year", "0", df["YearsCode"])
    df["YearsCode"] = np.where(df["YearsCode"]=="More than 50 years", "51", df["YearsCode"])

    df["YearsCodePro"] = np.where(df["YearsCodePro"]=="Sin información", "0", df["YearsCodePro"])
    df["YearsCodePro"] = np.where(df["YearsCodePro"]=="Less than 1 year", "0", df["YearsCodePro"])
    df["YearsCodePro"] = np.where(df["YearsCodePro"]=="More than 50 years", "51", df["YearsCodePro"])
    
    df.drop(df[df["ConvertedCompYearly"]=="Sin información"].index, inplace=True)
    
    df["YearsCode"] = df["YearsCode"].astype('float64')
    df["YearsCodePro"] = df["YearsCodePro"].astype('float64')
    df["ConvertedCompYearly"] = df["ConvertedCompYearly"].astype('float64')
    
    df.drop(df[df["ConvertedCompYearly"]=="Sin información"].index, inplace=True)
    
    df["Años de experiencia"] = df["YearsCode"] + df["YearsCodePro"]
    
    df.drop(df[df["Años de experiencia"]>55].index, inplace=True)
    lista =[]
    rango = [0,5,10,15,20,25,30,35,40,45,50,55]
    for i in range(len(rango)-1):
        df_intervalo_min = df.loc[(df["Años de experiencia"]>=rango[i]) & (df["Años de experiencia"]<rango[i+1])].groupby("Años de experiencia").min()
        df_intervalo_max = df.loc[(df["Años de experiencia"]>=rango[i]) & (df["Años de experiencia"]<rango[i+1])].groupby("Años de experiencia").max()
        lista.append([(str(rango[i])+"-"+str(rango[i+1])), df_intervalo_min["ConvertedCompYearly"].min(), df_intervalo_max["ConvertedCompYearly"].max()])
    
    df_intervalo = pd.DataFrame(lista, columns=["Años de experiencia","Intervalo inferior (USD/Año)","Intervalo superior (USD/Año)"])
    
    df_intervalo["Intervalo inferior (USD/Año)"] = df_intervalo["Intervalo inferior (USD/Año)"].map("{:,.0f}".format)
    df_intervalo["Intervalo superior (USD/Año)"] = df_intervalo["Intervalo superior (USD/Año)"].map("{:,.0f}".format)
    
    # //////////////////////////////////////////
    #creo un nuevo data frame con el indice de Años de experienciencia y me los agrupa con el valor mínimo y valor máximo
    # df2 = df.pivot_table(index="Age", values="ConvertedCompYearly", aggfunc={np.min,np.max})
    # #reseteo el indice para que los años de experiencia me queden como una columna mas
    # df2.reset_index(inplace=True)
    # #doy formato a los resultadso de max y min
    # df2["max"] = df2["max"].map("{:,.0f}".format)
    # df2["min"] = df2["min"].map("{:,.0f}".format)
    # df.rename(columns={"Age":"Años de experiencia"}, inplace=True)
    # df2.rename(columns={"max":"Intervalo superior (USD/Año)","min":"Intervalo inferior (USD/Año)"}, inplace=True)

    print(df_intervalo)
    return df_intervalo

def calcular_empleabilidad(dataframe):
    return dataframe[dataframe['Country']=='Chile']

def graficar_ingresos_paises(dataframe):
    dataframe['Ingreso promedio'] = dataframe['Ingreso promedio'].astype('float64')
    dataframe.plot(kind="bar", x="Pais", y="Ingreso promedio", title="Ingresos x Países")
    plt.show()

if __name__ == "__main__":
    df = cargar_dataset("developers_info.csv")
    df_limpios = limpiar_dataset(df,50)
    # df_p = calcular_ingresos_por_pais(df_limpios)
    df_i = calcular_ingresos_por_experiencia(df_limpios)
    print(df_i.dtypes) 

    # graficar_ingresos_paises(df_p)

    