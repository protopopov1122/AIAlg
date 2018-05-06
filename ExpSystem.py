from expsystem.Fact import Fact
from expsystem.Pattern import Pattern
from expsystem.Match import Match
from expsystem.Rule import Rule
from expsystem.Knowledge import Knowledge
from expsystem.Engine import Engine


@Rule(Pattern(light='green'))
def rule1(knowledge, match):
    knowledge.add_fact('can_cross', cauntion=False)


@Rule(Pattern(light='yellow') & Pattern(has_cars=False))
def rule2(knowledge, match):
    knowledge.add_fact('can_cross', cauntion=True)


@Rule(Pattern('risky') & Pattern(peds=Match.smart(lambda x: x < 5)) & Pattern(light=Match.any_of('green', 'yellow')))
def rule5(knowledge, match):
    knowledge.add(Fact('break_the_rules'))


@Rule(Pattern(light=Match.any_of('green', 'yellow')) & ~Pattern('break_the_rules'))
def rule3(knowledge, match):
    knowledge.add_fact(can_drive=False)


@Rule(Pattern('break_the_rules'))
def rule6(knowledge, match):
    knowledge.add_fact(can_drive=True)


@Rule(Pattern(light='red'))
def rule4(knowledge, match):
    knowledge.add(Fact('can_drive'))
    knowledge.add(Fact(can_cross=True))


def main():
    knowledge = Knowledge(Fact(light='green'), Fact(has_cars=True), Fact(peds=4), Fact(risky=False))
    eng = Engine(rule1, rule2, rule5, rule4, rule3, rule6)
    print(eng.process(knowledge) - knowledge)


if __name__ == '__main__':
    main()
