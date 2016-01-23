from patterns.builder import BuilderPatternMetaclass


class FormParams(object):
    __metaclass__ = BuilderPatternMetaclass

    def __init__(self):
        self.params = {}

    def set_user_id(self, id):
        self.params['user_id'] = id

    def set_github_handle(self, handle):
        self.params['github_handle'] = handle

    def set_url(self, url):
        self.params['url'] = url

    def set_repo_type(self, repo_type):
        self.params['repo_type'] = repo_type

