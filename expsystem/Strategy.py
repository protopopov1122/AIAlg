class FifoStrategy:
    def __init__(self, knowledge):
        self._knowledge = knowledge
        self._products = []

    def add(self, rule, product):
        if product is not None:
            self._products.append((rule, product))

    def is_finished(self):
        return len(self._products) > 0

    def get_knowledge(self):
        if len(self._products) == 0:
            return self._knowledge
        else:
            rule, product = self._products[0]
            return self._knowledge + product

    def get_activated_rules(self):
        if len(self._products) == 0:
            return list()
        else:
            rule, product = self._products[0]
            return [rule]


class AllInStrategy:
    def __init__(self, knowledge):
        self._knowledge = knowledge
        self._rules = list()

    def add(self, rule, product):
        if product is not None:
            self._knowledge += product
            self._rules.append(rule)

    def is_finished(self):
        return False

    def get_knowledge(self):
        return self._knowledge

    def get_activated_rules(self):
        return self._rules
