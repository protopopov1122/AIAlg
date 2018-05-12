from expsystem.Fact import Fact
from expsystem.Pattern import Pattern
from expsystem.Match import Match
from expsystem.Rule import Rule, Product
from expsystem.Knowledge import Knowledge
from expsystem.Engine import Engine
from expsystem.Strategy import FifoStrategy, AllInStrategy


@Rule(Pattern(light='green'))
def rule1(knowledge, match):
    return Fact('can_cross', cauntion=False)


@Rule(Pattern(light='yellow') & Pattern(has_cars=False))
def rule2(knowledge, match):
    return Fact('can_cross', cauntion=True)


@Rule(Pattern('risky') & Pattern(peds=Match.smart(lambda x: x < 5)) & Pattern(light=Match.any_of('green', 'yellow')))
def rule5(knowledge, match):
    return Fact('break_the_rules')


@Rule(Pattern(light=Match.any_of('green', 'yellow')) & ~Pattern('break_the_rules'))
def rule3(knowledge, match):
    return Fact(can_drive=False)


@Rule(Pattern(light='red'))
def rule4(knowledge, match):
    return Fact('can_drive'), Fact(can_cross=True)


def main():
    knowledge = Knowledge(Fact(light='green'), Fact(has_cars=True), Fact(peds=4), Fact(risky=True))
    rule6 = Product(Pattern('break_the_rules'), Fact(can_drive=True))
    eng = Engine(FifoStrategy, rule1, rule2, rule5, rule4, rule3, rule6)
    print(eng.process(knowledge) - knowledge)


if __name__ == '__main__':
    main()
