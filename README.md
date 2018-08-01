# Repositoy Mining - Paradigm Transfer

This repository contains the scripts and modules to examine paradigm transfer when changing programming languages.

## Procedure
Using this repository the folowing steps should be done in this order.
1. Edit the create a `settings.yml` file in the root folder following the structure of the [`settings.default.yml`](/settings.default.yml) file.
1. Run the [PostgreSQL scripts](/sql/view_creation.sql) in that very order to create all necessary materialized views.
1. Download the candidate repos for the three languages using the [script](/script_download_candidates.py).
1. Analyze the candidate repos for the three languages using the [script](/script_analyze_candidates.py).
1. Plot the aggregated results using the [script](/script_aggregate_results.py)

## Files and Folders
The files and folders are organized as follows:

- [`jupyter/`](/jupyter): contains two jupyter notebooks to discover the functionality of the modules.
The notebooks are:
  - [`detector_example`](/detector_example.ipynb): This notebook helps to understand how the `python_language_analyzer` module.
  - [`aggregation_plots`](/aggregation_plots.ipynb): This notebook helps to understand the plotter and aggregator for the detection results.
- [`sql/`](/sql): contains the PostgreSQL script to create all materialized views. The views are:
  - `earliest_project`: This view contains the earliest created project that has not been deleted for every commit. (Creation time: < 24h)
  - `loc_commit_file_ext`: This view contains the lines added and deleted for every file extension (language) of every commit. (Creation time: ~ 7 days)
  - `loc_user_file_ext`: This view contains the lines added and deleted for every file extension (language) of every user. (Creation time: < 12h)
  - `candidates_java_py`: This view contains all the commits of all Java candidates that fulfill the threshold requirements of added and deleted lines. (Creation time: < 12h)
  - `candidates_cpp_py` This view contains all the commits of all C++ candidates that fulfill the threshold requirements of added and deleted lines. (Creation time: < 12h)
  - `candidates_fun_py`:  This view contains all the commits of all functional programming candidates that fulfill the threshold requirements of added and deleted lines. (Creation time: < 12h)
- [`src/`](/src): contains the classes and modules used for downloading, analyzing and aggregation.
For further information about the usage of these modules see the [README.md](/src/README.md) in the source folder.
- [`settings.default.yml`](/settings.default.yml): This is the default settings file. It has to be copied and renamed to `settings.yml`. Most of the scripts require a settings file to load environment information.
- Scripts: The script files are all prefixed with `script_`.
The follwing scripts exist:
  - [download_candidates](/script_download_candidates.py): This script downloads the repositories for a given number of candidates for a given language.
  - [analyze_candidates](/script_analyze_candidates.py): This script analyzes the downloaded repositories for a given number of candidates for a given language.
  - [aggregate_results](/script_aggregate_results.py): This script aggregates and plots the results for the three candidate groups for _Java_, _C++_ and _functional languages_.
