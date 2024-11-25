from abc import ABC, abstractmethod
from typing import List
import xml.etree.ElementTree as ET


class MazeDAO(ABC):
    @abstractmethod
    def load_maze(self) -> List[List[int]]:
        """Načte bludiště z úložiště."""
        pass

    @abstractmethod
    def save_maze(self, maze: List[List[int]]) -> None:
        """Uloží bludiště do úložiště."""
        pass


class TextFileMazeDAO(MazeDAO):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_maze(self) -> List[List[int]]:
        try:
            with open(self.file_path, 'r') as file:
                return [list(map(int, line.strip())) for line in file]
        except FileNotFoundError:
            print(f"Soubor {self.file_path} neexistuje.")
            return []

    def save_maze(self, maze: List[List[int]]) -> None:
        with open(self.file_path, 'w') as file:
            for row in maze:
                file.write("".join(map(str, row)) + "\n")


class XMLFileMazeDAO(MazeDAO):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_maze(self) -> List[List[int]]:
        try:
            tree = ET.parse(self.file_path)
            root = tree.getroot()
            return [[int(cell) for cell in row.text] for row in root.findall('row')]
        except FileNotFoundError:
            print(f"Soubor {self.file_path} neexistuje.")
            return []

    def save_maze(self, maze: List[List[int]]) -> None:
        root = ET.Element('maze')
        for row in maze:
            row_elem = ET.SubElement(root, 'row')
            row_elem.text = ''.join(map(str, row))

        tree = ET.ElementTree(root)
        tree.write(self.file_path, encoding='utf-8', xml_declaration=True)
