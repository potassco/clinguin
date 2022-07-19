import sys
from clingo import parse_term, Control

ctl = Control()

for f in sys.argv[1:]:
    ctl.load(str(f))

dynamic_shows = '''
#show.
#external only_brave.
#show _brave(X):_brave(X), only_brave.
#external only_cautious.
#show _cautious(X):_cautious(X), only_cautious.
'''

ctl.add("base","",dynamic_shows)
ctl.ground([("base",[])])
assumptions= ["assign(1,red)"] #Selected by the user

# Collect brave
ctl.assign_external(parse_term('only_brave'),True)
ctl.configuration.solve.enum_mode = 'brave'
with ctl.solve(assumptions=[(parse_term(a),True) for a in assumptions],
                yield_=True) as result:
    brave_model = None
    for m in result:
        brave_model  = [a.arguments[0] for a in m.symbols(shown=True)]

    for a in brave_model:
        print(f"{a}.")

# Collect cautious
ctl.assign_external(parse_term('only_brave'),False)
ctl.assign_external(parse_term('only_cautious'),True)
ctl.configuration.solve.enum_mode = 'cautious'
with ctl.solve(assumptions=[(parse_term(a),True) for a in assumptions],
                yield_=True) as result:
    cautious_model = None
    for m in result:
        cautious_model  = [a.arguments[0] for a in m.symbols(shown=True)]

    for a in cautious_model:
        print(f"{a}.")
        