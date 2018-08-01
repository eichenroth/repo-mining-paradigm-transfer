from threading import Thread, Semaphore

from git import Repo
from git.exc import GitCommandError

from src.utils.directory_finder import DirectoryFinder

sem = Semaphore()


class Downloader:
    def __init__(self, worker_count, commits):
        """
        :param worker_count: Number of threads that should be started to download the repositories.
        :param shas: List of Sha objects
        """
        self.workers = []
        for i in range(worker_count):
            self.workers.append(DownloadWorker(self.get_project))

        self.commits = commits
        self.projects = set()
        for commit in self.commits:
            self.projects.add((commit[1], commit[2]))

    def get_project(self):
        project = None
        sem.acquire()
        if len(self.projects) > 0:
            project = self.projects.pop()
        sem.release()
        return project

    def start(self):
        for worker in self.workers:
            worker.start()
        for worker in self.workers:
            worker.join()


class DownloadWorker(Thread):
    PROTOCOL = 'https'
    INVALID_USER = 'sab22dok3g34b48q2f8b'
    INVALID_PASSWORD = 'nofdyo0dv3hq86flrpdu'
    GITHUB_URL = 'github.com'

    def __init__(self, get_project):
        super().__init__()

        self.get_project = get_project

        self.directory_finder = DirectoryFinder()

    def run(self):
        run = True

        while run:
            project = self.get_project()
            if not project:
                break
            if self.directory_finder.project_directory(project):
                continue

            try:
                repository_url = self._repository_url(project)
                repository_path = self.directory_finder.download_directory(project)

                Repo.clone_from(repository_url, repository_path)
            except GitCommandError as e:
                pass
                # Repo does not exist or repo gets copied at the same time
            except Exception as e:
                pass
                # TODO Log

    def _repository_url(self, project):
        return '{}://{}:{}@{}/{}/{}'.format(
            self.PROTOCOL,
            self.INVALID_USER,
            self.INVALID_PASSWORD,
            self.GITHUB_URL,
            project[0],
            project[1])
