import sys
from pathlib import Path

root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, f'{root_path}')

from git_repository_analyzer.network.API import API, PR_Type
from git_repository_analyzer.dbManager.db_manager import DbManager

dbM = DbManager()


def extract(repo_id, owner, repo_name):
    repository_data = API.get_github_project(owner, repo_name)
    entry = dict()

    entry['repo_id'] = repo_id
    entry['forks'] = repository_data['forks']
    entry['watchers'] = repository_data['watchers_count']
    entry['updated_at'] = repository_data['updated_at']
    entry['created_at'] = repository_data['created_at']
    entry['open_issues'] = repository_data['open_issues_count']
    entry['subscribers_count'] = repository_data['subscribers_count']
    entry['closed_issues'] = API.get_github_closed_issues(owner, repo_name)
    entry['pr_open'] = API.get_github_pr_count(owner, repo_name, PR_Type.Open)
    entry['pr_closed'] = API.get_github_pr_count(owner, repo_name, PR_Type.Closed)

    dbM.save_repository_statistics(entry)

def extract_user_name_from_url(url: str):
    splitted_url = url.split('/')
    if splitted_url.count < 4:
        # TODO: Raise error
        print('Invalid project url')
    return splitted_url[3]

def extract_project_name_from_url(url: str):
    splitted_url = url.split('/')
    if splitted_url.count < 4:
        # TODO: Raise error
        print('Invalid project url')
    return splitted_url[4]

