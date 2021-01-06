import sys
from pathlib import Path

root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, f'{root_path}')

from git_repository_analyzer.network.api import API, PR_Type

# Returns dictionary of parameters rady to save to database
def extract_github_data(repo_id, owner, repo_name):
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

    return entry


