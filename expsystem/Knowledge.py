from expsystem.Fact import Fact


class Knowledge:
    def __init__(self, *args):
        self._facts = set(args)

    def add(self, *args):
        for fact in args:
            self._facts.add(fact)

    def add_fact(self, *args, **kwargs):
        self.add(Fact(*args, **kwargs))

    def clone(self):
        return Knowledge(*[fact.clone() for fact in self._facts])

    def __iter__(self):
        return iter(self._facts)

    def __str__(self):
        return str(self._facts)

    def __len__(self):
        return len(self._facts)

    def __sub__(self, other):
        return self._facts.difference(other._facts)

