if __name__ == "__main__":
    root = tk.Tk()
    root.title("Bludiště v Tkinteru")

    # Vyberte DAO implementaci (textový nebo XML soubor)
    # dao = TextFileMazeDAO("mazes.txt")
    dao = XMLFileMazeDAO("mazes.xml")

    app = BludisteApp(root, dao)
    app.spustit()

    # Při zavření aplikace se uloží bludiště
    root.protocol("WM_DELETE_WINDOW", lambda: [app.ulozit_bludiste(), root.destroy()])
    root.mainloop()
