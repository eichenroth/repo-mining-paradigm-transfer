# Source

## Content
The source consists of these folders:
- [`database`](/src/database): Contains a database helper that helps creating a database connection, and reading and writing dicts using a database cursor.
- [`github`](/src/github): Contains the main logic of the project and connects all modules.
  - With the [candidates.py](/src/github/candidates.py) file one can create a list of candidates that fulfill the selection attributes for a candidate like the language or the lines of code.
  One is able to download all available repositories for all relevant commits for every candidate. This module also allows the analyzing of these repositories.
  - With the [plotter.py](/src/github/plotter.py) file one can plot all aggregated values from different aggregators.
- [`python_language_analyzer`](/src/python_language_analyzer): Contians the whole language feature detection logic as well as the aggregation logic. This package has no dependencies anywhere other in the project and can therefore be exporterd entirely.
  - With the [`Detector`](/src/python_language_analyzer/detector.py) class and its [subclasses](/src/python_language_analyzer/detectors) one can detect certain language usages in the project.
  `Detection`s are found using the `ast` parsing from python itself and the visitor pattern while traversing the `ast`-tree.
  New detectors, detections and visitors can be built inheriting from [`Detector`](/src/python_language_analyzer/detector.py), [`Detection`](/src/python_language_analyzer/detector.py) and `ast.NodeVisitor` respectively as seen in the [`detectors`](/src/python_language_analyzer/detectors) folder.
  - With the [`Analyzer`](/src/python_language_analyzer/analyzer.py) class it is possible to use all detectors or a selection of detectors on one file.
  The object gets a python file in form of a string or a list of lines and returns all [`Detection`s](/src/python_language_analyzer/detector.py).
  - With the [`Aggregator`](/src/python_language_analyzer/aggregator.py) class one can aggregate a detections on multiple levels, e.g. choosing the aggregation levels (user, commit, file) one could use tree different aggregations, each more granularly.
- [`utils`](/src/utils): Contains helpers.
  - A [settings](/src/utils/settings.py) file that allows loading of all settings.
  - A [directory finder](/src/utils/directory_finder.py) that helps finding the repositoy directory for a given project.

## Potential Improvements
- [`github`](/src/github): The `Candidate` object could be modified in order to select candiates with other criteria.
This would be possible by duplicating this object and overwriting the method `get_significant_commits` and returning another filtered set of candidate commits.
- [`python_language_analyzer`](/src/python_language_analyzer):
  - The detection percentages could be calculated not per detection but per line added or per commit.
  This could be implemented if the method `add_detections` would get an additional optional value that is 1 per default. This could be added to a counter for every key and the percentage is calculationg by dividing by this sum. This would also require to change the `save` and `load` methods.
  - Instead of calculating the mean during aggregation it is possible to implement other aggregation functions like min, max, median, geometric mean and harmonic mean.
  This would be possible by changing the `aggregation_list` calculation within the `aggregate` method.
