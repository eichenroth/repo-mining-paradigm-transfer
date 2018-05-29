class Detection:
    DETECTION_NAME = 'generic'

    def __init__(self):
        self.begin = None
        self.end = None
        self.info = {}

    def __setitem__(self, key, value):
        self.info[key] = value

    def __getitem__(self, item):
        return self.info[item]


class ClassDetection(Detection):
    DETECTION_NAME = 'class'


class FunctionDetection(Detection):
    DETECTION_NAME = 'function'


class BuiltInFunctionDetection(Detection):
    DETECTION_NAME = 'built_in_function'


class IfDetection(Detection):
    DETECTION_NAME = 'if'
