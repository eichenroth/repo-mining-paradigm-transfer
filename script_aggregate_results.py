import matplotlib
matplotlib.use('agg')

from src.github.plotter import Plotter
from src.python_language_analyzer.aggregator import Aggregator
from src.python_language_analyzer.detectors.built_in_function_detector import BuiltInFunctionDetection
from src.python_language_analyzer.detectors.class_detector import ClassDefinitionDetection
from src.python_language_analyzer.detectors.comprehension_detector import ListComprehensionDetection, \
    DictComprehensionDetection, SetComprehensionDetection
from src.python_language_analyzer.detectors.control_flow_detector import IfDetection
from src.utils.settings import Settings


def main():
    settings = Settings()
    java_aggregation_path = settings.get_path(['detections', 'java_python'])
    cpp_aggregation_path = settings.get_path(['detections', 'cpp_python'])
    fun_aggregation_path = settings.get_path(['detections', 'fun_python'])

    aggregation_paths = [java_aggregation_path, cpp_aggregation_path, fun_aggregation_path]
    aggregation_paths = [p + '/detections.json' for p in aggregation_paths]

    aggregators = [Aggregator.load(p) for p in aggregation_paths]
    labels = ['Java', 'C++', 'func languages']

    plotter = Plotter()

    # if
    if_percentage = [a.percentage(IfDetection, 'user_id') for a in aggregators]
    if_elseif_count_aggregation = [a.aggregate(IfDetection, 'elseif_count', 'user_id') for a in aggregators]
    if_has_else_aggregation = [a.aggregate(IfDetection, 'has_else', 'user_id') for a in aggregators]

    plotter(if_percentage, labels, 'If percentage')
    plotter(if_elseif_count_aggregation, labels, 'Elseif count')
    plotter(if_has_else_aggregation, labels, 'If has else')

    # class
    def line_count(detection):
        return detection.end - detection.begin + 1

    def name_length(detection):
        return len(detection.name)

    class_definition_percentage = [a.percentage(ClassDefinitionDetection, 'user_id') for a in aggregators]
    class_line_count_aggregation = [a.aggregate(ClassDefinitionDetection, line_count, 'user_id') for a in aggregators]
    class_method_count_aggregation = [a.aggregate(ClassDefinitionDetection, 'method_count', 'user_id') for a in aggregators]
    class_name_length_aggregation = [a.aggregate(ClassDefinitionDetection, name_length, 'user_id') for a in aggregators]
    class_is_nested_aggregation = [a.aggregate(ClassDefinitionDetection, 'nested', 'user_id') for a in aggregators]

    plotter(class_definition_percentage, labels, 'Class percentage')
    plotter(class_line_count_aggregation, labels, 'Class line count')
    plotter(class_method_count_aggregation, labels, 'Class method count')
    plotter(class_name_length_aggregation, labels, 'Class name length')
    plotter(class_is_nested_aggregation, labels, 'Class is nested')

    # built in functions
    class IsFunction:
        def __init__(self, name):
            self.name = name

        def __call__(self, detection):
            return 1 if detection.name == self.name else 0

    bif_percentage = [a.percentage(BuiltInFunctionDetection, 'user_id') for a in aggregators]
    bif_map_count_aggregation = [a.aggregate(BuiltInFunctionDetection, IsFunction('map'), 'user_id') for a in aggregators]
    bif_filter_count_aggregation = [a.aggregate(BuiltInFunctionDetection, IsFunction('filter'), 'user_id') for a in aggregators]
    bif_list_count_aggregation = [a.aggregate(BuiltInFunctionDetection, IsFunction('list'), 'user_id') for a in aggregators]
    bif_dict_count_aggregation = [a.aggregate(BuiltInFunctionDetection, IsFunction('dict'), 'user_id') for a in aggregators]
    bif_set_count_aggregation = [a.aggregate(BuiltInFunctionDetection, IsFunction('set'), 'user_id') for a in aggregators]

    plotter(bif_percentage, labels, 'Built in function percentage')
    plotter(bif_map_count_aggregation, labels, 'Map percentage')
    plotter(bif_filter_count_aggregation, labels, 'Filter percentage')
    plotter(bif_list_count_aggregation, labels, 'List percentage')
    plotter(bif_dict_count_aggregation, labels, 'Dict percentage')
    plotter(bif_set_count_aggregation, labels, 'Set percentage')

    # comprehensions
    list_comprehension_percentage = [a.percentage(ListComprehensionDetection, 'user_id') for a in aggregators]
    dict_comprehension_percentage = [a.percentage(DictComprehensionDetection, 'user_id') for a in aggregators]
    set_comprehension_percentage = [a.percentage(SetComprehensionDetection, 'user_id') for a in aggregators]

    list_comprehension_generator_count_aggregation = [a.aggregate(ListComprehensionDetection,
                                                                          'generator_count',
                                                                          'user_id') for a in aggregators]
    dict_comprehension_generator_count_aggregation = [a.aggregate(DictComprehensionDetection,
                                                                          'generator_count',
                                                                          'user_id') for a in aggregators]
    set_comprehension_generator_count_aggregation = [a.aggregate(SetComprehensionDetection,
                                                                         'generator_count',
                                                                         'user_id') for a in aggregators]

    plotter(list_comprehension_percentage, labels, 'List comprehension percentage')
    plotter(dict_comprehension_percentage, labels, 'Dict comprehension percentage')
    plotter(set_comprehension_percentage, labels, 'Set comprehension percentage')
    plotter(list_comprehension_generator_count_aggregation, labels, 'List comprehension generator count')
    plotter(dict_comprehension_generator_count_aggregation, labels, 'Dict comprehension generator count')
    plotter(set_comprehension_generator_count_aggregation, labels, 'Set comprehension generator count')


if __name__ == '__main__':
    main()
