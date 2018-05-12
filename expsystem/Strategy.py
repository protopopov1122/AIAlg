import abc


class AbstractStrategy(abc.ABC):
    @abc.abstractmethod
    def add(self, rule, product, **params): pass

    @abc.abstractmethod
    def is_finished(self): pass

    @abc.abstractmethod
    def get_knowledge(self): pass

    @abc.abstractmethod
    def get_activated_rules(self): pass


class FifoStrategyFactory(AbstractStrategy):
    def __init__(self, knowledge, activate_all_rules: bool, finish_on_first: bool):
        self._knowledge = knowledge
        self._products = []
        self._finish_on_first = finish_on_first
        self._activate_all_rules = activate_all_rules

    def add(self, rule, product, **params):
        if product is not None:
            self._products.append((rule, product))

    def is_finished(self):
        return len(self._products) > 0 and self._finish_on_first

    def get_knowledge(self):
        if len(self._products) == 0:
            return self._knowledge
        else:
            rule, product = self._products[0]
            return self._knowledge + product

    def get_activated_rules(self):
        if len(self._products) == 0:
            return list()
        elif self._activate_all_rules:
            return [rule for rule, product in self._products]
        else:
            rule, product = self._products[0]
            return [rule]


def FifoStrategy(activate_all_rules: bool = False, finish_on_first: bool = True):
    def fn(knowledge):
        return FifoStrategyFactory(knowledge, activate_all_rules, finish_on_first)
    return fn


class AllInStrategy(AbstractStrategy):
    def __init__(self, knowledge):
        self._knowledge = knowledge
        self._rules = list()

    def add(self, rule, product, **params):
        if product is not None:
            self._knowledge += product
            self._rules.append(rule)

    def is_finished(self):
        return False

    def get_knowledge(self):
        return self._knowledge

    def get_activated_rules(self):
        return self._rules


class ComplexityBasedStrategyFactory(AbstractStrategy):
    def __init__(self, knowledge, reversed: bool = False):
        self._knowledge = knowledge
        self._products = list()
        self._reversed = reversed

    def add(self, rule, product, **params):
        if product:
            complexity = params['complexity'] if 'complexity' in params else 0
            self._products.append((rule, product, complexity))
            self._products.sort(key=lambda product: product[2], reverse=not self._reversed)

    def is_finished(self):
        return False

    def _get_opt_product(self):
        if self._products:
            return self._products[0]

    def get_knowledge(self):
        product = self._get_opt_product()
        if product:
            return self._knowledge + product[1]
        else:
            return self._knowledge

    def get_activated_rules(self):
        product = self._get_opt_product()
        if product:
            return [product[0]]
        else:
            return list()


def ComplexityBasedStrategy(reversed: bool = False):
    def fn(knowledge):
        return ComplexityBasedStrategyFactory(knowledge, reversed)
    return fn


class PriorityBasedStrategyFactory(AbstractStrategy):
    def __init__(self, knowledge, reversed: bool = False):
        self._knowledge = knowledge
        self._products = list()
        self._reversed = reversed

    def add(self, rule, product, **params):
        if product:
            priority = params['priority'] if 'priority' in params else 0
            self._products.append((rule, product, priority))
            self._products.sort(key=lambda product: product[2], reverse=self._reversed)

    def is_finished(self):
        return False

    def _get_opt_product(self):
        if self._products:
            return self._products[0]

    def get_knowledge(self):
        product = self._get_opt_product()
        if product:
            return self._knowledge + product[1]
        else:
            return self._knowledge

    def get_activated_rules(self):
        product = self._get_opt_product()
        if product:
            return [product[0]]
        else:
            return list()


def PriorityBasedStrategy(reversed: bool = False):
    def fn(knowledge):
        return PriorityBasedStrategyFactory(knowledge, reversed)
    return fn