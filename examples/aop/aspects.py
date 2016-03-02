from patterns.aop import after, before, around
from examples.aop.model import User



def before_change_name(obj, new_name, **kwargs):
    print 'Trying to change the name of the user: %s to :%s' % (obj.name, new_name)


def after_change_name(obj, new_name, **kwargs):
    print 'New name of the user is: %s' % new_name


def before_tx_begin(obj, new_name, aop_context={}):
    aop_context['old_name'] = obj.name


def after_tx_end(obj, new_name, aop_context={}, result=None):
    if result in (True, False):
        if result:
            print 'Name changed successfully for the user from %s to %s' % (aop_context['old_name'], new_name)
        else:
            print 'Name change failed for the user from %s to %s' % (aop_context['old_name'], new_name)


before(User.update_name, before_change_name)
after(User.update_name, after_change_name)
around(User.update_name, before_tx_begin, after_tx_end)

