import csv
from itertools import product


class LearningAgent():

    def __init__(self):
        self.leaningMatrix = self.generateClearStateMatrix()
        self.steps = []
        self.map = ''
        self.player = 'O'
        self.Winning = 0

    #Определение завершения игры
    #Если winnerCheck==True, то определяет победил ли агент
    def isEnd(self,map,winnerCheck=False):
        rows = [map[:3], map[3:-3], map[-3:],
                map[::3], map[1::3], map[2::3],
                map[0::4], map[6:0:-2]]
        if winnerCheck:
            return any([row in [self.player*3] for row in rows])
        return any([row in ['XXX','OOO'] for row in rows])

    def generateClearStateMatrix(self):
        states = dict()
        for i in product(' XO', repeat=9):
            word = ''.join(i)
            value = 0.5
            if self.isEnd(word):
                value = 1.0
            states[word] = (len(states), value)
        return states

    def setMap(self,map):
        self.map = map

    def getFree(self):
        free = []
        for i in range(len(self.map)):
            if self.map[i] == ' ':
                free.append(i)
        return free

    def step(self):
        free = self.getFree()
        value = 0
        preferedState = ''
        for index in free:
            state = self.map[:index] + self.player + self.map[index + 1:]
            stateValue = self.leaningMatrix[state]
            if stateValue[1] > value:
                value = stateValue[1]
                preferedState = state
        self.steps.append((preferedState))
        self.map = preferedState

    def saveAgent(self):
        with open('Agent.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for state in self.leaningMatrix.keys():
                value = self.leaningMatrix[state]
                writer.writerow((state,value[0],value[1]))

    def loadAgent(self,path):
        with open(path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=';')
            for state in reader:
                self.leaningMatrix[state[0]] = (int(state[1]),float(state[2]))
    def restart(self):
        self.steps = []

    def learn(self):
        isWinner = self.isEnd(self.map,winnerCheck=True)
        self.Winning += int(isWinner)
        valueDiff = 0.1 if isWinner else 0
        for step in self.steps:
            #print(step,end='->')
            temp = self.leaningMatrix[step]
            self.leaningMatrix[step] = (temp[0],temp[1]+valueDiff)