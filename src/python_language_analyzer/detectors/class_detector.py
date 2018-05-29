import ast

from src.python_language_analyzer.detection import ClassDetection
from src.python_language_analyzer.detector import Detector, get_last_line


class ClassDetector(Detector):
    def __call__(self):
        file_module = ast.parse(''.join(self.file))
        class_visitor = ClassVisitor()
        class_visitor.visit(file_module)

        return class_visitor.detections


class ClassVisitor(ast.NodeVisitor):
    def __init__(self):
        self._stack_height = 0
        self.detections = []

    def generic_visit(self, node):
        self._stack_height += 1
        super().generic_visit(node)
        self._stack_height -= 1

    def visit_ClassDef(self, node):
        detection = ClassDetection()
        detection.begin = node.lineno
        detection.end = get_last_line(node)
        detection['name'] = node.name
        detection['method_number'] = len([child for child in node.body if child.__class__.__name__ == 'FunctionDef'])
        detection['nested'] = self._stack_height > 0
        self.detections.append(detection)

        self.generic_visit(node)

    def visit_Module(self, node):
        super().generic_visit(node)
