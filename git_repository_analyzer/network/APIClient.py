# TODO: bootstrap script to install dependencies
import requests

# To fetch data about repository call APIClient.{method_name(id)} eg. APIClient.get_gitlab_project(6853087)
class APIClient:

    __github_api_base_url = 'https://api.github.com/'
    __gitlab_api_base_url = 'https://gitlab.com/api/v4/'

    @classmethod
    def get_github_project(cls, id):
        url = f'{cls.__github_api_base_url}projects/{id}'
        response = requests.get(url)
        return response
    
    @classmethod
    def get_gitlab_project(cls, id):
        url = f'{cls.__gitlab_api_base_url}projects/{id}'
        response = requests.get(url)
        return response.json()