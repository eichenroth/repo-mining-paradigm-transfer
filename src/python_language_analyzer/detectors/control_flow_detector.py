import ast

from src.python_language_analyzer.detection import IfDetection
from src.python_language_analyzer.detector import Detector, get_last_line


class ControlFlowDetector(Detector):
    def __call__(self):
        file_module = ast.parse(''.join(self.file))
        control_flow_visitor = ControlFlowVisitor()
        control_flow_visitor.visit(file_module)

        return control_flow_visitor.detections


class ControlFlowVisitor(ast.NodeVisitor):
    def __init__(self):
        self.detections = []
        self.visited = set()

    def generic_visit(self, node):
        super().generic_visit(node)

    def visit_If(self, node):
        if node not in self.visited:
            detection = IfDetection()
            detection.begin = node.lineno
            detection.end = get_last_line(node)
            detection['elseif_number'] = 0
            self._recursive_if_visit(node, detection)
            self.detections.append(detection)

        self.generic_visit(node)

    def _recursive_if_visit(self, node, detection):
        self.visited.add(node)

        if len(node.orelse) == 0:
            detection['has_else'] = False
        elif len(node.orelse) == 1 and node.orelse[0].__class__.__name__ == 'If':
            detection['elseif_number'] += 1
            self._recursive_if_visit(node.orelse[0], detection)
        else:
            detection['has_else'] = True
