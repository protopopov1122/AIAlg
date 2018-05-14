from expsystem.Fact import Fact


class Knowledge:
    def __init__(self, *args):
        self._facts = set(args)

    def add(self, *args):
        arr = [arg for arg in args if arg is not None]
        def check_overlap(fact, facts):
            for f in facts:
                if f.overlaps(fact):
                    return True
            return False
        facts = [fact for fact in self._facts if not check_overlap(fact, arr)]
        facts.extend(arr)
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
            return self.add(*other._facts)
        elif type(other) == set:
            return self.add(*other)
        elif type(other) == list:
            return self.add(*other)
        else:
            return self.add(other)

    def __sub__(self, other):
        return Knowledge(*list(self._facts.difference(other._facts)))

