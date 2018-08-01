import ast

from src.python_language_analyzer.detector import Detector, Detection


class ControlFlowDetector(Detector):
    def __call__(self):
        return super().__call__(ControlFlowVisitor())


class ControlFlowVisitor(ast.NodeVisitor):
    def __init__(self):
        self.detections = []
        self.visited = set()

    def generic_visit(self, node):
        super().generic_visit(node)

    def visit_If(self, node):
        if node not in self.visited:
            detection = IfDetection(node, elseif_count=0, has_else=False)
            self._recursive_if_visit(node, detection)
            self.detections.append(detection)

        self.generic_visit(node)

    def _recursive_if_visit(self, node, detection):
        self.visited.add(node)

        if len(node.orelse) == 1 and node.orelse[0].__class__.__name__ == 'If':
            detection.elseif_count += 1
        elif len(node.orelse) != 0:
            detection.has_else = True


class IfDetection(Detection):
    INFO_KEYS = ['has_else', 'elseif_count']
