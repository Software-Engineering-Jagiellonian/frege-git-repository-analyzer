import sys
from pathlib import Path

root_path = Path(__file__).parent.parent.parent
sys.path.insert(0, f'{root_path}')

from git_repository_analyzer.network.api import API, StateType

# Returns dictionary of parameters rady to save to database
def extract_github_data(repo_primary_key, owner, repo_name):
    repository_data = API.get_github_project(owner, repo_name)
    
    entry = dict()
    entry['repo_id'] = repo_primary_key
    entry['forks'] = repository_data['forks']
    entry['watchers'] = repository_data['watchers_count']
    entry['updated_at'] = repository_data['updated_at']
    entry['created_at'] = repository_data['created_at']
    entry['open_issues'] = repository_data['open_issues_count']
    entry['subscribers_count'] = repository_data['subscribers_count']
    entry['closed_issues'] = API.get_github_closed_issues(owner, repo_name)
    entry['pr_open'] = API.get_github_pr_count(owner, repo_name, StateType.Open)
    entry['pr_closed'] = API.get_github_pr_count(owner, repo_name, StateType.Closed)

    return entry

def extract_gitlab_data(repo_id):
    repository_data = API.get_gitlab_project(repo_id.split('-')[0])
    issues_statistics = API.get_gitlab_issues_statistics(repo_id)

    entry = dict()
    entry['repo_id'] = f'gitlab-{repo_id}'
    entry['forks'] = repository_data['forks_count']
    entry['watchers'] = repository_data['star_count']
    entry['updated_at'] = repository_data['last_activity_at']
    entry['created_at'] = repository_data['created_at']
    entry['subscribers_count'] = None
    entry['open_issues'] = issues_statistics['opened']
    entry['closed_issues'] = issues_statistics['closed']
    entry['pr_open'] = API.get_gitlab_mr_statistics(repo_id, StateType.Opened)
    entry['pr_closed'] = API.get_gitlab_mr_statistics(repo_id, StateType.Closed)

    return entry


# TODO: 
# Change watchers to starred
# Remove subscribers (gitlab does not have that option)
# Add number of commits