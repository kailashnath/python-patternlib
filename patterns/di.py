from copy import copy
from .builder import BuilderPatternMetaclass
import inspect


class DIConfig(object):
    '''
    https://en.wikipedia.org/wiki/Dependency_injection

    Use only if you are aware of the pros and cons of the pattern. If things are too straight forward
    and not many types involved go ahead with param passing pattern

    class DbConnection(object):
        __metaclass__ = SingletonPatternMetaclass

        def __init__(self, sqlConn):
            self.connection = sqlConn

        def execute(self, query):
            return self.connection.execute('BEGIN %s END' % query)

    diconfig = DIConfig().bind('sqlConn', sql2).bind('db', DbConnection)

    conn = diconfig.inject('db')
    conn.execute('select 1');

    Now to test the class without modifying the construction and usage we override the injectable

    class EchoSqlConnection(object):

        def execute(self, query):
            return query


    diconfig.bind('sqlConn', EchoSqlConnection)

    conn = diconfig.inject('db')
    assert conn.execute('select 1') == 'BEGIN %s END' % query


    .freeze():

    Call this method on the config object if you choose to not mutate the defined
    dependencies. It will be handle when you are exposing the config out of the scope of
    the given module

    '''

    __metaclass__ = BuilderPatternMetaclass
    __meta_builder_prefix__ = 'bind'

    def __init__(self, preconfig={}):
        self.__mapping = {} 
        self.__mapping.update(**preconfig)
        self._frozen = False

    def bind(self, name, implementation):
        if not self._frozen:
            self.__mapping[name] = implementation
            return self
        else:
            return DIConfig(preconfig=copy(self.mapping))

    def inject(self, name, **overrides):
        val = self.__mapping[name]
        kwargs = {}
        if inspect.isclass(val):
            args = []
            if inspect.ismethod(val.__init__):
                argspec = inspect.getargspec(val.__init__)
                f_args = argspec.args[1:]
                for each in f_args:
                    if each == 'self':
                        continue

                    if each in overrides:
                        args.append(overrides[each])

                    elif each in self.__mapping:
                        args.append(self.inject(each))

                if len(f_args) < len(args):
                    args += argspec.defaults

            obj = val(*args, **kwargs)
            obj._injector = self
            return obj
        else:
            return val

    def freeze(self):
        self._frozen = True
        return self

