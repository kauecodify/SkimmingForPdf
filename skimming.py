import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader

class TextSkimmerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Skimming em Textos")

        self.text_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 12))
        self.text_box.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.word_listbox = tk.Listbox(root, height=8, font=("Arial", 12))
        self.word_listbox.pack(fill=tk.BOTH, padx=10, pady=5)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        tk.Button(self.button_frame, text="Carregar PDF", command=self.load_pdf).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Destacar Palavras", command=self.highlight_words).pack(side=tk.LEFT, padx=5)

        self.text_box.bind("<Return>", self.add_selected_word)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if file_path:
            try:
                reader = PdfReader(file_path)
                text = "\n".join(page.extract_text() for page in reader.pages)
                self.text_box.delete("1.0", tk.END)
                self.text_box.insert(tk.END, text)
                messagebox.showinfo("Sucesso", "PDF carregado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível carregar o PDF: {e}")

    def add_selected_word(self, event=None):
        try:
            word = self.text_box.selection_get().strip()
            if word and word not in self.word_listbox.get(0, tk.END):
                self.word_listbox.insert(tk.END, word)
            else:
                messagebox.showinfo("Aviso", "Palavra já adicionada ou não selecionada.")
        except tk.TclError:
            messagebox.showwarning("Nenhuma Seleção", "Selecione uma palavra antes de pressionar Enter.")
        return "break"

    def highlight_words(self):
        self.text_box.tag_remove("highlight", "1.0", tk.END)
        words = self.word_listbox.get(0, tk.END)

        for word in words:
            start = "1.0"
            while True:
                start = self.text_box.search(word, start, stopindex=tk.END, nocase=False)
                if not start:
                    break
                end = f"{start}+{len(word)}c"
                self.text_box.tag_add("highlight", start, end)
                start = end

        self.text_box.tag_config("highlight", background="yellow", foreground="black")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TextSkimmerApp(root)
    app.run()
