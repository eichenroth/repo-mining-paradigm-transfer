import os

from git import Repo
from psycopg2.sql import SQL, Identifier

from src.database.postgres_db import PostgresDbDictCursor
from src.github.downloader import Downloader
from src.github.helper.patch import Patch
from src.python_language_analyzer.aggregator import Aggregator
from src.python_language_analyzer.analyzer import Analyzer
from src.python_language_analyzer.detector import UnparsableError
from src.utils.directory_finder import DirectoryFinder
from src.utils.settings import Settings


class Candidate:
    def __init__(self, user_id, login, expert_language, second_language, expert_loc=10000, second_loc=1000):
        """
        :param user_id: User id
        :param login: User name
        :param expert_language: helper.language.Language object of the expert language.
        :param second_language: helper.language.Language object of the language to examine. For now just Python.
        :param expert_loc: Lines of code that is the threshold for an expert.
        :param second_loc: Lines of code threshold for the language to examine to get a code base that is large enough.
        """
        self.user_id = user_id
        self.login = login
        self.expert_language = expert_language
        self.second_language = second_language
        self.expert_loc = expert_loc
        self.second_loc = second_loc

        settings = Settings()
        if self.expert_language.language == 'java' and self.second_language.language == 'python':
            self.candidates_view = settings.get_database_view('candidates_java_py')
            self.result_dir_path = settings.get_path(['detections', 'java_python'])
        elif self.expert_language.language == 'cpp' and self.second_language.language == 'python':
            self.candidates_view = settings.get_database_view('candidates_cpp_py')
            self.result_dir_path = settings.get_path(['detections', 'cpp_python'])
        elif self.expert_language.language == 'fun' and self.second_language.language == 'python':
            self.candidates_view = settings.get_database_view('candidates_fun_py')
            self.result_dir_path = settings.get_path(['detections', 'fun_python'])
        else:
            raise ValueError('No database view for this combination of languages.')

    def get_significant_commits(self):
        with PostgresDbDictCursor() as cursor:
            query = SQL('''
                SELECT * FROM {} WHERE author_id = %s ORDER BY created_at ASC;
            ''').format(
                Identifier(self.candidates_view)
            )
            cursor.execute(query, [self.user_id])

            expert_language_loc = {ext: 0 for ext in self.expert_language.file_extensions}
            second_language_loc = {ext: 0 for ext in self.second_language.file_extensions}
            max_expert_language_loc = 0
            commits = []

            for row in cursor:
                if row['file_ext'] in self.expert_language.file_extensions:
                    expert_language_loc[row['file_ext']] += row['additions']
                    max_expert_language_loc = max(max_expert_language_loc, expert_language_loc[row['file_ext']])
                elif row['file_ext'] in self.second_language.file_extensions:
                    second_language_loc[row['file_ext']] += row['additions']
                    if max_expert_language_loc >= self.expert_loc and second_language_loc[
                        row['file_ext']] >= self.second_loc:
                        commits.append((row['sha'], row['owner'], row['project_name']))
            return commits


class Candidates:
    def __init__(self, expert_language, second_language, expert_loc=10000, second_loc=1000):
        """
        :param expert_language: helper.language.Language object of the expert language.
        :param second_language: helper.language.Language object of the language to examine. For now just Python.
        :param expert_loc: Lines of code that is the threshold for an expert.
        :param second_loc: Lines of code threshold for the language to examine to get a code base that is large enough.
        """
        self.expert_language = expert_language
        self.second_language = second_language
        self.expert_loc = expert_loc
        self.second_loc = second_loc

        settings = Settings()
        loc_user_file_ext_view = settings.get_database_view('loc_user_file_ext')

        self.query = SQL('''
            SELECT
                u1.user_id,
                u1.login
            FROM {} AS u1
                JOIN {} AS u2 ON u1.user_id = u2.user_id
                JOIN users u ON u1.user_id = u.id
            WHERE u1.additions >= %s AND u1.file_ext = ANY(%s) AND u2.additions >= %s AND u2.file_ext = ANY(%s) AND u.type = 'USR';
        ''').format(
            Identifier(loc_user_file_ext_view),
            Identifier(loc_user_file_ext_view)
        )

        self.detection_path = settings.get_path(['detections', expert_language.language + '_' + second_language.language])

    def __iter__(self, *args, **kwargs):
        with PostgresDbDictCursor() as cursor:
            cursor.execute(self.query, [self.expert_loc, self.expert_language.file_extensions, self.second_loc,
                                        self.second_language.file_extensions])
            for row in cursor:
                yield row['user_id'], row['login']

    def __call__(self):
        for user_id, login in self:
            yield Candidate(user_id, login, self.expert_language, self.second_language, self.expert_loc,
                            self.second_loc)

    def download(self, limit=None):
        for counter, candidate in enumerate(self()):
            if counter == limit:
                break
            print('download candidate {}'.format(counter+1))
            commits = candidate.get_significant_commits()
            downloader = Downloader(10, commits)
            downloader.start()

    def analyze(self, limit=None):
        aggregator = Aggregator(('user_id', 'commit_sha', 'file_name'), file_path=self.detection_path + '/detections.json')

        for counter, candidate in enumerate(self()):
            if counter == limit:
                break
            print('analyze candidate {}'.format(counter+1))

            commits = candidate.get_significant_commits()
            directory_finder = DirectoryFinder()

            for commit in commits:
                repository_dir = directory_finder.project_directory((commit[1], commit[2]))
                if repository_dir is None:
                    continue
                repository = Repo(repository_dir)
                try:
                    current_commit = repository.commit(commit[0])
                except ValueError:
                    # cannot find commit in repo
                    continue

                if len(current_commit.parents) == 0:
                    diffs = current_commit.diff(create_patch=True)
                elif len(current_commit.parents) == 1:
                    diffs = current_commit.parents[0].diff(current_commit, create_patch=True)
                else:
                    continue

                for diff in diffs:
                    patch = Patch(diff.diff.decode('utf-8', 'replace'))
                    if diff.renamed_file \
                            or diff.deleted_file \
                            or len(patch.hunks) == 0 \
                            or os.path.splitext(diff.b_path)[1].lower() != '.py':
                        continue

                    try:
                        file_content = diff.b_blob.data_stream.read().decode('utf-8', 'replace')
                    except ValueError:
                        continue

                    # line_count = len(file_content.split('\n'))
                    analyzer = Analyzer(file_content)
                    try:
                        current_detections = analyzer()
                    except UnparsableError:
                        continue
                    current_detections = self.filter_detections(current_detections, patch)
                    aggregator.add_detections((candidate.user_id, current_commit.hexsha, diff.b_path),
                                              current_detections)

            aggregator.save()

    @staticmethod
    def filter_detections(detections, patch):
        filtered_detections = []
        for detection in detections:
            for hunk in patch.hunks:
                if detection.begin >= hunk.begin and detection.end <= hunk.end:
                    filtered_detections.append(detection)
        return filtered_detections
