from expsystem.Fact import Fact
from expsystem.Pattern import Pattern
from expsystem.Match import Match
from expsystem.Rule import Rule, Product
from expsystem.Knowledge import Knowledge
from expsystem.Engine import Engine
from expsystem.Strategy import FifoStrategy


def is_int(val):
    try:
        res = int(val)
        return True
    except:
        return False


def input_variant(prompt: str, min: int, max: int)->int:
    while True:
        res = input('{} [{}-{}]: '.format(prompt, min, max))
        if not is_int(res):
            print('Enter a number')
        else:
            ires = int(res)
            if ires < min or ires > max:
                print('Out of range')
            else:
                return ires


def input_boolean(prompt: str)->bool:
    while True:
        res = input('{} [Y/N]: '.format(prompt))
        if res in ['y', 'Y']:
            return True
        elif res in ['n', 'N']:
            return False
        else:
            print('Enter Y(es) or N(o)')


def input_fact(prompt: str, facts)->Fact:
    for index, fact in enumerate(facts):
        print('{}.\t{}'.format(index + 1, fact[0]))
    res = input_variant(prompt, 1, len(facts)) - 1
    return facts[res][1]


def decision(text):
    return lambda k, m: print(text)


@Rule()
def query_application_type(knowledge, match):
    app_types = [
        ('Embedded', Fact(application='embedded')),
        ('Desktop', Fact(application='desktop')),
        ('Backend', Fact(application='backend'))
    ]
    print('Application types:')
    return input_fact('Select type', app_types)


@Rule(Pattern(application=Match.any_of('embedded', 'desktop')) | Pattern(backend='microservices'))
def query_performance(knowledge, match):
    return Fact(performance='critical' if input_boolean('Is performance critical?') else 'moderate')


@Rule((Pattern(application='embedded') & Pattern(performance='critical')) | (Pattern(application='desktop') & ~Pattern(performance='critical')))
def query_portability(knowledge, match):
    return Fact(portable=input_boolean('Is portability a priority?'))


@Rule(Pattern(application='backend'))
def query_backend_type(knowledge, match):
    backend_types = [
        ('Microservices', Fact(backend='microservices')),
        ('Server-side page generation', Fact(backend='serverside')),
        ('Complex solutions', Fact(backend='complex'))
    ]
    print('Backend application types:')
    return input_fact('Select', backend_types)


@Rule(Pattern(backend='complex'))
def query_backend_platform(knowledge, match):
    backend_platforms = [
        ('Multiplatform', Fact(backend_platform='multi')),
        ('Windows Server', Fact(backend_platform='win'))
    ]
    return input_fact('Select platform', backend_platforms)


@Rule(Pattern(application='desktop') & Pattern(performance='critical'))
def desktop_type(knowledge, match):
    print('What is it?')
    desktop_types = [
        ('Game', Fact(desktop='game')),
        ('Rendering & graphics', Fact(desktop='graphics')),
        ('Mathematics & calculations', Fact(desktop='math'))
    ]
    return input_fact('Select', desktop_types)


@Rule(Pattern(application='desktop') & ~Pattern('portable'))
def query_desktop_app_type(knowledge, match):
    print('It is strange to restrict portability')
    return Fact(desktop='system_util' if input_boolean('Is it system utility UI?') else 'anything')


def main():
    knowledge = Knowledge()
    rules = [
        query_application_type,
        query_performance,
        Product(Pattern(application='embedded') & Pattern(performance='moderate'), decision('You should use Python 3 with Raspberry Pi')),
        query_portability,
        Product(Pattern(application='embedded') & Pattern(performance='critical') & Pattern('portable'), decision('Then you should use strict ISO C99')),
        Product(Pattern(application='embedded') & Pattern(performance='critical') & ~Pattern('portable'), decision('You may use the last C standard and all compiler extensions, as well as inline assembly')),
        query_backend_type,
        Product(Pattern(backend='microservices') & Pattern(performance='critical'), decision('You should use NodeJS with proper scaling')),
        Product(Pattern(backend='microservices') & Pattern(performance='moderate'), decision('You may use Python 3 with Aiohttp or Flask')),
        Product(Pattern(backend='serverside'), decision('You may pick a modern PHP with Lavarel')),
        query_backend_platform,
        Product(Pattern(backend_platform='multi'), decision('Then Java and Spring are for you')),
        Product(Pattern(backend_platform='win'), decision('Use C# with .NET Framework')),
        desktop_type,
        Product(Pattern(desktop='game'), decision('Just Unity. With C# of course')),
        Product(Pattern(desktop='graphics'), decision('C++ and Vulkan will rock')),
        Product(Pattern(desktop='math'), decision('Use existing math libraries on C/C++ or even Fortran. And a lightweight graphics library')),
        Product(Pattern(application='desktop') & Pattern('portable'), decision('Use HTML/JS/CSS. Then wrap it by Elecron and Phonegap.')),
        query_desktop_app_type,
        Product(Pattern(desktop='system_util'), decision('Use your system toolkits. Xlib for Linux, WinAPI for Windows, Cocoa for macOS')),
        Product(Pattern(desktop='anything'), decision('Pick a QT, GTK, wxWidgets. You even use them with some scripting languages'))
    ]
    engine = Engine(FifoStrategy(), *rules)
    print('New facts: {}'.format(engine.process(knowledge) - knowledge))


if __name__ == '__main__':
    main()
