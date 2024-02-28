import tkinter as tk

def ingresar_palabras(n): #Ingresamos las palabras en una lista
    palabras = [] #Inicializamos el arreglo donde se guardarán las palabras del usuario
    for i in range(n): #n es el numero de palabras que ingresa el usuario y la cantidad de veces que se itera el bucle
        palabra = input(f"Ingrese la palabra {i+1}: ") #Se solicitan y agregan
        palabras.append(palabra) #Se agregan al final de la lista
    return palabras

def prefijos(palabra):
    resultado = [palabra] # Inicializamos una lista con la palabra completa
    while palabra: # Mientras la palabra no sea vacía
        palabra = palabra[:-1] # Eliminamos la última letra de la palabra
        resultado.append(palabra) # Añadimos la palabra modificada a la lista
    return resultado

def sufijos(palabra):
    resultado = [palabra] 
    while palabra: 
        palabra = palabra[1:] # Eliminamos la primera letra de la palabra
        resultado.append(palabra)
    return resultado

def interseccion(l1, l2): #Convertimos listas en conjuntos con set y utilizamos & para regresar una lista con el resultado
    return list(set(l1) & set(l2))

def diferencia(l1, l2):
    return list(set(l1) - set(l2))

def concatenacion(l1, l2):#Utilizando comprensión de lista iteramos por cada elemento de l1 y l2 a la vez que concatenamos
    return [palabra1 + palabra2 for palabra1 in l1 for palabra2 in l2]

def calcular(event=None): #Eventos 
    l1 = l1_int.get().split()
    l2 = l2_int.get().split()
    opcion = opcion_var.get()
    if opcion == "Intersección":
        resultado = interseccion(l1, l2)
    elif opcion == "Diferencia":
        resultado = diferencia(l1, l2)
    elif opcion == "Concatenación":
        resultado = concatenacion(l1, l2)    
    elif opcion == "Prefijos": 
        if len(l1) == 1: # Se verifica que el usuario haya ingresado una sola palabra en l1
            resultado = prefijos(l1[0]) # Llamamos a la función prefijos con la palabra ingresada
        else: # Si el usuario ingresó más de una palabra en l1
            resultado = "Error: Debes ingresar una sola palabra en el Lenguaje 1 para calcular los prefijos." 
    elif opcion == "Sufijos": 
        if len(l1) == 1: 
            resultado = sufijos(l1[0])
        else:
            resultado = "Error: Debes ingresar una sola palabra en el Lenguaje 1 para calcular los sufijos."         
    else:
        resultado = "Opción inválida"
    resultado_T.config(text=f"El resultado es: {resultado}")

window = tk.Tk() #Creamos la ventana
window.title("20110340 Hernández Camarena Martín Ulises")


titulo = tk.Label(window, text="Operaciones de lenguaje", font=("Arial", 16)) #Ponemos Titulo dentro de ella
titulo.grid(row=0, column=0, columnspan=2, pady=10)

l1_T = tk.Label(window, text="Ingresa las palabras del Lenguaje 1: (Separadas por espacios)")
l1_T.grid(row=1, column=0, sticky="w", padx=10)
l1_int = tk.Entry(window) #Caja de texto para el primer Lenguaje
l1_int.grid(row=1, column=1, sticky="ew", padx=10)

l2_T = tk.Label(window, text="Ingresa las palabras del Lenguaje 2: (Separadas por espacios)")
l2_T.grid(row=2, column=0, sticky="w", padx=10)
l2_int = tk.Entry(window) #Caja de texto del segundo Lenguaje
l2_int.grid(row=2, column=1, sticky="ew", padx=10)

opcion_T = tk.Label(window, text="Elige una opción:")
opcion_T.grid(row=3, column=0, sticky="w", padx=10)
opcion_var = tk.StringVar(window)
opcion_menu = tk.OptionMenu(window, opcion_var, "Intersección", "Diferencia", "Concatenación", "Sufijos", "Prefijos") #Menu opciones
opcion_menu.grid(row=3, column=1, sticky="ew", padx=10)

calcular_btn = tk.Button(window, text="Calcular", command=calcular)
calcular_btn.grid(row=4, column=0, columnspan=2, pady=10)

resultado_T = tk.Label(window, text="El resultado es:")
resultado_T.grid(row=5, column=0, columnspan=2, pady=10)

window.mainloop()
