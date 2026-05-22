import tkinter as tk
from tkinter import scrolledtext


class LogPanel:
    def __init__(self, parent):
        self.text = scrolledtext.ScrolledText(parent, bg="#000", fg="#00ff88")

    def write(self, msg):
        self.text.insert(tk.END, msg + "\n")
        self.text.see(tk.END)