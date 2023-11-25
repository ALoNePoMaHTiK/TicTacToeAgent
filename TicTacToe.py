from itertools import product
from random import randint
import csv
import matplotlib.pyplot as plt

import LearningAgent

def out(row):
    print(f'\t┏━━━┓')
    print(f'\t┃{row[:3]}┃')
    print(f'\t┃{row[3:-3]}┃')
    print(f'\t┃{row[-3:]}┃')
    print(f'\t┗━━━┛')

def isEnd(map):
    rows = [map[:3], map[3:-3], map[-3:],
            map[::3], map[1::3], map[2::3],
            map[0::4], map[6:0:-2]]
    return any([row in ['XXX', 'OOO'] for row in rows]) or map.count(' ') == 0
def generateClearStateMatrixInFile():
    states = []
    for i in product(' XO',repeat=9):
        word = ''.join(i)
        value = 0.5
        if isEnd(word):
            value = 1.0
        states.append((len(states),word,value))
    with open('States.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=';')
        writer.writerows(states)
def generateClearStateMatrix():
    states = dict()
    for i in product(' XO', repeat=9):
        word = ''.join(i)
        value = 0.5
        if isEnd(word):
            value = 1.0
        states[word] =(len(states),value)
    return states

def getFree(map):
    free = []
    for i in range(len(map)):
        if map[i] == ' ':
            free.append(i)
    return free

def staticAgent(map:str):
    free = getFree(map)
    player = 'O' if map.count('X')>map.count('O') else 'X'
    index = free[randint(0,len(free)-1)]
    return map[:index]+player + map[index+1:]


la = LearningAgent.LearningAgent()
la.loadAgent('Agent.csv')
winners = []
WinningSum = 0
for i in range(10000):
    map = ' '*9
    while not isEnd(map):
        map = staticAgent(map)
        la.setMap(map)
        if isEnd(map):
            break
        la.step()
        map = la.map
    la.learn()
    la.restart()
    if i%50==0 and i!=0:
        winners.append(la.Winning-WinningSum)
        WinningSum+= la.Winning
    print(f'#{i}')

la.saveAgent()
plt.plot(winners)
plt.show()










