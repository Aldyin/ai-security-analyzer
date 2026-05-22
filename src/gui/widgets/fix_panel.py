import tkinter as tk

from tkinter.scrolledtext import (
    ScrolledText
)


class FixPanel(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        tk.Label(
            self,
            text="Suggested Fix"
        ).pack(
            anchor="w"
        )

        self.text = ScrolledText(
            self,
            height=20
        )

        self.text.pack(
            fill="both",
            expand=True
        )

    def update_fix(
        self,
        fixed_code
    ):

        self.text.delete(
            "1.0",
            tk.END
        )

        self.text.insert(
            tk.END,
            fixed_code
        )