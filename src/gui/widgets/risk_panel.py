import tkinter as tk


class RiskPanel(tk.Frame):

    COLORS = {
        "LOW": "#4CAF50",
        "MEDIUM": "#FFC107",
        "HIGH": "#FF5722",
        "CRITICAL": "#F44336",
        "UNKNOWN": "#9E9E9E"
    }

    def __init__(self, parent):
        super().__init__(parent)

        self.title = tk.Label(
            self,
            text="Risk Level",
            font=("Arial", 14, "bold")
        )

        self.title.pack(anchor="w", padx=5, pady=5)

        self.risk_label = tk.Label(
            self,
            text="UNKNOWN",
            font=("Arial", 18, "bold"),
            width=20,
            height=2
        )

        self.risk_label.pack(
            fill=tk.X,
            padx=5,
            pady=5
        )

    def set_risk(self, risk: str):

        color = self.COLORS.get(
            risk,
            "#9E9E9E"
        )

        self.risk_label.config(
            text=risk,
            bg=color,
            fg="white"
        )