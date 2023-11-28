import os
from random import randint
import matplotlib.pyplot as plt

import LearningAgent

def out(row):
    print(f' ┏━━━┓')
    print(f' ┃{row[:3]}┃')
    print(f' ┃{row[3:-3]}┃')
    print(f' ┃{row[-3:]}┃')
    print(f' ┗━━━┛')

# Определение завершенности игры
def isEnd(map):
    rows = [map[:3], map[3:-3], map[-3:],
            map[::3], map[1::3], map[2::3],
            map[0::4], map[6:0:-2]]
    return any([row in ['XXX', 'OOO'] for row in rows]) or map.count(' ') == 0

# Получение индексов пустых полей
def getFree(map):
    free = []
    for i in range(len(map)):
        if map[i] == ' ':
            free.append(i)
    return free

# Случайный ход крестиком
def staticAgent(map:str):
    free = getFree(map)
    player = 'O' if map.count('X')>map.count('O') else 'X'
    index = free[randint(0,len(free)-1)]
    return map[:index]+player + map[index+1:]

# Игра с агентом
def playWithAgent():
    la = LearningAgent.LearningAgent()
    la.loadAgent('Agent.csv')
    map = ' ' * 9
    free = getFree(map)
    step = -1
    while not isEnd(map):
        while step not in free:
            out(map)
            step = int(input())
            os.system('cls')
        map = map[:step] + 'X' + map[step+1:]
        step = -1
        out(map)
        if isEnd(map):
            break
        la.setMap(map)
        la.step()
        map = la.map
        os.system('cls')

# Тренировка агента
def TrainAgent():
    la = LearningAgent.LearningAgent()
    if os.path.exists('Agent.csv'):
        la.loadAgent('Agent.csv')
    winners = []
    WinningLast = 0
    for i in range(10000000):
        map = ' '*9
        while not isEnd(map):
            map = staticAgent(map)
            if isEnd(map):
                break
            la.setMap(map)
            la.step()
            map = la.map
        la.learn()
        la.restart()
        if i%50000==0 and i!=0:
            winners.append((la.Winning-WinningLast)/50000*100)
            WinningLast= la.Winning
        print(f'#{i}')
    print(winners)
    la.saveAgent('Agent.csv')
    plt.plot(winners)
    plt.savefig('Learn.png')
    plt.show()

#TrainAgent()
playWithAgent()







