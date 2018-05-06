class Engine:
    def __init__(self, *args):
        self._rules = list(args)

    def add_rule(self, rule):
        self._rules.append(rule)

    def process(self, knowledge):
        knowledge_copy = knowledge.clone()
        process = True
        while process:
            process = False
            start_len = len(knowledge_copy)
            for rule in self._rules:
                rule(knowledge_copy)
            process = process or len(knowledge_copy) > start_len
        return knowledge_copy
