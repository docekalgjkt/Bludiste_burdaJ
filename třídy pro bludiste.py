import tkinter as tk
from typing import List, Tuple


class Bludiste:
    def __init__(self, bludiste: List[List[int]]):
        self.bludiste = bludiste

    def jeVolno(self, souradnice: Tuple[int, int]) -> bool:
        x, y = souradnice
        return self.bludiste[y][x] == 0

    def getSirka(self) -> int:
        return len(self.bludiste[0])

    def getVyska(self) -> int:
        return len(self.bludiste)

    def getRozmery(self) -> Tuple[int, int]:
        return self.getSirka(), self.getVyska()

    def jeVychod(self, souradnice: Tuple[int, int]) -> bool:
        x, y = souradnice
        return y == len(self.bludiste) - 1 and x == len(self.bludiste[0]) - 3


class BludisteView:
    def __init__(self, bludiste: Bludiste, rozmerPolicka: int = 40, padding: int = 10):
        self.bludiste = bludiste
        self.rozmerPolicka = rozmerPolicka
        self.padding = padding

    def vykresli(self, canvas: tk.Canvas):
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
