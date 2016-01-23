from .builder import BuilderPatternMetaclass
import inspect


class DIConfig(object):
    __metaclass__ = BuilderPatternMetaclass
    __meta_builder_prefix__ = 'bind'

    def __init__(self):
        self.mapping = {}

    def bind(self, name, implementation):
        self.mapping[name] = implementation

    def inject(self, name):
        val = self.mapping[name]
        kwargs = {}
        if inspect.isclass(val):
            args = []
            if inspect.ismethod(val.__init__):
                argspec = inspect.getargspec(val.__init__)
                f_args = argspec.args[1:]
                for each in f_args:
                    if each == 'self':
                        continue
                    if each in self.mapping:
                        args.append(self.inject(each))

                if len(f_args) < len(args):
                    args += argspec.defaults

            obj = val(*args, **kwargs)

            obj._meta_injector = self
            return obj
        else:
            return val

