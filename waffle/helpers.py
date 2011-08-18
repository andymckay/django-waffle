from contextlib import contextmanager

import jingo
import jinja2

from waffle import flag_is_active, sample_is_active, switch_is_active


@jinja2.contextfunction
def flag_helper(context, flag_name):
    return flag_is_active(context['request'], flag_name)


jingo.env.globals['waffle'] = {
    'flag': flag_helper,
    'switch': switch_is_active,
    'sample': sample_is_active,
}


@contextmanager
def patch_waffle(key, method):
    """A method to patch jingo for tests"""
    item = jingo.env.globals['waffle']
    orig, item[key] = item[key], method
    yield
    item[key] = orig
