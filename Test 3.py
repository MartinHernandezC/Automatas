import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

class AFD:
    def __init__(self):
        self.words = ["if", "else", "switch", "case", "default", "for", "while", "break", "int", "String", "double", "char", "print"]
        self.numbers = "0123456789"
        self.a_operatores = ["+", "-", "*", "/", "%"]
        self.r_operatores = ["<", "<=", ">", ">=", "==", "!="]

    def evaluate(self, array, i):
        if not array:
            return {"status": False, "key": "E", "name": "Error"}
        
        e = array[i]
        i += 1
        if e in self.words:
            return self.identificador(array, i)
        elif e in self.a_operatores:
            return self.operador_aritmetico(array, i)
        elif e in self.numbers:
            return self.numero_entero(array, i)
        elif e in self.r_operatores:
            return self.operador_relacional(array, i)
        elif e in ["{", "}"]:
            return self.llave(array, i)
        elif e in ["(", ")"]:
            return self.parentesis(array, i)
        elif e == "&":
            return self.operador_logico_and(array, i)
        elif e == "|":
            return self.operador_logico_or(array, i)
        elif e == "/":
            return self.division(array, i)
        elif e == "-":
            return self.resta(array, i)
        elif e == '"':
            return self.cadena_caracteres(array, i)
        else:
            return {"status": False, "key": "E", "name": "Error"}
    
    def identificador(self, array, i):
        while i < len(array) and (array[i].isalnum() or array[i] == '_'):
            i += 1
        return {"status": True, "key": "I", "name": "Identificador"}

    def operador_aritmetico(self, array, i):
        return {"status": True, "key": "OA", "name": "Operador Aritmetico"}

    def numero_entero(self, array, i):
        while i < len(array) and array[i] in self.numbers:
            i += 1
        if i < len(array) and array[i] == '.':
            return self.numero_decimal(array, i + 1)
        return {"status": True, "key": "NE", "name": "Numero Entero"}

    def numero_decimal(self, array, i):
        while i < len(array) and array[i] in self.numbers:
            i += 1
        return {"status": True, "key": "ND", "name": "Numero Decimal"}

    def operador_relacional(self, array, i):
        if i < len(array) and array[i] == '=':
            i += 1
        return {"status": True, "key": "OR", "name": "Operador Relacional"}

    def llave(self, array, i):
        return {"status": True, "key": "L", "name": "Llave"}

    def parentesis(self, array, i):
        return {"status": True, "key": "P", "name": "Parentesis"}

    def operador_logico_and(self, array, i):
        if i < len(array) and array[i] == '&':
            return {"status": True, "key": "OL", "name": "Operador Logico"}
        return {"status": False, "key": "E", "name": "Error"}

    def operador_logico_or(self, array, i):
        if i < len(array) and array[i] == '|':
            return {"status": True, "key": "OL", "name": "Operador Logico"}
        return {"status": False, "key": "E", "name": "Error"}

    def division(self, array, i):
        if i < len(array) and array[i] == '*':
            return self.comentario_multilinea(array, i + 1)
        elif i < len(array) and array[i] == '/':
            return self.comentario_linea(array, i + 1)
        return {"status": True, "key": "OA", "name": "Operador Aritmetico"}

    def comentario_multilinea(self, array, i):
        while i < len(array):
            if array[i] == '*' and (i + 1 < len(array) and array[i + 1] == '/'):
                return {"status": True, "key": "C", "name": "Comentario"}
            i += 1
        return {"status": False, "key": "E", "name": "Error"}

    def comentario_linea(self, array, i):
        while i < len(array) and array[i] != '\n':
            i += 1
        return {"status": True, "key": "C", "name": "Comentario"}

    def resta(self, array, i):
        if i < len(array) and array[i] in self.numbers:
            return self.numero_entero(array, i)
        return {"status": True, "key": "OA", "name": "Operador Aritmetico"}

    def cadena_caracteres(self, array, i):
        while i < len(array):
            if array[i] == '"':
                return {"status": True, "key": "Cc", "name": "Cadena de caracteres"}
            i += 1
        return {"status": False, "key": "E", "name": "Error"}

class TokenAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("Token Analyzer")
        
        self.afd = AFD()
        
        self.label = tk.Label(master, text="Token Analyzer")
        self.label.pack()
        
        self.text_area = ScrolledText(master, width=80, height=20)
        self.text_area.pack()
        
        self.load_button = tk.Button(master, text="Load File", command=self.load_file)
        self.load_button.pack()
        
        self.analyze_button = tk.Button(master, text="Analyze", command=self.analyze_file)
        self.analyze_button.pack()
        
        self.result_area = ScrolledText(master, width=80, height=20)
        self.result_area.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            
    def analyze_file(self):
        content = self.text_area.get(1.0, tk.END)
        words = content.split()
        report = {
            "PR": 0,  # Palabras reservadas
            "I": 0,   # Identificadores
            "OR": 0,  # Operadores relacionales
            "OL": 0,  # Operadores logicos
            "OA": 0,  # Operadores aritmeticos
            "A": 0,   # Asignacion
            "NE": 0,  # Numeros enteros
            "ND": 0,  # Numeros decimales
            "C": 0,   # Comentarios
            "P": 0,   # Parentesis
            "L": 0,   # Llaves
            "E": 0,   # Errores
            "Cu": 0,  # Cadena caracteres
            "Cc": 0   # Cadena caracteres
        }
        
        for word in words:
            result = self.afd.evaluate(list(word), 0)
            if result["status"]:
                report[result["key"]] += 1
            else:
                report["E"] += 1
        
        result_text = "Token Analysis Report:\n"
        for token_type, count in report.items():
            result_text += f"{token_type}: {count}\n"
        
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenAnalyzer(root)
    root.mainloop()
