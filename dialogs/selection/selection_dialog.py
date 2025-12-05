#!/usr/bin/python3
"""Dialog to make a selection"""

import tkinter as tk

from tkinter import simpledialog, ttk

from libraries.constants.constants import Constants


class SelectionDialog(simpledialog.Dialog):
    """Dialog to make a selectio"""

    def __init__(
        self,
        parent,
        title,
        message,
        values
    ):
        self.message = message
        self.values = values
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        """Define the body"""

        # Crée un frame horizontal
        container = ttk.Frame(master)
        container.pack(
            padx=Constants.UI_PAD_BIG,
            pady=Constants.UI_PAD_BIG,
            fill=tk.X
        )

        # Label à gauche
        label = ttk.Label(container, text=self.message)
        label.pack(
            side=tk.LEFT
        )

        # Combobox à droite
        self.combo = ttk.Combobox(
            container, values=self.values, state="readonly")
        self.combo.current(0)
        self.combo.pack(
            side=tk.LEFT,
            padx=Constants.UI_PAD_SMALL,
            fill=tk.X,
            expand=True
        )

        return self.combo  # focus

    def apply(self):
        self.result = self.combo.get()
