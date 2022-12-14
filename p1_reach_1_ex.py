from dtpc import DTPCGame
import itertools

states = list(range(6))
p1_acts = ['-', 'a', 'b', 'c']
p2_acts = ['-', 'D', 'E']
actions = itertools.product(p1_acts, p2_acts)

gamma_1 = {
    0: ['a', 'b', 'c'],
    1: ['-'],
    2: ['a'],
    3: ['-'],
    4: ['-'],
    5: ['-']
}

gamma_2 = {
    0: ['D', 'E', '-'],
    1: ['-'],
    2: ['D', 'E'],
    3: ['-'],
    4: ['-'],
    5: ['D', 'E'],
}

gamma = [gamma_1, gamma_2]

trans_dict = {
    0: {('b','D') : 1, ('c','-') : 1, ('a','D') : 2, ('b', 'E') : 2, ('a', 'E') : 3},
    1: {('-', '-') : 1},
    2: {('a','D') : 4, ('a','E') : 5},
    3: {('-', '-') : 3},
    4: {('-', '-') : 4},
    5: {('-','E') : 3, ('-','D') : 5}
}


game = DTPCGame(actions=actions, trans_dict=trans_dict, start_state=0, y=[gamma_1, gamma_2])

win, pi = game.asw_reach(player=0, final={1})
print(win)
print(pi)