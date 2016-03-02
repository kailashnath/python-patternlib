from patterns.aop import watchable

class User(object):
    def __init__(self, name):
        self.name = name

    @watchable
    def update_name(self, new_name):
        self.name = new_name
        return True

