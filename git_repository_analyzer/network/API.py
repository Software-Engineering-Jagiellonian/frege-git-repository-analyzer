# TODO: bootstrap script to install dependencies
import requests

# To fetch repository data call API.{method_name(id)} 
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
        url = f'{cls.__github_api_base_url}repos/{owner}/{repo_name}'
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = cls.__get__(url, headers)
        return response.json()
    
    # Returns data about any public GitLab repository with given id in JSON format
    @classmethod
    def get_gitlab_project(cls, id):
        url = f'{cls.__gitlab_api_base_url}projects/{id}'
        response = cls.__get__(url, {})
        return response.json()