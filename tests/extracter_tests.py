import unittest
from git_repository_analyzer.analyzer.github_data_extracter import extract_project_name_from_url, extract_user_name_from_url

class TestExtracter(unittest.TestCase):

    def test_extract_project_name(self):
        url = 'https://gitlab.com/gitlab-org/gitlab'
        project_name = extract_project_name_from_url(url)
        self.assertEqual(project_name, 'gitlab')

    def test_extract_user_name(self):
        url = 'https://gitlab.com/gitlab-org/gitlab'
        user_name = extract_user_name_from_url(url)
        self.assertEqual(user_name, 'gitlab')