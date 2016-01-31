from copy import copy
from .builder import BuilderPatternMetaclass
import inspect


class DIConfig(object):
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

    def inject(self, name):
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
                    if each in self.__mapping:
                        args.append(self.inject(each))

                if len(f_args) < len(args):
                    args += argspec.defaults

            obj = val(*args, **kwargs)

            obj._meta_injector = self
            return obj
        else:
            return val

    def freeze(self):
        self._frozen = True
        return self

