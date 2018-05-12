def Rule(pattern, priority: int=0):
    def decorator(func):
        def wrapper(knowledge, *args, **kwargs):
            if pattern.matches(knowledge):
                complexity, match = pattern.match(knowledge)
                res = func(knowledge, *args, **kwargs)
                if type(res) == list or type(res) == tuple:
                    return {
                        'complexity': complexity,
                        'product': set(res),
                        'priority': priority
                    }
                elif res is not None:
                    rs = set()
                    rs.add(res)
                    return {
                        'complexity': complexity,
                        'product': rs,
                        'priority': priority
                    }
            return None
        wrapper.pattern = pattern
        return wrapper
    return decorator


def Product(pattern, *args, **kwargs):
    def fn(knowledge):
        return args
    if 'priority' in kwargs:
        return Rule(pattern, kwargs['priority'])(fn)
    else:
        return Rule(pattern)(fn)
