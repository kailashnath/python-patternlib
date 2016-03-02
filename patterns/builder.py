from types import FunctionType
from functools import wraps


class BuilderPatternMetaclass(type):
    '''
    https://en.wikipedia.org/wiki/Builder_pattern

    ex:
        class Params(object):
            __metaclass__ = BuilderPatternMetaclass

            __meta_builder_prefix__ = 'use_'

            def use_name(self, name):
                self.name = name

            def use_id(self, di):
                self.id = id

        params = Params()
        params.use_name('builder').use_id(100)

        print params.name, params.id => builder, 100

    '''

    FUNC_PREFIX = 'set_'

    @staticmethod
    def builder_pattern_wrap(func):
        @wraps(func)
        def wrapped(self, *args, **kwargs):
            return func(self, *args, **kwargs) or self
        return wrapped

    def __new__(cls, name, bases, local):
        overrides = {}
        for name, val in local.items():
            prefix = local.get('__meta_builder_prefix__', BuilderPatternMetaclass.FUNC_PREFIX)
            if type(val) == FunctionType and \
                    val.func_name.startswith(prefix):
                val = BuilderPatternMetaclass.builder_pattern_wrap(val)
            overrides[name] = val
        return type.__new__(cls, name, bases, overrides)

