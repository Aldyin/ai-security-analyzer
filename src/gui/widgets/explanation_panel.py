import tkinter as tk

from tkinter.scrolledtext import ScrolledText


class ExplanationPanel(tk.LabelFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            text="Explanation",
            font=("Arial", 12, "bold")
        )

        self.text = ScrolledText(
            self,
            height=8,
            font=("Consolas", 11),
            wrap=tk.WORD
        )

        self.text.pack(
            fill=tk.BOTH,
            expand=True,
            padx=5,
            pady=5
        )

    def set_explanation(self, explanation):

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            tk.END,
            explanation
        )