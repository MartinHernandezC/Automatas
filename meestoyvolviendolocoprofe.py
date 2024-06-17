import tkinter as tk
from tkinter import filedialog, scrolledtext

class AFD:
    def __init__(self):
        self.transitions = {
            1: {'w': 12, 'e': 15, 'other': 1},
            12: {'w': 12, 'e': 135, 'other': 1},
            135: {'w': 12, 'e': 15, 'b': 146, 'other': 1},
            146: {'w': 12, 'e': 15, 'a': 17, 'other': 1},
            15: {'b': 16, 'w': 12, 'e': 15, 'other': 1},
            16: {'a': 17, 'w': 12, 'e': 15, 'other': 1},
            17: {'y': 18, 'w': 12, 'e': 15, 'other': 1},
            18: {'w': 12, 'e': 15, 'other': 1},
        }
        self.accept_states = {146, 18}
        self.reset()

    def reset(self):
        self.current_state = 1
        self.web_count = 0
        self.ebay_count = 0
        self.potential_web = False
        self.following_chars = ''  # Cadena para rastrear los caracteres siguientes después de "web"

    def process(self, char):
        char = char.lower()
        if char in self.transitions[self.current_state]:
            if self.current_state == 135 and char == 'b':
                self.potential_web = True  # Se activa si se detecta "web"
            if self.potential_web:
                self.following_chars += char  # Agregar el caracter actual a la cadena de seguimiento
            self.current_state = self.transitions[self.current_state][char]
        else:
            self.current_state = self.transitions[self.current_state]['other']
            if not self.potential_web:
                self.following_chars = ''  # Restablecer si no estamos en una secuencia de "web"
        self.check_state(char)  # Llamar a check_state con el argumento 'char'

    def check_state(self, char):
        if self.current_state == 146:
            if 'a' in self.following_chars or 'ay' in self.following_chars:  # Si 'a' o 'ay' sigue a "web", es "webay"
                self.web_count += 1
                self.ebay_count += 1
                self.following_chars = ''
            else:
                # Incrementar solo 'web' si no se sigue de 'a' o 'ay'
                self.web_count += 1
            self.potential_web = False
            self.current_state = 1  # Reset after recognizing "web"
        elif self.current_state == 18:
            # Incrementar solo 'ebay' si no se ha detectado previamente "web"
            if not self.potential_web:
                self.ebay_count += 1
            self.current_state = 1  # Reset after recognizing "ebay"
        else:
            # Restablecer la cadena de seguimiento si no estamos en una secuencia de "webay"
            if not (self.current_state == 135 and char == 'b'):
                self.following_chars = ''

class TokenAnalyzerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Token Analyzer")

        self.afd = AFD()

        self.label = tk.Label(master, text="Token Analyzer")
        self.label.pack()

        self.text_area = scrolledtext.ScrolledText(master, width=80, height=20)
        self.text_area.pack()

        self.load_button = tk.Button(master, text="Load File", command=self.load_file)
        self.load_button.pack()

        self.analyze_button = tk.Button(master, text="Analyze", command=self.analyze_file)
        self.analyze_button.pack()

        self.result_area = scrolledtext.ScrolledText(master, width=80, height=20)
        self.result_area.pack()

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)

    def analyze_file(self):
        content = self.text_area.get(1.0, tk.END).strip()
        self.afd.reset()

        for char in content:
            self.afd.process(char)

        result = f"Token Analysis Report:\nWeb: {self.afd.web_count}\nEbay: {self.afd.ebay_count}"
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = TokenAnalyzerApp(root)
    root.mainloop()
