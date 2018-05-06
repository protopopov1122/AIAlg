def Rule(pattern):
    def decorator(func):
        def wrapper(knowledge, *args, **kwargs):
            if pattern.matches(knowledge):
                match = pattern.match(knowledge)
                res = func(knowledge, match=match, *args, **kwargs)
            else:
                return None
        return wrapper
    return decorator
