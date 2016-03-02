'''
https://en.wikipedia.org/wiki/Aspect-oriented_software_development

Ex:

@watchable
def add_user_to_project(project_id, user_id, sql=sql2):
    project = get(project_id)
    with sql2.transaction() as tx:
        project.addMember(user_id)
        tx.add('INSERT INTO ppWSUsers (wsId, userId) VALUES (:project_id, :user_id)',
                {'project_id': project_id, 'user_id': user_id})
    return True


def log_begin(project_id, user_id):
    kpi.publish(USER_ADD_PROJECT_BEGIN, project_id, user_id)


def log_end(project_id, user_id, aop_context):
    kpi.publish(USER_ADD_PROJECT_END, project_id, user_id)
    ev = USER_ADD_PROJECT_SUCCESS if aop_context['result'] else USER_ADD_PROJECT_FAIL
    kpi.publish(ev, project_id, user_id)


def trace_tx_begin(project_id, user_id, aop_context):
    import time
    aop_context['ts'] = time.time()


def trace_tx_end(project_id, user_id, aop_context):
    import time
    print "Time for transaction: %s" % time.time() - aop_context['ts']


before(add_user_to_project, log_begin)
after(add_user_to_project, log_end)
around(add_user_to_project, trace_tx_begin, trace_tx_end)
'''


from functools import wraps

import logging
import sys

logger = logging.getLogger('aop')
logger.addHandler(logging.StreamHandler())

__Befores = {}
__Afters = {}



def load_dependencies(func, importer=__import__):
    loc = sys.modules[func.__module__].__package__

    # this is a hack for api.wsgi because we have watchable there as well and it's also
    # an entry point into the system which in itself is bad, hence the hack
    package = '%s.aspects' % loc

    if package:
        try:
            importer(package)
        except ImportError, e:
            logging.exception(repr(e))


def call(fs, *args, **kwargs):
    for f in fs:
        try:
            f(*args, **kwargs)
        except AssertionError, e:
            raise e
        except Exception, e:
            logger.exception(repr(e))


def watchable(func):
    id = uid(func)
    @wraps(func)
    def wrap(*args, **kwargs):
        # a lazy way of loading the aspects
        load_dependencies(func)

        befores = __Befores.get(id, None)
        afters = __Afters.get(id, None)
        aopKwargs = kwargs.copy()
        if befores and afters:
            aopKwargs['aop_context'] = {}

        if befores:
            call(befores, *args, **aopKwargs)

        result = func(*args, **kwargs)

        if afters:
            aopKwargs['result'] = result
            call(afters, *args, **aopKwargs)

        return result

    wrap.__aop_func__ = func
    return wrap


def uid(func):
    return id(func.func_code)


def register(coll, joinPoint, *advices):
    act_func = getattr(joinPoint, '__aop_func__', None)

    if not act_func:
        raise TypeError("The %s is not watchable" % joinPoint)
    elif not advices:
        raise Exception("Atleast one advice is required for registering")

    jid = uid(act_func)

    if jid in coll:
        coll[jid] += advices
    else:
        coll[jid] = advices


def before(joinPoint, *advices):
    global __Befores
    register(__Befores, joinPoint, *advices)


def after(joinPoint, *advices):
    global __Afters
    register(__Afters, joinPoint, *advices)


def around(joinPoint, b, a):
    before(joinPoint, b)
    after(joinPoint, a)

