class Language:
    """
    Resticts the usage of available languages.
    Links every language to a file extension or a set of file extensions.
    """
    FILE_EXTENSIONS = {
        'java': ['java'],
        'cpp': ['cpp'],
        'python': ['py'],
        'fun': ['hs', 'lhs', 'erl', 'hrl', 'lisp', 'lsp', 'clj', 'cljs', 'cljc', 'edu']
    }

    def __init__(self, language):
        if language not in self.FILE_EXTENSIONS.keys():
            raise ValueError('only accepted languages are ' + ', '.join(self.FILE_EXTENSIONS.keys()))

        self.language = language
        self.file_extensions = self.FILE_EXTENSIONS[language]