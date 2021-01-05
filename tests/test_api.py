import unittest
from git_repository_analyzer.network.API import API, PR_Type

class TestAPI(unittest.TestCase):

    def test_github_project(self):
        result = API.get_github_project('facebook', 'react')
        self.assertEqual(result['id'], 10270250)
        self.assertEqual(result['name'], 'react')

    def test_github_closed_issues(self):
        result = API.get_github_closed_issues('facebook', 'react')
        self.assertTrue(isinstance(result, int))
        self.assertTrue(result > 0)
    
    def test_github_pr_count(self):
        open_prs_count = API.get_github_pr_count('facebook', 'react', PR_Type.Open)
        self.assertTrue(isinstance(open_prs_count, int))
        self.assertTrue(open_prs_count > 0)

        closed_prs_count = API.get_github_pr_count('facebook', 'react', PR_Type.Closed)
        self.assertTrue(isinstance(closed_prs_count, int))
        self.assertTrue(closed_prs_count > 0)

    def test_gitlab(self):
        result = API.get_gitlab_project('278964')
        self.assertEqual(result['id'], 278964)
        self.assertIn('GitLab', result['description'])

