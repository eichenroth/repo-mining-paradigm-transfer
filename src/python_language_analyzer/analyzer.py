from src.python_language_analyzer.detectors.built_in_function_detector import BuiltInFunctionDetector
from src.python_language_analyzer.detectors.class_detector import ClassDefinitionDetector
from src.python_language_analyzer.detectors.comprehension_detector import ComprehensionDetector
from src.python_language_analyzer.detectors.control_flow_detector import ControlFlowDetector


class Analyzer:
    def __init__(self, file, detector_classes=None):
        """
        :param file: List of strings representing the lines of the file or whole file as string.
        :param detector_classes: List of detector classes that should be used.
        """
        if type(file) is str:
            self.file = file
        elif type(file) is list:
            self.file = ''.join(file)
        else:
            raise ValueError('File needs to be list of lines or string.')

        self.detectors = []
        if detector_classes is None:
            self.detectors.append(BuiltInFunctionDetector(self.file))
            self.detectors.append(ClassDefinitionDetector(self.file))
            self.detectors.append(ControlFlowDetector(self.file))
            self.detectors.append(ComprehensionDetector(self.file))
        else:
            for detector_class in detector_classes:
                self.detectors.append(detector_class(self.file))

        self._metrics()
        self.detections = []

    def _metrics(self):
        self.loc = 0
        for line in self.file:
            if line != '\n':
                self.loc += 1

    def __call__(self):
        """
        Runs all detectors on the file. Creates a list of detection objects.
        :return: List of detection objects.
        """
        for detector in self.detectors:
            self.detections.extend(detector())
        return self.detections
