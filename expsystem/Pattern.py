from expsystem.Fact import FactBase, Fact
from expsystem.Match import Match


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

    @staticmethod
    def _eval_complexity(val):
        if isinstance(val, Match):
            return val.complexity()
        else:
            return 1

    def complexity(self):
        return sum(value for value in self._fact.values())

    def matches(self, knowledge):
        for fact in knowledge:
            if self == fact:
                return True
        return False

    def match(self, knowledge):
        for fact in knowledge:
            if self == fact:
                return sum(Pattern._eval_complexity(value) for value in fact._fact.values()), fact
        return -1, None


class AndPattern(PatternBase):
    def __init__(self, *args):
        super().__init__()
        self._patterns = args

    def complexity(self):
        return max(patt.complexity() for patt in self._patterns)

    def matches(self, knowledge):
        for pattern in self._patterns:
            if not pattern.matches(knowledge):
                return False
        return True

    def match(self, knowledge):
        match = list()
        complexity = 0
        for pattern in self._patterns:
            m = pattern.match(knowledge)
            if m[1] is None:
                return -1, None
            else:
                if len(m[1]) > 0:
                    match.append(m)
                complexity += m[0]
        return complexity, match

    def __str__(self):
        return ' & '.join(str(p) for p in self._patterns)


class OrPattern(PatternBase):
    def __init__(self, *args):
        super().__init__()
        self._patterns = args

    def complexity(self):
        return min(patt.complexity() for patt in self._patterns)

    def matches(self, knowledge):
        for pattern in self._patterns:
            if pattern.matches(knowledge):
                return True
        return False

    def match(self, knowledge):
        match = -1, None
        for pattern in self._patterns:
            m = pattern.match(knowledge)
            if m[1] is not None:
                if len(m[1]) > 0 and (match[0] == -1 or m[0] < match[0]):
                    match = m
                elif m[0] > 0 and (match[0] == -1 or m[0] < match[0]):
                    match = m
        return match

    def __str__(self):
        return ' | '.join(str(p) for p in self._patterns)


class NotPattern(PatternBase):
    def __init__(self, pattern: Pattern):
        super().__init__()
        self._pattern = pattern

    def complexity(self):
        return self._pattern.complexity()

    def matches(self, knowledge):
        return not self._pattern.matches(knowledge)

    def match(self, knowledge):
        return self.complexity(), Fact()

    def __str__(self):
        return '~{}'.format(self._pattern)
