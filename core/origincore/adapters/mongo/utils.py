#! -*- coding: utf-8 -*-


def cursor_to_list(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retval = func(*args, **kwargs)
        if isinstance(retval, Cursor):
            retval = [x for x in retval]
        elif isinstance(retval, dict) and 'results' in retval and 'total' in retval:
            if isinstance(retval['results'], Cursor):
                retval['results'] = [x for x in retval['results']]
        return retval
    return wrapper
