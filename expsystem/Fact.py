import types
from expsystem.Error import ExpSystemException
from expsystem.Match import Match


class FactBase:
    def __init__(self, restrict_matches: bool, name: str, *args, **kwargs):
        self._fact = dict()
        self._name = name
        for value in args:
            if restrict_matches and isinstance(value, Match):
                raise ExpSystemException('Matches are restricted')
            self._fact[value] = True
        for key, value in kwargs.items():
            if restrict_matches and isinstance(value, Match):
                raise ExpSystemException('Matches are restricted')
            self._fact[key] = value

    def overlaps(self, fact):
        for key in fact._fact.keys():
            if key not in self._fact:
                return False
        return True

    def __getattr__(self, item):
        if item in self._fact:
            return self._fact[item]
        else:
            return None

    def __getitem__(self, item):
        if item in self._fact:
            return self._fact[item]
        else:
            return None

    def __contains__(self, item):
        return item in self._fact

    def __str__(self):
        return '{} {}'.format(self._name, str(self._fact))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        for key, value in self._fact.items():
            if key not in other._fact:
                return False
            if (isinstance(value, types.LambdaType) and not value(other._fact[key])) or \
                    (not isinstance(value, types.LambdaType) and value != other._fact[key]):
                return False
        return True

    def __hash__(self):
        res = 0
        for key, value in self._fact.items():
            res += hash(key) + hash(value) * 29
            res *= 31
        return res

    def __len__(self):
        return len(self._fact)


class Fact(FactBase):
    def __init__(self, *args, **kwargs):
        super().__init__(True, 'Fact', *args, **kwargs)

    def clone(self):
        return Fact(**self._fact)
