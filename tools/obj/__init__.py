OBJ_LEVEL_BASE: str = ' ' * 4
OBJ_PREFIX: str = ' = '


def objrepr(obj,
            name: str = '',
            level: int = 0,
            add_list_idx: bool = True,
            add_tuple_idx: bool = True,
            sort_dict_keys: bool = True) -> str:
    level_str: str = (level *
                      OBJ_LEVEL_BASE)
    if name:
        p = '%s%s' % (name, OBJ_PREFIX)
    else:
        p: str = ''
    r: str = ''
    if obj is None:
        r = '%s%sNone' % (level_str, p)
    elif isinstance(obj, str):
        r = '%s%sstr(%s)' % (level_str, p, obj)
    elif isinstance(obj, bool) \
            or isinstance(obj, bytes) \
            or isinstance(obj, bytearray):
        r = '%s%s%s' % (level_str, p, str(obj))
    elif isinstance(obj, int):
        r = '%s%sint(%s)' % (level_str, p, str(obj))
    elif isinstance(obj, float):
        r = '%s%sfloat(%s)' % (level_str, p, str(obj))
    elif isinstance(obj, range):
        r = '%s%srange(%s, %s, %s)' % (level_str, p, str(obj.start), str(obj.stop), str(obj.step))
    elif isinstance(obj, complex):
        if obj.imag < 0:
            s: str = ''
        else:
            s: str = '+'
        r = '%s%scomplex(%s%s%sj)' % (level_str, p, str(obj.real), s, str(obj.imag))
    elif isinstance(obj, list) or isinstance(obj, tuple):
        if isinstance(obj, list):
            h: str = 'list'
            add_idx: bool = add_list_idx
        else:
            h: str = 'tuple'
            add_idx: bool = add_tuple_idx
        if obj:
            r = '%s%s%s(\n' % (level_str, p, h)
            i: int = 0
            n: str = ''
            for e in obj:
                if add_idx:
                    n = '#%d' % i
                r += '%s\n' % (objrepr(e,
                                       name=n,
                                       level=level + 1,
                                       add_list_idx=add_list_idx,
                                       add_tuple_idx=add_tuple_idx,
                                       sort_dict_keys=sort_dict_keys))
                i += 1
            r += '%s)' % (level_str)
        else:
            r = '%s%s%s()' % (level_str, p, h)
    elif isinstance(obj, set) or isinstance(obj, frozenset):
        if isinstance(obj, set):
            h: str = 'set'
        else:
            h: str = 'frozenset'
        if obj:
            r = '%s%s%s(\n' % (level_str, p, h)
            # Create an ordered list to always have the same result
            s2l: list = []
            for e in obj:
                s2l.append(objrepr(e,
                                   level=level + 1,
                                   add_list_idx=add_list_idx,
                                   add_tuple_idx=add_tuple_idx,
                                   sort_dict_keys=sort_dict_keys
                                   )
                           )
            s2l.sort()
            for e in s2l:
                r += '%s\n' % (e)
            r += '%s)' % (level_str)
        else:
            r = '%s%s%s()' % (level_str, p, h)
    elif isinstance(obj, dict) or isinstance(obj, object):
        if isinstance(obj, dict):
            h: str = 'dict'
            keys: list = list(obj.keys())
            d: dict = obj
        else:
            h: str = 'attributes'
            p: str = '%sclass(%s)%s' % (p, obj.__class__.__name__, OBJ_PREFIX)
            d: dict = obj.__dict__
            keys: list = list(d.keys())
        if d:
            r = '%s%s%s(\n' % (level_str, p, h)
            if sort_dict_keys:
                keys.sort()
            for k in keys:
                r += '%s\n' % (objrepr(d[k],
                                       name='<%s>' % str(k),
                                       level=level + 1,
                                       add_list_idx=add_list_idx,
                                       add_tuple_idx=add_tuple_idx,
                                       sort_dict_keys=sort_dict_keys))
            r += '%s)' % (level_str)
        else:
            r = '%s%s%s()' % (level_str, p, h)
    else:
        r = '%s%sunknown(%s)' % (level_str, p, str(obj))
    return r


def value2dict(value):
    if value is None:
        r = None
    elif isinstance(value, str) \
            or isinstance(value, bool) \
            or isinstance(value, int) \
            or isinstance(value, float) \
            or isinstance(value, complex) \
            or isinstance(value, bytes) \
            or isinstance(value, bytearray)\
            or isinstance(value, range):
        r = value
    elif isinstance(value, list) \
            or isinstance(value, tuple) \
            or isinstance(value, set) \
            or isinstance(value, frozenset):
        r = []
        for e in value:
            r.append(value2dict(e))
        r = r
    elif isinstance(value, dict):
        r = {}
        for e in value:
            r[e] = value2dict(value[e])
        r = r
    elif isinstance(value, object):
        r = {}
        for attr_name in value.__dict__:
            r[attr_name] = value2dict(value.__dict__[attr_name])
    else:
        r = str(value)
    return r
