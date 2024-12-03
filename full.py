import tkinter as tk
from typing import List, Tuple
from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET


# === MODEL ===
class Bludiste:
    def __init__(self, bludiste: List[List[int]]):
        self.bludiste = bludiste

    def je_volno(self, x: int, y: int) -> bool:
        return 0 <= y < len(self.bludiste) and 0 <= x < len(self.bludiste[0]) and self.bludiste[y][x] in (0, 2)

    def get_rozmery(self) -> Tuple[int, int]:
        return len(self.bludiste[0]), len(self.bludiste)

    def je_vychod(self, x: int, y: int) -> bool:
        return self.bludiste[y][x] == 2


# === VIEW ===
class BludisteView:
    def __init__(self, bludiste: Bludiste, canvas: tk.Canvas, rozmer_policka: int = 40):
        self.bludiste = bludiste
        self.canvas = canvas
        self.rozmer_policka = rozmer_policka

    def vykresli(self):
        for y, radek in enumerate(self.bludiste.bludiste):
            for x, hodnota in enumerate(radek):
                x1 = x * self.rozmer_policka
                y1 = y * self.rozmer_policka
                x2 = x1 + self.rozmer_policka
                y2 = y1 + self.rozmer_policka
                if hodnota == 1:
                    barva = "green"
                elif hodnota == 2:
                    barva = "powder blue"
                else:
                    barva = "brown"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=barva, outline="black")


# === APP ===
class BludisteApp:
    def __init__(self, root: tk.Tk, bludiste: List[List[int]]):
        self.bludiste = Bludiste(bludiste)
        sirka, vyska = self.bludiste.get_rozmery()

        self.canvas = tk.Canvas(root, width=sirka * 40, height=vyska * 40)
        self.canvas.pack()

        self.bludiste_view = BludisteView(self.bludiste, self.canvas)
        self.bludiste_view.vykresli()

        self.hraci_pozice = [7, 14]
        self.hraci_objekt = self.canvas.create_oval(10, 10, 30, 30, fill="violet red")
        self.presun_hrace()

        root.bind("<Up>", lambda e: self.posun_hrace(0, -1))
        root.bind("<Down>", lambda e: self.posun_hrace(0, 1))
        root.bind("<Left>", lambda e: self.posun_hrace(-1, 0))
        root.bind("<Right>", lambda e: self.posun_hrace(1, 0))

    def presun_hrace(self):
        x, y = self.hraci_pozice
        x1 = x * 40 + 10
        y1 = y * 40 + 10
        x2 = x1 + 20
        y2 = y1 + 20
        self.canvas.coords(self.hraci_objekt, x1, y1, x2, y2)

    def posun_hrace(self, dx: int, dy: int):
        x, y = self.hraci_pozice
        nx, ny = x + dx, y + dy
        if self.bludiste.je_volno(nx, ny):
            self.hraci_pozice = [nx, ny]
            self.presun_hrace()
            if self.bludiste.je_vychod(nx, ny):
                print("Úspěšně jste dokončili bludiště!")
                self.zobraz_zpravu("Úspěch!", "Úspěšně jste dokončili bludiště!")

    def zobraz_zpravu(self, titulek: str, zprava: str):
        win = tk.Toplevel()
        win.title(titulek)
        tk.Label(win, text=zprava, padx=20, pady=10).pack()
        tk.Button(win, text="OK", command=win.destroy).pack()


# === MAIN ===
if __name__ == "__main__":
    bludiste_data = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 2],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    root = tk.Tk()
    root.title("Bludiště")
    app = BludisteApp(root, bludiste_data)
    root.mainloop()
