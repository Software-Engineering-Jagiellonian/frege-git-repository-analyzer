import unittest
from git_repository_analyzer.network.api import API

class TestAPI(unittest.TestCase):

    def test_github(self):
        result = API.get_github_project('facebook', 'react')
        self.assertEqual(result['id'], 10270250)
        self.assertEqual(result['name'], 'react')

    def test_gitlab(self):
        result = API.get_gitlab_project('278964')
        self.assertEqual(result['id'], 278964)
        self.assertIn('GitLab', result['description'])
        