import tkinter as tk
from typing import List, Tuple

class Bludiste:
    def __init__(self, bludiste: List[List[int]]):
        self.bludiste = bludiste

    def jeVolno(self, souradnice: Tuple[int, int]) -> bool:
        """Kontroluje, zda je na souřadnicích volno (0)."""
        x, y = souradnice
        return self.bludiste[y][x] == 0

    def getSirka(self) -> int:
        """Vrací šířku bludiště (počet sloupců)."""
        return len(self.bludiste[0])

    def getVyska(self) -> int:
        """Vrací výšku bludiště (počet řádků)."""
        return len(self.bludiste)

    def getRozmery(self) -> Tuple[int, int]:
        """Vrací rozměry bludiště (šířka, výška)."""
        return self.getSirka(), self.getVyska()

    def jeVychod(self, souradnice: Tuple[int, int]) -> bool:
        """Kontroluje, zda jsou souřadnice na východu bludiště."""
        x, y = souradnice
        return y == len(self.bludiste) - 1 and x == len(self.bludiste[0]) - 3
