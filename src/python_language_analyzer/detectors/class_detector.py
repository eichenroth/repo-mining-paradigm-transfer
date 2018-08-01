import ast

from src.python_language_analyzer.detector import Detector, Detection


class ClassDefinitionDetector(Detector):
    def __call__(self):
        return super().__call__(ClassDefinitionVisitor())


class ClassDefinitionVisitor(ast.NodeVisitor):
    def __init__(self):
        self._stack_height = 0
        self.detections = []

    def generic_visit(self, node):
        self._stack_height += 1
        super().generic_visit(node)
        self._stack_height -= 1

    def visit_ClassDef(self, node):
        name = node.name
        method_count = len([child for child in node.body if child.__class__.__name__ == 'FunctionDef'])
        nested = self._stack_height > 0

        detection = ClassDefinitionDetection(node, name=name, method_count=method_count, nested=nested)
        self.detections.append(detection)

        self.generic_visit(node)

    def visit_Module(self, node):
        super().generic_visit(node)


class ClassDefinitionDetection(Detection):
    INFO_KEYS = ['name', 'method_count', 'nested']
