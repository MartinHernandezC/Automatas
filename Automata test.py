import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

class Automata:
    def __init__(self):
        self.keywords = ["if", "else", "switch", "case", "default", "for", "while", "break", "int", "String", "double", "char", "print"]
        self.rel_operators = ["<", "<=", ">", ">=", "==", "!="]
        self.log_operators = ["&&", "||", "!"]
        self.arith_operators = ["+", "-", "*", "/", "%"]
        self.assign_operator = "="
        self.parenthesis = ["(", ")"]
        self.braces = ["{", "}"]

    def is_keyword(self, word):
        return word in self.keywords

    def is_identifier(self, word):
        return word[0].isalpha() and all(c.isalnum() or c == '_' for c in word)

    def is_number(self, word):
        return word.isdigit()

    def is_decimal(self, word):
        try:
            float(word)
            return True
        except ValueError:
            return False

    def is_string(self, word):
        return word.startswith('"') and word.endswith('"')

    def is_multiline_comment(self, word):
        return word.startswith('/*') and word.endswith('*/')

    def is_line_comment(self, word):
        return word.startswith('//')

    def identify_token(self, word):
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
        words = content.split()
        report = {
            "Keyword": 0,
            "Identifier": 0,
            "Relational Operator": 0,
            "Logical Operator": 0,
            "Arithmetic Operator": 0,
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
        
        for word in words:
            token_type = self.automata.identify_token(word)
            report[token_type] += 1
        
        result = "Token Analysis Report:\n"
        for token_type, count in report.items():
            result += f"{token_type}: {count}\n"
        
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenAnalyzer(root)
    root.mainloop()
    
