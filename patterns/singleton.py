
class SingletonPatternMetaclass(type):
    '''
    https://en.wikipedia.org/wiki/Singleton_pattern

    ex:
        class DbConnection(object):
            __metaclass__ = SingletonPatternMetaclass

            def __init__(self):
                self.connection = open_connection()

            def execute(self, query):
                return self.connection.execute(query)

        d_1 = DbConnection()
        d_2 = DbConnection()

        assert d_1 == d_2 # True
    '''
    def __call__(cls, *args, **kwargs):
        instance = None
        if hasattr(cls, '_inst_cache'):
            for inst, argcol in cls._inst_cache:
                if argcol == (args, kwargs):
                    instance = inst
        else:
            cls._inst_cache = []

        if not instance:
            instance = super(SingletonPatternMetaclass, cls).__call__(*args, **kwargs)

        cls._inst_cache.append([instance, (args, kwargs)])

        return instance

