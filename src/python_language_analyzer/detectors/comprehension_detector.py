import ast

from src.python_language_analyzer.detector import Detector, Detection


class ComprehensionDetector(Detector):
    def __call__(self):
        return super().__call__(ComprehensionVisitor())


class ComprehensionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.detections = []

    def generic_visit(self, node):
        super().generic_visit(node)

    def visit_ListComp(self, node):
        detection = ListComprehensionDetection(node, generator_count=len(node.generators))
        self.detections.append(detection)

    def visit_DictComp(self, node):
        detection = DictComprehensionDetection(node, generator_count=len(node.generators))
        self.detections.append(detection)

    def visit_SetComp(self, node):
        detection = SetComprehensionDetection(node, generator_count=len(node.generators))
        self.detections.append(detection)


class ComprehensionDetection(Detection):
    INFO_KEYS = ['generator_count']


class ListComprehensionDetection(ComprehensionDetection):
    pass


class DictComprehensionDetection(ComprehensionDetection):
    pass


class SetComprehensionDetection(ComprehensionDetection):
    pass
