import re


class Patch:
    """
    Used to analyze the changes patch of a commit.
    Wraps a list of hunks that the commit consists of.
    """
    def __init__(self, string):
        lines = string.split('\n')
        self.hunks = []

        for line in lines:
            if len(line) > 0 and line[0] == '@':
                line_split = line.split()
                hunk_lines = line_split[len(line_split[0])]
                self.hunks.append(Hunk(hunk_lines=hunk_lines))


class Hunk:
    HUNK_LINES_REGEX_SING = re.compile('\+([0-9]+)')
    HUNK_LINES_REGEX_MULT = re.compile('\+([0-9]+)\,([0-9]+)')

    def __init__(self, begin=0, end=0, hunk_lines=None):
        self.begin = begin
        self.end = end
        if hunk_lines is not None:
            self.set_hunk_lines(hunk_lines)

    def set_hunk_lines(self, hunk_lines):
        mult_match = self.HUNK_LINES_REGEX_MULT.match(hunk_lines)
        if mult_match is not None:
            self.begin = int(mult_match.group(1))
            self.end = int(mult_match.group(2)) + self.begin - 1
        else:
            sing_match = self.HUNK_LINES_REGEX_SING.match(hunk_lines)
            self.begin = self.end = int(sing_match.group(1))
