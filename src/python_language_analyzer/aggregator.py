import json
import os

from src.python_language_analyzer.detector import Detection
from src.python_language_analyzer.detectors.built_in_function_detector import BuiltInFunctionDetection
from src.python_language_analyzer.detectors.class_detector import ClassDefinitionDetection
from src.python_language_analyzer.detectors.comprehension_detector import ComprehensionDetection, \
    ListComprehensionDetection, DictComprehensionDetection, SetComprehensionDetection
from src.python_language_analyzer.detectors.control_flow_detector import IfDetection


class Aggregator:
    def __init__(self, aggregation_levels, file_path=None):
        """
        :param aggregation_levels: Iterable of aggregation level names.
        :param save_file: File, that the aggregation should be saved in
        """
        self.aggregation_levels = tuple(aggregation_levels)
        self.file_path = file_path

        self.detections = {}

    def add_detections(self, identifier, detections):
        assert type(identifier) == tuple or type(identifier) == list
        assert len(identifier) == len(self.aggregation_levels)
        for detection in detections:
            assert issubclass(detection.__class__, Detection)

        self.detections[tuple(identifier)] = detections

    def save(self, file_path=None):
        file_path = file_path or self.file_path

        detections = [[key, [detection.serialize() for detection in detections]] for key, detections in
                      self.detections.items()]
        data = {
            'aggregation_levels': self.aggregation_levels,
            'detections': detections
        }

        dir_name = os.path.dirname(file_path)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def aggregate(self, detection_class, info, aggregation_level):
        """
        :param detection_class:
        :param info: Identifier string for an info key of the detection or function calculating the desired value.
        :param aggregation_level:
        :return:
        """
        if type(info) == str:
            assert info in detection_class.INFO_KEYS
        assert aggregation_level in self.aggregation_levels

        level_index = self.aggregation_levels.index(aggregation_level)

        aggregation_dict = {}
        for key, detections in self.detections.items():
            for detection in detections:
                if detection.__class__ != detection_class:
                    continue

                key = key[:level_index + 1]
                if key not in aggregation_dict:
                    aggregation_dict[key] = []
                if type(info) == str:
                    aggregation_dict[key].append(detection.__getattribute__(info))
                else:
                    aggregation_dict[key].append(info(detection))

        aggregation_list = [sum(l) / len(l) for l in aggregation_dict.values()]
        return aggregation_list

    def percentage(self, detection_class, aggregation_level):
        assert aggregation_level in self.aggregation_levels

        level_index = self.aggregation_levels.index(aggregation_level)

        count_dict = {}
        for key, detections in self.detections.items():
            key = key[:level_index + 1]
            if key not in count_dict:
                count_dict[key] = [0, 0]
            for detection in detections:
                count_dict[key][0] += 1
                if detection.__class__ == detection_class:
                    count_dict[key][1] += 1

        percentage_list = [l[1] / l[0] for l in count_dict.values() if l[0] > 0]
        return percentage_list

    @staticmethod
    def load(file_path):
        detection_classes = [
            Detection,
            BuiltInFunctionDetection,
            ClassDefinitionDetection,
            ComprehensionDetection,
            ListComprehensionDetection,
            DictComprehensionDetection,
            SetComprehensionDetection,
            IfDetection
        ]
        detection_classes = {d.__name__: d for d in detection_classes}

        with open(file_path, 'r') as f:
            data = json.load(f)
        aggregator = Aggregator(data['aggregation_levels'], file_path=file_path)

        for key, serialized_detections in data['detections']:
            detections = []
            for serialized_detection in serialized_detections:
                detection = detection_classes[serialized_detection['class']].deserialize(serialized_detection)
                detections.append(detection)
            aggregator.add_detections(key, detections)

        return aggregator
