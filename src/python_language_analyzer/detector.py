import ast
from abc import ABC


class Detector(ABC):
    def __init__(self, file):
        """
        :param file: File content string.
        """
        self.file = file

    def __call__(self, visitor):
        try:
            file_module = ast.parse(self.file)
            visitor.visit(file_module)
            return visitor.detections
        except (SyntaxError, TypeError) as e:
            raise UnparsableError()

    @staticmethod
    def get_last_line(node):
        lines = [n.lineno for n in ast.walk(node) if isinstance(n, ast.AST) and hasattr(n, 'lineno')]
        return max(lines)


class UnparsableError(ValueError):
    pass


class Detection:
    INFO_KEYS = []

    def __init__(self, node, **kwargs):
        """
        :param node: The node that the detector detected.
        :param kwargs: Arguments that are required per subclass and defined by self.INFO_KEYS.
        """
        self.begin = node.lineno
        self.end = Detector.get_last_line(node)

        for key in self.INFO_KEYS:
            assert key in kwargs
            self.__setattr__(key, kwargs[key])

    def serialize(self):
        result = {key: self.__getattribute__(key) for key in self.INFO_KEYS}
        result['class'] = self.__class__.__name__
        result['begin'] = self.begin
        result['end'] = self.end
        return result

    @classmethod
    def deserialize(cls, serialized_detection):
        instance = cls.__new__(cls)
        instance.begin = serialized_detection['begin']
        instance.end = serialized_detection['end']

        for key in instance.INFO_KEYS:
            assert key in serialized_detection
            instance.__setattr__(key, serialized_detection[key])

        return instance
