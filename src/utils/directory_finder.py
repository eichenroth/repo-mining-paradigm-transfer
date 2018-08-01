import os

from src.utils.settings import Settings


class DirectoryFinder:
    def __init__(self):
        settings = Settings()
        self.archive_path = settings.get_path('download_archive')
        self.download_path = settings.get_path('downloads')

    def project_directory(self, project):
        path = '{}/{}/{}'.format(self.archive_path, project[0], project[1])
        if os.path.isdir(path + '/.git'):
            return path

        path = '{}/{}/{}'.format(self.download_path, project[0], project[1])
        if os.path.isdir(path + '/.git'):
            return path

    def download_directory(self, project):
        return '{}/{}/{}'.format(
            self.download_path,
            project[0],
            project[1])
