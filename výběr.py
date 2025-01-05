import tkinter as tk
from tkinter import simpledialog, messagebox
from typing import List, Tuple


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


class Robot:
    def __init__(self, bludiste: Bludiste, start_x: int, start_y: int):
        self.bludiste = bludiste
        self.pozice = (start_x, start_y)
        self.cesta = []

    def get_pozice(self) -> Tuple[int, int]:
        return self.pozice

    def posun_na(self, x: int, y: int):
        """Posune robota na novou pozici."""
        self.pozice = (x, y)

    def hledat_cestu(self):
        """Hledá cestu k cíli pomocí DFS."""
        self.cesta = []
        self._dfs(self.pozice[0], self.pozice[1], set())
        return self.cesta

    def _dfs(self, x: int, y: int, navstivene: set) -> bool:
        if (x, y) in navstivene:
            return False
        navstivene.add((x, y))
        self.cesta.append((x, y))

        if self.bludiste.je_vychod(x, y):
            return True

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if self.bludiste.je_volno(nx, ny) and self._dfs(nx, ny, navstivene):
                return True

        self.cesta.pop()  # Pokud není cesta, odstraň z cesty
        return False


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


class RobotView:
    def __init__(self, robot: Robot, canvas: tk.Canvas, rozmer_policka: int = 40):
        self.robot = robot
        self.canvas = canvas
        self.rozmer_policka = rozmer_policka
        self.sprite = None
        self.vykresli()

    def vykresli(self):
        """Vykreslí robota na aktuální pozici."""
        x, y = self.robot.get_pozice()
        x1 = x * self.rozmer_policka + 10
        y1 = y * self.rozmer_policka + 10
        x2 = x1 + 20
        y2 = y1 + 20
        if not self.sprite:
            self.sprite = self.canvas.create_oval(x1, y1, x2, y2, fill="blue")
        else:
            self.canvas.coords(self.sprite, x1, y1, x2, y2)


# === APP ===
class BludisteApp:
    def __init__(self, root: tk.Tk, bludiste: List[List[int]]):
        self.bludiste = Bludiste(bludiste)
        sirka, vyska = self.bludiste.get_rozmery()

        self.canvas = tk.Canvas(root, width=sirka * 40, height=vyska * 40)
        self.canvas.pack()

        self.bludiste_view = BludisteView(self.bludiste, self.canvas)
        self.bludiste_view.vykresli()

        self.robot = Robot(self.bludiste, 19, 16)  # Startovní pozice robota
        self.robot_view = RobotView(self.robot, self.canvas)

        self.start_hledani()

    def start_hledani(self):
        """Spustí hledání cesty a postupné vykreslování pohybu robota."""
        self.robot.hledat_cestu()
        self.pohybuj(0)

    def pohybuj(self, index: int):
        """Postupně posunuje robota podle nalezené cesty."""
        if index < len(self.robot.cesta):
            x, y = self.robot.cesta[index]
            self.robot.posun_na(x, y)
            self.robot_view.vykresli()
            self.canvas.after(200, lambda: self.pohybuj(index + 1))  # Prodleva mezi kroky
        elif index == len(self.robot.cesta):  # Robot dosáhl cíle
            messagebox.showinfo("Cíl dosažen", "Ugabuga!!!")


# === MAIN ===
if __name__ == "__main__":
    # Předdefinovaná bludiště
    bludiste1 = [
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

    bludiste2 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 2, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    bludiste3 = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 2, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    bludiste_volby = [bludiste1, bludiste2, bludiste3]

    def vyber_bludiste():
        """Zobrazí dialogové okno pro výběr bludiště."""
        volba = simpledialog.askinteger(
            "Výběr bludiště",
            "Vyberte bludiště (1-3):",
            minvalue=1,
            maxvalue=len(bludiste_volby),
        )
        if volba is None:
            root.destroy()  # Zavřít aplikaci, pokud uživatel stornuje výběr
            return None
        return bludiste_volby[volba - 1]

    root = tk.Tk()
    root.title("Bludiště s robotem")
    vybrane_bludiste = vyber_bludiste()

    if vybrane_bludiste:
        app = BludisteApp(root, vybrane_bludiste)
        root.mainloop()
