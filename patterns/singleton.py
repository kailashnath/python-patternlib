
class SingletonPatternMetaclass(type):

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

