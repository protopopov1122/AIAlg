import abc
from expsystem.Fact import FactBase
from expsystem.Match import Match


class PatternMatch(list):
    def __getattr__(self, item):
        return self.__dict__[item]

    def __setattr__(self, key, value):
        self.__dict__[key] = value


class PatternBase(abc.ABC):
    def And(self, other):
        return AndPattern(self, other)

    def Or(self, other):
        return OrPattern(self, other)

    def Not(self):
        return NotPattern(self)

    @abc.abstractmethod
    def complexity(self): pass

    @abc.abstractmethod
    def matches(self, knowledge): pass

    @abc.abstractmethod
    def match(self, knowledge): pass

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
        return sum(self._eval_complexity(value) for value in self._fact.values())

    def matches(self, knowledge):
        for fact in knowledge:
            if self == fact:
                return True
        return False

    def match(self, knowledge):
        for fact in knowledge:
            if self == fact:
                match = PatternMatch()
                match.append(fact)
                match.complexity = sum(Pattern._eval_complexity(value) for value in fact._fact.values())
                return match


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
        match = PatternMatch()
        match.complexity = 0
        for pattern in self._patterns:
            pmatch = pattern.match(knowledge)
            if pmatch is not None:
                match.complexity += pmatch.complexity
                match.extend(pmatch)
            else:
                return
        return match

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
        for pattern in self._patterns:
            match = pattern.match(knowledge)
            if match is not None:
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
        match = PatternMatch()
        match.complexity = self.complexity()
        return match

    def __str__(self):
        return '~{}'.format(self._pattern)
