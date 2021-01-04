import sys
from pathlib import Path
root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, f'{root_path}')

from git_repository_analyzer.network.api import API, PR_Type

def extract(owner, repo_name):
    repository_data = API.get_github_project(owner, repo_name)
    forks = repository_data['forks']
    watchers = repository_data['watchers_count']
    updated_at = repository_data['updated_at']
    created_at = repository_data['created_at']
    open_issues = repository_data['open_issues_count']
    subscribers_count = repository_data['subscribers_count']
    closed_issues = API.get_github_closed_issues(owner, repo_name)
    pr_open = API.get_github_pr_count(owner, repo_name, PR_Type.Open)
    pr_closed = API.get_github_pr_count(owner, repo_name, PR_Type.Closed)

    # TODO: Save to database

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
