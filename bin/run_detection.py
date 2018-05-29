import argparse

from src.python_language_analyzer.analyzer import Analyzer
from src.python_language_analyzer.detectors.built_in_function_detector import BuiltInFunctionDetector
from src.python_language_analyzer.detectors.class_detector import ClassDetector
from src.python_language_analyzer.detectors.control_flow_detector import ControlFlowDetector


def detection():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, required=True, help='file path to the of the file the detection should run on')
    args = parser.parse_args()

    with open(args.file) as f:
        file = f.readlines()

    detectors = [ClassDetector, ControlFlowDetector, BuiltInFunctionDetector]
    analyzer = Analyzer(file, detectors)

    detections = analyzer()

    for d in detections:
        print('detection name: {} | begin: {} | end: {}'.format(d.DETECTION_NAME, d.begin, d.end))
        print(d.info)
        print()


if __name__ == '__main__':
    detection()
