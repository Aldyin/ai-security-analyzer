import tkinter as tk

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

from matplotlib.figure import Figure


class ProbabilityChart(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.figure = Figure(
            figsize=(5, 3),
            dpi=100
        )

        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=self
        )

        self.canvas.get_tk_widget().pack(
            fill=tk.BOTH,
            expand=True
        )

    def update_chart(self, labels, probs):

        self.ax.clear()

        self.ax.bar(
            labels,
            probs
        )

        self.ax.set_ylim(0, 100)

        self.ax.set_ylabel("Confidence %")

        self.ax.set_title(
            "Vulnerability Confidence"
        )

        self.canvas.draw()