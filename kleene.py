import tkinter as tk

def kleene(conjunto, nivel): #Recibimos como parametros conjunto de palabras y nivel (Potencia)
    if nivel == 0:
        return {"λ"}
    elif nivel == 1:
        return conjunto.copy()
    else:
        cerradura_nivel_anterior = kleene(conjunto, nivel - 1) #obtenemos la cerradura de Kleene del nivel anterior
        resultado = set()  # Inicializamos un conjunto vacío que contendrá el nivel actual
        for cadena in cerradura_nivel_anterior:  # Iteramos sobre la cerradura del nivel anterior
            for cadena_anterior in conjunto: 
                resultado.add(cadena + cadena_anterior) #Producto Cartesiano entre niveles
        return resultado

def calcular(): #Obtenemos datos y validamos
    num_palabras = num_entry.get()
    palabras = palabras_entry.get()
    nivel = nivel_entry.get()
    try:
        num_palabras = int(num_palabras) #Intentamos convertir el numero de palabras a un entero positivo
        if num_palabras <= 0:
            raise ValueError("El número de palabras debe ser un entero positivo.")
    except ValueError as e:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "Error: " + str(e))
        return
    palabras = palabras.split() #Dividimos utilizando split, si no coincide la cantidad con el numero mostramos mensaje
    if len(palabras) != num_palabras:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "Error: El número de palabras no coincide con las palabras ingresadas.")
        return
    for palabra in palabras: #Validamos que cada palabra sea una cadena de caracteres
        if not isinstance(palabra, str):
            resultado_text.delete(1.0, tk.END)
            resultado_text.insert(tk.END, "Error: La palabra debe ser una cadena válida.")
            return
    conjunto = set(palabras)
    try:
        nivel = int(nivel) #intentamos convertir el nivel de cerradura (nivel) a un entero.
        if nivel < 0:
            raise ValueError("El nivel de cerradura debe ser un entero no negativo.")
    except ValueError as e:
        resultado_text.delete(1.0, tk.END)
        resultado_text.insert(tk.END, "Error: " + str(e))
        return
    cerradura = kleene(conjunto, nivel) #Llamamos y guardamos la función con el conjunto de palabras y el nivel de cerradura especificados para calcular la cerradura de Kleene.
    resultado_text.delete(1.0, tk.END) #Limpiamos cuando se calcula algo más
    resultado_text.insert(tk.END, "\n".join(cerradura) + f"\n(Cantidad de palabras: {len(cerradura)})") 

window = tk.Tk()#Creamos la ventana
window.title("20110340 Cerradura de Kleene")
window.geometry("1000x500")  # Definimos el tamaño de la ventana

#Titulos/Etiquetas
num_label = tk.Label(window, text="¿Cuántas palabras tiene el lenguaje?")
num_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

palabras_label = tk.Label(window, text="Ingresa las palabras del lenguaje (Separadas por espacios)")
palabras_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=10)

nivel_label = tk.Label(window, text="¿Qué nivel de cerradura de Kleene deseas conocer?")
nivel_label.grid(row=2, column=0, sticky=tk.W, padx=10, pady=10)

resultado_label = tk.Label(window, text="Resultado:")
resultado_label.grid(row=3, column=0, sticky=tk.W, padx=10, pady=10)

#Entradas de texto
num_entry = tk.Entry(window)
num_entry.grid(row=0, column=1, sticky=tk.E, padx=250, pady=10)

palabras_entry = tk.Entry(window)
palabras_entry.grid(row=1, column=1, sticky=tk.E, padx=250, pady=10)

nivel_entry = tk.Entry(window)
nivel_entry.grid(row=2, column=1, sticky=tk.E, padx=250, pady=10)

resultado_text = tk.Text(window, height=10, width=40) 
resultado_text.grid(row=3, column=1, sticky=tk.E, padx=250, pady=10)  

#Botón
boton = tk.Button(window, text="Calcular", command=calcular)
boton.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

#Mantenemos la ventana corriendo
window.mainloop()
