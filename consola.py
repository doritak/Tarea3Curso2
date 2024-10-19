from consultas import cargar_dataset

# df = cargar_dataset('developers_info.csv')

def cargar_menu():
    print('Para continuar ingrese el número equivalente a la consulta:')
    print('¡Hola, bienvenido/a!')
    print('[1] Limpieza de datos')
    print('[2] Calcular ingresos por país')
    print('[3] Calcular ingresos por experiencia')
    print('[4] Calcular empleabilidad')
    print('[5] Graficar ingresos paises')
    print('[6] Salir')

def ingresar_seleccion():
    cargar_menu()
    Opcion = [1,2,3,4,5,6]
    while True:
        try:
            sel = int(input("Ingrese aquí:"))
            
        except ValueError as e:
            print("Favor ingresar un número sólo un número."),
            cargar_menu()
        else:
            if sel in Opcion: 
                return sel
            else: 
                print("Valor incorrecto.")
                cargar_menu()


if __name__== "__main__":
    numero = ingresar_seleccion()
    print(f"Número seleccionado fue el {numero}")
    