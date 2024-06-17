import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

class Automata:
    def __init__(self): #Definimos todos los tipos de caracteres
        self.keywords = ["main", "if", "else", "switch", "case", "default", "for", "while", "break", "int", "String", "double", "char", "print"]
        self.rel_operators = ["<", "<=", ">", ">=", "==", "!="]
        self.log_operators = ["&&", "||", "!"]
        self.arith_operators = ["+", "-", "*", "/", "%"]
        self.assign_operator = "="
        self.increment_operator = "++"
        self.decrement_operator = "--"
        self.parenthesis = ["(", ")"]
        self.braces = ["{", "}"]

    def is_keyword(self, word):#Función para identificar Palabrasa reservadas
        return word in self.keywords

    def is_identifier(self, word):#Identificadores
        return word[0].isalpha() and all(c.isalnum() or c == '_' for c in word)

    def is_number(self, word):#Números Enteros
        return word.isdigit()

    def is_decimal(self, word):#Números Décimales
        try:
            float(word)
            return True
        except ValueError:
            return False

    def is_string(self, word):#Strings
        return word.startswith('"') and word.endswith('"')

    def is_multiline_comment(self, word):#Comentarios Multilinea
        return word.startswith('/*') and word.endswith('*/')

    def is_line_comment(self, word):#Comentarios Normales
        return word.startswith('//')

    def identify_token(self, word):#toma una palabra y determina su tipo según las reglas anteriores. Retorna el tipo del token como un string, como "Keyword", "Identifier", "Integer", "String", etc.
        if self.is_keyword(word):
            return "Keyword"
        elif self.is_identifier(word):
            return "Identifier"
        elif word in self.rel_operators:
            return "Relational Operator"
        elif word in self.log_operators:
            return "Logical Operator"
        elif word in self.arith_operators:
            return "Arithmetic Operator"
        elif word == self.increment_operator:
            return "Increment Operator"
        elif word == self.decrement_operator:
            return "Decrement Operator"
        elif word == self.assign_operator:
            return "Assignment Operator"
        elif self.is_number(word):
            return "Integer"
        elif self.is_decimal(word):
            return "Decimal Number"
        elif self.is_string(word):
            return "String"
        elif self.is_multiline_comment(word):
            return "Multiline Comment"
        elif self.is_line_comment(word):
            return "Line Comment"
        elif word in self.parenthesis:
            return "Parenthesis"
        elif word in self.braces:
            return "Brace"
        else:
            return "Unknown Token"

class TokenAnalyzer:
    def __init__(self, master):
        self.master = master
        self.master.title("Token Analyzer")

        self.automata = Automata()

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
        with open(file_path, "r") as file:
            content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)

    def analyze_file(self):
        content = self.text_area.get(1.0, tk.END)
        tokens = self.tokenize(content)
        report = {
            "Keyword": 0,
            "Identifier": 0,
            "Relational Operator": 0,
            "Logical Operator": 0,
            "Arithmetic Operator": 0,
            "Increment Operator": 0,
            "Decrement Operator": 0,
            "Assignment Operator": 0,
            "Integer": 0,
            "Decimal Number": 0,
            "String": 0,
            "Multiline Comment": 0,
            "Line Comment": 0,
            "Parenthesis": 0,
            "Brace": 0,
            "Unknown Token": 0
        }

        for token in tokens:
            token_type = self.automata.identify_token(token)
            report[token_type] += 1

        result = "Token Analysis Report:\n"
        for token_type, count in report.items():
            result += f"{token_type}: {count}\n"

        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, result)

    def tokenize(self, content):#Analizamos caracter por caracter
        tokens = []
        current_token = ""
        i = 0
        inside_comment = False
        inside_string = False

        while i < len(content):
            char = content[i]

            if inside_comment:
                if char == '*' and i + 1 < len(content) and content[i + 1] == '/':
                    inside_comment = False
                    current_token += '*/'
                    tokens.append(current_token)
                    current_token = ""
                    i += 2
                else:
                    current_token += char
                    i += 1
                continue

            if inside_string:
                current_token += char
                if char == '"':
                    inside_string = False
                    tokens.append(current_token)
                    current_token = ""
                i += 1
                continue

            if char == '/':
                if i + 1 < len(content) and content[i + 1] == '*':
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    inside_comment = True
                    current_token = '/*'
                    i += 2
                    continue
                elif i + 1 < len(content) and content[i + 1] == '/':
                    if current_token:
                        tokens.append(current_token)
                        current_token = ""
                    while i < len(content) and content[i] != '\n':
                        current_token += content[i]
                        i += 1
                    tokens.append(current_token)
                    current_token = ""
                    continue

            if char == '"':
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                inside_string = True
                current_token = '"'
                i += 1
                continue

            if char.isspace():
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                i += 1
                continue

            if char in self.automata.parenthesis or char in self.automata.braces:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)
                i += 1
                continue

            if char == '&' and i + 1 < len(content) and content[i + 1] == '&':
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append('&&')
                i += 2
                continue

            if char == '|' and i + 1 < len(content) and content[i + 1] == '|':
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append('||')
                i += 2
                continue

            if char in self.automata.arith_operators or char == '=' or char in ['<', '>', '!', '=']:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                if char == '+' and i + 1 < len(content) and content[i + 1] == '+':
                    tokens.append('++')
                    i += 2
                    continue
                if char == '-' and i + 1 < len(content) and content[i + 1] == '-':
                    tokens.append('--')
                    i += 2
                    continue
                if char in ['<', '>', '!', '='] and i + 1 < len(content) and content[i + 1] == '=':
                    tokens.append(char + '=')
                    i += 2
                    continue
                tokens.append(char)
                i += 1
                continue

            current_token += char
            i += 1

        if current_token:
            tokens.append(current_token)

        return tokens

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenAnalyzer(root)
    root.mainloop()
