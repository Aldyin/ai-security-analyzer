import tkinter as tk

from tkinter.scrolledtext import (
    ScrolledText
)


class ExplanationPanel(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        tk.Label(
            self,
            text="Explanation"
        ).pack(
            anchor="w"
        )

        self.text = ScrolledText(
            self,
            height=10
        )

        self.text.pack(
            fill="both",
            expand=True
        )

    def update_explanation(
        self,
        explanation
    ):

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            tk.END,
            explanation
        )