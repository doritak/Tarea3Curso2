import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Tarea entregada el 25 de octubre 2024
# Dora Novoa

def cargar_dataset(ruta_dataset: str):
    df = pd.read_csv(ruta_dataset,encoding="latin-1",sep=",")
    print(df.head(5))
    return df


def limpiar_dataset(dataframe, cantidad_null: int):
    
    col_no_eliminar = ["Employment","Country","YearsCode","Gender","Ethnicity","ConvertedCompYearly"]
    TotalFilas = len(dataframe)
    
    sr_contar_no_nulos = dataframe.count()
    
    # el count devuelve una serie con núm de elementos no nulos ni NaN de c/col, si lo divido x total de filas y le resto 1, tengo los elementos nulos
    sr_porcentaje = (1-(sr_contar_no_nulos/TotalFilas))*100

    df = dataframe.fillna("Sin información")
    
    # Paso por toda la serie y cuando cumple la condicion, elimino la columna, el index de la serie son los nombres de las col de df
    for i, valor in enumerate(sr_porcentaje):
        if valor > cantidad_null:
            if not sr_porcentaje.index[i] in col_no_eliminar: # valido que nunca va a eliminar las columnas que serán ocupadas para selecciones posteriores.
                col = sr_porcentaje.index[i]
                del df[col]
    
    return df    
    

def calcular_ingresos_por_pais(dataframe):

    Paises = ["Germany", "Spain", "Chile", "Austria", "United States of America"]
    dataframe.drop(dataframe[dataframe["ConvertedCompYearly"]=="Sin información"].index, inplace=True)
    dataframe['ConvertedCompYearly'] = dataframe['ConvertedCompYearly'].astype('float64')

    #df_paises = df.pivot_table(index="Country", values="ConvertedCompYearly", aggfunc=np.mean)
    df_Tpaises = dataframe.groupby("Country").agg({"ConvertedCompYearly":"mean"})
    df_Tpaises.reset_index(inplace=True)
    df = pd.DataFrame()
    for pais in Paises:
        l_pais = df_Tpaises[df_Tpaises["Country"]==pais]
        df = pd.concat([l_pais,df],ignore_index=True)
        ##f.append(p,ignore_index=True) --- no puede usar el append pq me sale un error pq esta descontinuado 

    df.sort_values(by="ConvertedCompYearly", ascending=False, inplace=True)
    df["ConvertedCompYearly"]=df["ConvertedCompYearly"].map("{:,.0f}".format).apply(lambda x:x.replace(",","."))
    df.rename(columns={"Country":"País", "ConvertedCompYearly":"Ingreso promedio"}, inplace=True)
    df.loc[df["País"]=="United States of America", "País"]="U.S.A"
    
    return df


def calcular_ingresos_por_experiencia(dataframe):
    # realizo un dataframe con 2 columnas, que son las que me interesan
    df = dataframe.loc[:, ["YearsCode", "ConvertedCompYearly"]]   
    # elimino los sin información en el salario anual y años
    df.drop(df[df["ConvertedCompYearly"]=="Sin información"].index, inplace=True)
    df.drop(df[df["YearsCode"]=="Sin información"].index, inplace=True)
    
    # Cuando es Menor que 1 año, lo reemplazo por 0. Cuando es mayor que 50, lo cambio por 51.
    df["YearsCode"] = df["YearsCode"].str.replace("Less than 1 year", "0")
    df["YearsCode"] = df["YearsCode"].str.replace("More than 50 years", "51")
    # una vez limpiado y estandarizado los datos numericos, lo puedo pasar a float
    df = df.astype({"YearsCode":float, "ConvertedCompYearly":float})  
    
    #realizo una nueva columna con la función cut() ver pandas.pydata.org, especialmente usada para determinar rango de años, ver doc.
    df["Rango Edad"] = pd.cut(df["YearsCode"], bins=range(0, 60, 5), right=False)
    #formateo el obtejo category que me entrego, con una función anómima para el intervalo, uso el apply que recorre la columna, como un for pero para 1 col
    df["Años de experiencia"] = df["Rango Edad"].apply(lambda x: f"{int(x.left)} - {int(x.right)}")
    
    # lo paso a groupby pq sale un Warning, y con esto lo saco .. lo informé x correo, también me sale otro Warning para poner el observed=False
    df2 = df.groupby("Años de experiencia", observed=False).agg({"ConvertedCompYearly":["min","max"]})
    # Ahora con la tabla correcta, puedo hacer una tabla dinámica con los años de experiencia y montos de los sueldos, para obtener por grupos de intervalos el max y min
    #df2 = df.pivot_table(index="Años de experiencia", values="ConvertedCompYearly", observed=False, aggfunc={np.min,np.max})

    # Renombrar el nombre de las columnas
    df2.columns = ["Intervalo inferior (USD/Año)","Intervalo superior (USD/Año)" ]

    #FORMATEAR A MILES: usé la función map() que es como un for dentro del df, y la función anómima lambda, para realizar un replace()
    df2["Intervalo inferior (USD/Año)"] = df2["Intervalo inferior (USD/Año)"].map("{:,.0f}".format).apply(lambda x:x.replace(",","."))
    df2["Intervalo superior (USD/Año)"] = df2["Intervalo superior (USD/Año)"].map("{:,.0f}".format).apply(lambda x:x.replace(",","."))

    # reintegro el índice, para que los Años de experiencia sean la primera columna. 
    df2.reset_index(inplace=True)
    
    return df2


