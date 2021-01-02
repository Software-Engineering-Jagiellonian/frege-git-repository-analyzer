# TODO: bootstrap script to install dependencies
import requests
from enum import Enum

class PR_Type(Enum):
    Open = 'open'
    Closed = 'closed'

# To fetch repository data call API.{method_name(...)} 
# eg. API.get_gitlab_project(6853087)

class API:

    __github_api_base_url = 'https://api.github.com/'
    __gitlab_api_base_url = 'https://gitlab.com/api/v4/'

    @classmethod
    def __get__(cls, url, headers):
        # TODO: Handle exception
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response
        except requests.exceptions.ConnectionError as err:
            raise SystemExit(err)
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)
        except requests.exceptions.RequestException as err:
            raise SystemExit(err)

    # Returns data about any public GitHub repository with owner and repo name in JSON format
    @classmethod
    def get_github_project(cls, owner, repo_name):
        path = f'{cls.__github_api_base_url}repos/{owner}/{repo_name}'
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = cls.__get__(path, headers)
        return response.json()

    # Returns number of closed issues for given GitHub repository
    @classmethod
    def get_github_closed_issues(cls, owner, repo_name):
        path = f'{cls.__github_api_base_url}search/issues?q=repo:{owner}/{repo_name}+type:issue+state:closed'
        response = cls.__get__(path, {})
        return response.json()['total_count']

    # Returns number of open/closed pull requests from given GitHub repository
    # Takes PR_Type as a state parameter
    @classmethod
    def get_github_pr_count(cls, owner, repo_name, state):
        if  not isinstance(state, PR_Type):
            raise TypeError("state attribute must be set to an instance of PR_Type")

        path = f'{cls.__github_api_base_url}search/issues?q=repo:{owner}/{repo_name}+type:pr+state:{state.value}'
        response = cls.__get__(path, {})
        return response.json()['total_count']
    
    # Returns data about any public GitLab repository with given id in JSON format
    @classmethod
    def get_gitlab_project(cls, id):
        path = f'{cls.__gitlab_api_base_url}projects/{id}'
        response = cls.__get__(path, {})
        return response.json()