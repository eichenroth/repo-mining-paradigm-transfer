import ast
from abc import ABC, abstractmethod


class Detector(ABC):
    def __init__(self, file):
        """
        :param file: List of strings representing the lines of the file.
        """
        self.file = file

    @abstractmethod
    def __call__(self):
        ...


def get_last_line(node):
    lines = [n.lineno for n in ast.walk(node) if isinstance(n, ast.AST) and hasattr(n, 'lineno')]
    return max(lines)
