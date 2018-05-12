class Engine:
    def __init__(self, strategy, *args):
        self._strategy = strategy
        self._rules = list(args)

    def add_rule(self, rule):
        self._rules.append(rule)

    def process(self, knowledge):
        process = True
        rules: list = self._rules.copy()
        while process:
            start_len = len(knowledge)
            knowledge, rules = self._iterate(knowledge, rules)
            process = len(knowledge) > start_len and len(rules) > 0
        return knowledge

    def _iterate(self, knowledge, rules):
        strategy = self._strategy(knowledge)
        for rule in rules:
            res = rule(strategy.get_knowledge())
            if res is not None:
                strategy.add(rule, res['product'], **{key: value for key, value in res.items() if key != 'product'})
                if strategy.is_finished():
                    break
        activated_rules = strategy.get_activated_rules()
        return strategy.get_knowledge(), [rule for rule in rules if rule not in activated_rules]
