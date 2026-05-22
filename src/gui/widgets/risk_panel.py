import tkinter as tk


class RiskPanel(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.label = tk.Label(
            self,
            text="Risk: UNKNOWN",
            font=("Arial", 12, "bold")
        )

        self.label.pack(
            anchor="w"
        )

    def update_risk(
        self,
        risk
    ):

        self.label.config(
            text=f"Risk: {risk}"
        )