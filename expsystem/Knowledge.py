from expsystem.Fact import Fact


class Knowledge:
    def __init__(self, *args):
        self._facts = set(args)

    def add(self, *args):
        facts = list(self._facts)
        facts.extend(args)
        return Knowledge(*facts)

    def add_fact(self, *args, **kwargs):
        return self.add(Fact(*args, **kwargs))

    def clone(self):
        return Knowledge(*[fact.clone() for fact in self._facts])

    def __iter__(self):
        return iter(self._facts)

    def __str__(self):
        return str(self._facts)

    def __len__(self):
        return len(self._facts)

    def __add__(self, other):
        facts: set = self._facts.copy()
        if isinstance(other, Knowledge):
            facts = facts.union(other._facts)
        elif type(other) == set:
            facts = facts.union(other)
        elif type(other) == list:
            facts = facts.union(set(other))
        else:
            facts.add(other)
        return Knowledge(*facts)

    def __sub__(self, other):
        return Knowledge(*list(self._facts.difference(other._facts)))

