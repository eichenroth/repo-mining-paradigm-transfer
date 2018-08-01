from argparse import ArgumentParser

from src.github.candidates import Candidates
from src.github.helper.language import Language


def analyze():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--expert_language', required=True, choices=('cpp', 'java', 'fun'))
    arg_parser.add_argument('--max_candidates', type=int, default=-1)

    arguments = arg_parser.parse_args()

    expert_language = Language(arguments.expert_language)
    python = Language('python')

    candidates = Candidates(expert_language, python)
    if arguments.max_candidates >= 0:
        limit = arguments.max_candidates
    else:
        limit = None
    candidates.analyze(limit)


if __name__ == '__main__':
    analyze()
