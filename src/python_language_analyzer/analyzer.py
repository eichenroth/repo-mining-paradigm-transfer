class Analyzer:
    def __init__(self, file, detector_classes):
        """
        :param file: List of strings representing the lines of the file.
        :param detector_classes: List of detector classes that should be used.
        """
        self.file = file

        self.detectors = []
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
