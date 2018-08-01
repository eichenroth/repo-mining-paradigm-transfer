import os

from psycopg2.sql import SQL, Identifier

from src.database.postgres_db import PostgresDbDictCursor
from src.utils.settings import Settings


class Sha:
    """
    Commit sha.
    Links to a commit and therefore can be associated with a project.
    """
    def __init__(self, sha):
        self.sha = sha

        settings = Settings()
        self._downloads_path = settings.get_path('downloads')
        self._download_archive_path = settings.get_path('download_archive')
        self._earliest_project_view = settings.get_database_view('earliest_project')

    def get_projects(self):
        """
        :return: Used to locate the repositories on github.
            List of tuples containing owner name and repo name.
        """
        with PostgresDbDictCursor() as cursor:
            query = SQL('''
                SELECT
                  c.sha,
                  u.login AS username,
                  p.name  AS project_name
                From commits AS c
                  JOIN project_commits pc on c.id = pc.commit_id
                  JOIN projects p ON pc.project_id = p.id
                  JOIN users u ON p.owner_id = u.id
                WHERE c.sha = %s;
            ''')

            cursor.execute(query, [self.sha])
            return [(row['username'], row['project_name']) for row in cursor.fetchall()]

    def get_earliest_project(self):
        """
        :return: Used to locate the repository on github.
            Tuple containing owner name and repo name.
        """
        with PostgresDbDictCursor() as cursor:
            query = SQL('''
                SELECT
                  ep.sha,
                  u.login AS username,
                  p.name AS project_name
                FROM {} ep
                  JOIN projects p ON ep.project_id = p.id
                  JOIN users u ON p.owner_id = u.id
                WHERE ep.sha = %s;
            ''').format(
                Identifier(self._earliest_project_view)
            )

            cursor.execute(query, [self.sha])
            row = cursor.fetchone()
            return row['username'], row['project_name']

    def downloaded_project(self):
        """
        :return:
            - None if no project with this sha is downloaded.
            - Project dir containing this sha if any is downloaded.
        """
        projects = self.get_projects()
        for project in projects:
            path = '{}/{}/{}'.format(
                self._download_archive_path,
                project[0],
                project[1])
            if os.path.isdir(path + '/.git'):
                return path

            path = '{}/{}/{}'.format(
                self._downloads_path,
                project[0],
                project[1]
            )
            if os.path.isdir(path + '/.git'):
                return path

    def __str__(self):
        return self.sha