def calcular_empleabilidad(dataframe):
    # Deberás encontrar el porcentaje de empleabilidad basado en la raza y el género de los desarrolladores. 
    # columnas a usar Employment, Gender, Ethnicity
    # la raza y genero lo puse en un set, luego para ser filtrado abajo.
    raza = {"Black or of African descent","Hispanic or Latino/a/x","East Asian","I don't know","Indigenous (such as Native American, Pacific Islander, or Indigenous Australian)","Middle Eastern","White or of European descent"}
    genero =  {'Man','Non-binary','genderqueer','gender non-conforming','Woman'}
    # realizo un dataframe con tres columnas, que son las que me interesan
    df_i = dataframe.loc[:, ["Ethnicity","Gender", "Employment"]]

    # Filtro mis valores según la lista de raza y género entregada, para construir mi df a trabajar, tuve que realizarlo dentro de un dataframe sino me sale un Warning de copia
    df = pd.DataFrame(df_i[(df_i["Ethnicity"].isin(raza)) & (df_i["Gender"].isin(genero))])

    # Consulto por los valores únicos de la columna Employment y lo dejo en una lista
    # Valores_unicos_Employment = dataframe["Employment"].unique().tolist()
    # print(Valores_unicos_Employment)
    
    # le asigno un peso a cada opción de empleabilidad, si es full-time es 1, para sumar, .. trate de usar contar, y no me dejo? el ny.count
    df.loc[df["Employment"]=="Employed full-time", "Employment"] = 1
    df.loc[df["Employment"]=="Employed part-time", "Employment"] = 0.5
    df.loc[df["Employment"]=="Not employed, but looking for work", "Employment"] = 0
    
    # Agrupo por Ethnicity y Gender y cuento las ocurrencias del Employment según su peso mensionado arriba, use groupby, me da el mismo resultado con el otro indicado abajo
    df_EM = df.groupby(["Ethnicity", "Gender"]).agg({"Employment":"sum"})
    
    # realizo una tabla dinámica con col: raza y genero y los valores de Empleabilidad para que se sumen , 
    # ----- esto que está comentado, es una forma alternativa, pero me da un warning ---- dice que ahora ocupe el DataFrameGroupBy.sum
    #df_EM = df.pivot_table(index=["Ethnicity", "Gender"],values="Employment", aggfunc=np.sum)
     
    # ahora calculo el porcentaje pero a la suma de filas en total del df_i, pq quiero su comparación real al total de la muestra
    df_EM["Employment"] = df_EM["Employment"]/df_i.shape[0]*100
    
    #formateo a % 
    df_EM["Employment"] = df_EM["Employment"].map("{:.2f}%".format).apply(lambda x:x.replace(",","."))
    
    # pongos los index original, para dejarlo como título
    df_EM.reset_index(inplace=True)

    return df_EM


def graficar_ingresos_paises(dataframe):
    
    df = calcular_ingresos_por_pais(dataframe)
    df['Ingreso promedio'] = df['Ingreso promedio'].astype('float64')
    df.plot(kind="bar", x="País", y="Ingreso promedio", title="Ingresos x Países")
    plt.show()


if __name__ == "__main__":
    
    df = cargar_dataset("developers_info.csv")
    df_limpios = limpiar_dataset(df,60)
    
    df_p = calcular_ingresos_por_pais(df_limpios)
    print(df_p)
    
    df_i = calcular_ingresos_por_experiencia(df_limpios)
    print(df_i)
    
    df_e = calcular_empleabilidad(df_limpios)
    print(df_e)

    graficar_ingresos_paises(df_limpios)




    