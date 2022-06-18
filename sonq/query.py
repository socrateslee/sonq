'''
Query dict or SON data objects with the style used in mongo shell,
support most of the operators documented in
https://docs.mongodb.com/manual/reference/operator/query/ .
'''
import bson

class NonExistOpHandlerException(Exception):
    pass


def get_separated_attr(dict_obj, attr_name, separator='.'):
    '''
    Extract dot separated attribute from dict_object.
    '''
    parts = attr_name.split(separator)
    curr = dict_obj
    existed = False
    parts_last_idx = len(parts) - 1
    for num, part in enumerate(parts):
        if curr is None:
            break
        if part.isdigit() and isinstance(curr, (list, tuple)):
            part = int(part)
            if part < len(curr):
                curr = curr[part]
                if num == parts_last_idx:
                    existed = True
            else:
                curr = None
        elif isinstance(curr, dict) and part in curr:
            curr = curr[part]
            if num == parts_last_idx:
                existed = True
        else:
            curr = None
    return existed, curr


class Handlers:
    @classmethod
    def op_noop(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        '''
        A noop op handler.
        '''
        return match(curr_obj, op_filter)

    @classmethod
    def op_eq(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        if isinstance(curr_obj, (list, tuple)):
            return op_filter == curr_obj or op_filter in curr_obj
        if isinstance(curr_obj, bson.objectid.ObjectId):
            return str(curr_obj) == op_filter
        return curr_obj == op_filter

    @classmethod
    def op_ne(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        return not cls.op_eq(curr_obj, op_filter, parent_filters)

    @classmethod
    def op_gt(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        if curr_obj is None:
            return False
        return curr_obj > op_filter

    @classmethod
    def op_gte(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        if curr_obj is None:
            return False
        return curr_obj >= op_filter

    @classmethod
    def op_lt(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        if curr_obj is None:
            return False
        return curr_obj < op_filter

    @classmethod
    def op_lte(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        if curr_obj is None:
            return False
        return curr_obj <= op_filter

    @classmethod
    def op_in(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        if not hasattr(op_filter, '__iter__'):
            return False
        if isinstance(curr_obj, (list, tuple)):
            for i in curr_obj:
                if i in op_filter:
                    return True
        return curr_obj in op_filter

    @classmethod
    def op_nin(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        return not cls.op_in(curr_obj, op_filter, parent_filters)

    @classmethod
    def op_and(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        for sub_filter in op_filter:
            if not match(curr_obj, sub_filter, separator=separator):
                return False
        return True

    @classmethod
    def op_or(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        for sub_filter in op_filter:
            if match(curr_obj, sub_filter, separator=separator):
                return True
        return False

    @classmethod
    def op_nor(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        return not cls.op_or(curr_obj, op_filter, parent_filters, separator=separator)

    @classmethod
    def op_not(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        return not match(curr_obj, op_filter, separator=separator)

    @classmethod
    def op_and(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        for sub_filter in op_filter:
            if not match(curr_obj, sub_filter, separator=separator):
                return False
        return True

    @classmethod
    def op_not(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        return not match(curr_obj, op_filter, separator=separator)

    @classmethod
    def op_exists(cls, curr_obj, op_filter, parent_filters, separator='.', **kw):
        existed = kw.get('existed')
        if op_filter not in (True, False):
            raise Exception("The value of '$exists' must be true or false.")
        return existed == op_filter


def call_op_handler(op, dict_obj, op_filter, parent_filters, separator='.', **kw):
    '''
    Call an op handler.
    '''
    op_handler = getattr(Handlers, 'op_%s' % op[1:], None)
    if op_handler is None:
        raise NonExistOpHandlerException("Op handler %s is not existed." % op)
    return op_handler(dict_obj, op_filter, parent_filters, separator=separator, **kw)


def match(dict_obj, filters, separator='.', existed=None):
    '''
    Match a dict_obj with the filters.
    '''
    correct_filters = {k: v for (k, v) in filters.items() if k != '$comment'}
    for k, rule in correct_filters.items():
        if k.startswith('$'):  # for op handler
            ret = call_op_handler(k, dict_obj, rule, correct_filters,
                                  separator=separator, existed=existed)
        else:  # separator nested attribute
            existed, value = get_separated_attr(dict_obj,
                                                k,
                                                separator=separator)
            if isinstance(rule, dict):  # nested attribute
                ret = match(value, rule, separator=separator, existed=existed)
            else:
                ret = Handlers.op_eq(value, rule, correct_filters)
        if not ret:
            return False
    return True


def query(iterable, filters, serarator='.'):
    '''
    Query an iterable sequence with filters, yield match objects.
    '''
    for dict_obj in iterable:
        if match(dict_obj, filters, separator='.'):
            yield dict_obj
