import tkinter as tk

from tkinter.scrolledtext import ScrolledText


class CodeEditor(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.label = tk.Label(
            self,
            text="Code Editor",
            font=("Arial", 14, "bold")
        )

        self.label.pack(
            anchor="w",
            padx=5,
            pady=5
        )

        self.text = ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Consolas", 12)
        )

        self.text.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

    def get_code(self):

        return self.text.get(
            "1.0",
            tk.END
        )

    def set_code(self, code: str):

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            tk.END,
            code
        )

    def clear(self):

        self.text.delete(
            "1.0",
            tk.END
        )