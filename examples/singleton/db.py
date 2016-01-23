from patterns.singleton import SingletonPatternMetaclass


class DbConnection(object):
    __metaclass__ = SingletonPatternMetaclass


