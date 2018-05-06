class Match:
    def __eq__(self, other):
        return self.matches(other)

    def __repr__(self):
        return str(self)

    @staticmethod
    def exact(value = True):
        return ExactMatch(value)

    @staticmethod
    def any_of(*args):
        return AnyOfMatch(args)

    @staticmethod
    def exists():
        return ExistsMatch()

    @staticmethod
    def smart(cond):
        return SmartMatch(cond)


class ExactMatch(Match):
    def __init__(self, value=True):
        self._value = value

    def matches(self, value):
        return value == self._value

    def __str__(self):
        return str(self._value)


class AnyOfMatch(Match):
    def __init__(self, values: list):
        self._values = values

    def matches(self, value):
        return value in self._values

    def __str__(self):
        return str(self._values)


class SmartMatch(Match):
    def __init__(self, condition):
        self._cond = condition

    def matches(self, value):
        return self._cond(value)

    def __str__(self):
        return 'SmartMatch'


class ExistsMatch(Match):
    def matches(self, value):
        return True

    def __str__(self):
        return '*'