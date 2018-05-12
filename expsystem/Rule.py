def Rule(pattern):
    def decorator(func):
        def wrapper(knowledge, *args, **kwargs):
            if pattern.matches(knowledge):
                match = pattern.match(knowledge)
                res = func(knowledge, match=match, *args, **kwargs)
                if type(res) == list or type(res) == tuple:
                    return match[0], set(res)
                elif res is not None:
                    rs = set()
                    rs.add(res)
                    return match[0], rs
            return -1, None
        wrapper.pattern = pattern
        return wrapper
    return decorator


def Product(pattern, *args):
    def fn(knowledge, match):
        return args
    return Rule(pattern)(fn)
