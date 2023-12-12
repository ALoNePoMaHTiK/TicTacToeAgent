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
    #Цикл для правильного хода при возможной победе
    for index in free:
        tempMap = map[:index]+player + map[index+1:]
        rows = [tempMap[:3], tempMap[3:-3], tempMap[-3:],
                tempMap[::3], tempMap[1::3], tempMap[2::3],
                tempMap[0::4], tempMap[6:0:-2]]
        if any([row == 'XXX' for row in rows]):
            return map[:index] + player + map[index + 1:]
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

    iterationCount = 5000000
    checkNumber = 50000        #Каждые checkCount игр будет определен процент побед
    winners = []
    WinningLast = 0
    for i in range(iterationCount):
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
        if i%checkNumber==0 and i!=0:
            winners.append((la.Winning-WinningLast)/checkNumber*100)
            WinningLast= la.Winning
        print(f'#{i}')
    print(winners)
    la.saveAgent('Agent.csv')
    plt.plot(range(checkNumber,iterationCount,checkNumber),winners)
    plt.xlabel('Кол-во игр, тыс. шт.')
    plt.yticks(range(65,100,1))
    plt.xticks(range(checkNumber,iterationCount,iterationCount//20))
    plt.ylabel('Процент побед, %')
    plt.grid()
    plt.savefig('Learn.png')
    plt.show()

#TrainAgent()
playWithAgent()






