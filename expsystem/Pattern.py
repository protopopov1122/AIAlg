from expsystem.Fact import FactBase


class PatternBase:
    def And(self, other):
        return AndPattern(self, other)

    def Or(self, other):
        return OrPattern(self, other)

    def Not(self):
        return NotPattern(self)

    def __or__(self, other):
        return self.Or(other)

    def __and__(self, other):
        return self.And(other)

    def __invert__(self):
        return self.Not()

    def __repr__(self):
        return str(self)


class Pattern(PatternBase, FactBase):
    def __init__(self, *args, **kwargs):
        FactBase.__init__(self, False, 'Pattern', *args, **kwargs)
        PatternBase.__init__(self)

    def matches(self, knowledge):
        for fact in knowledge:
            if self == fact:
                return True
        return False

    def match(self, knowledge):
        for fact in knowledge:
            if self == fact:
                return fact
        return None


class AndPattern(PatternBase):
    def __init__(self, *args):
        super().__init__()
        self._patterns = args

    def matches(self, knowledge):
        for pattern in self._patterns:
            if not pattern.matches(knowledge):
                return False
        return True

    def match(self, knowledge):
        match = list()
        for pattern in self._patterns:
            m = pattern.match(knowledge)
            if m is None:
                return None
            match.append(m)
        return match

    def __str__(self):
        return ' & '.join(str(p) for p in self._patterns)


class OrPattern(PatternBase):
    def __init__(self, *args):
        super().__init__()
        self._patterns = args

    def matches(self, knowledge):
        for pattern in self._patterns:
            if pattern.matches(knowledge):
                return True
        return False

    def match(self, knowledge):
        for pattern in self._patterns:
            match = pattern.match(knowledge)
            if match is not None:
                return match
        return None

    def __str__(self):
        return ' | '.join(str(p) for p in self._patterns)


class NotPattern(PatternBase):
    def __init__(self, pattern: Pattern):
        super().__init__()
        self._pattern = pattern

    def matches(self, knowledge):
        return not self._pattern.matches(knowledge)

    def match(self, knowledge):
        if not self._pattern.matches(knowledge):
            return self._pattern.match(knowledge)
        else:
            return None

    def __str__(self):
        return '~{}'.format(self._pattern)
