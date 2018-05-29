import ast

from src.python_language_analyzer.detection import BuiltInFunctionDetection
from src.python_language_analyzer.detector import get_last_line, Detector


class BuiltInFunctionDetector(Detector):
    def __call__(self):
        file_module = ast.parse(''.join(self.file))
        built_in_function_visitor = BuiltInFunctionVisitor()
        built_in_function_visitor.visit(file_module)

        return built_in_function_visitor.detections


class BuiltInFunctionVisitor(ast.NodeVisitor):
    BUILT_IN_FUNCTIONS = ['abs', 'dict', 'help', 'min', 'setattr', 'all', 'dir', 'hex', 'next', 'slice', 'any',
                          'divmod', 'id', 'object', 'sorted', 'ascii', 'enumerate', 'input', 'oct', 'staticmethod',
                          'bin', 'eval', 'int', 'open', 'str', 'bool', 'exec', 'isinstance', 'ord', 'sum', 'bytearray',
                          'filter', 'issubclass', 'pow', 'super', 'bytes', 'float', 'iter', 'print', 'tuple',
                          'callable', 'format', 'len', 'property', 'type', 'chr', 'frozenset', 'list', 'range', 'vars',
                          'classmethod', 'getattr', 'locals', 'repr', 'zip', 'compile', 'globals', 'map', 'reversed',
                          '__import__', 'complex', 'hasattr', 'max', 'round', 'delattr', 'hash', 'memoryview', 'set', ]

    def __init__(self):
        self.detections = []

    def visit_Call(self, node):
        if hasattr(node.func, 'id') and node.func.id in self.BUILT_IN_FUNCTIONS:
            detection = BuiltInFunctionDetection()
            detection['name'] = node.func.id
            detection.begin = node.lineno
            detection.end = get_last_line(node)
            self.detections.append(detection)

        self.generic_visit(node)
