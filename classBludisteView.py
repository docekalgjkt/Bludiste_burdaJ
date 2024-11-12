import tkinter as tk
from typing import List, Tuple

class BludisteView:
    def __init__(self, bludiste: Bludiste, rozmerPolicka: int = 40, padding: int = 10):
        self.bludiste = bludiste
        self.rozmerPolicka = rozmerPolicka
        self.padding = padding

    def vykresli(self, canvas: tk.Canvas):
        """Vykreslí bludiště na canvas."""
        for i in range(self.bludiste.getVyska()):
            for j in range(self.bludiste.getSirka()):
                x1 = self.padding + j * self.rozmerPolicka
                y1 = self.padding + i * self.rozmerPolicka
                x2 = x1 + self.rozmerPolicka
                y2 = y1 + self.rozmerPolicka
                if self.bludiste.bludiste[i][j] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")