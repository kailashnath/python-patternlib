
class SingletonPatternMetaclass(type):

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_single_inst'):
            cls._single_inst = super(SingletonPatternMetaclass, cls).__call__(*args, **kwargs)

        return cls._single_inst

