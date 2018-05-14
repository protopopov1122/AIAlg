import types


def Rule(pattern=None, priority: int=0):
    def decorator(func):
        def wrapper(knowledge, *args, **kwargs):
            if pattern is None or pattern.matches(knowledge):
                match = pattern.match(knowledge) if pattern is not None else []
                res = func(knowledge, match, *args, **kwargs)
                if type(res) == list or type(res) == tuple:
                    return {
                        'match': match,
                        'product': set(res),
                        'priority': priority
                    }
                elif res is not None:
                    rs = set()
                    rs.add(res)
                    return {
                        'match': match,
                        'product': rs,
                        'priority': priority
                    }
        wrapper.pattern = pattern
        return wrapper
    return decorator


def Product(pattern, *args, **kwargs):
    def fn(knowledge, match):
        def eval_arg(arg):
            if isinstance(arg, types.LambdaType):
                return arg(knowledge, match)
            else:
                return arg
        return [eval_arg(arg) for arg in args]
    if 'priority' in kwargs:
        return Rule(pattern, kwargs['priority'])(fn)
    else:
        return Rule(pattern)(fn)
