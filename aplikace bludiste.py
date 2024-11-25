class BludisteApp:
    def __init__(self, root: tk.Tk, dao: MazeDAO):
        self.dao = dao
        self.bludiste_data = self.dao.load_maze()

        if not self.bludiste_data:
            print("Bludiště nebylo načteno, použijeme výchozí data.")
            self.bludiste_data = [[1, 0, 1], [1, 0, 1], [1, 1, 1]]

        self.canvas = tk.Canvas(root, width=len(self.bludiste_data[0]) * 40 + 20,
                                height=len(self.bludiste_data) * 40 + 20)
        self.canvas.pack()
        self.bludiste = Bludiste(self.bludiste_data)
        self.bludisteView = BludisteView(self.bludiste)

    def spustit(self):
        self.bludisteView.vykresli(self.canvas)

    def ulozit_bludiste(self):
        self.dao.save_maze(self.bludiste_data)
