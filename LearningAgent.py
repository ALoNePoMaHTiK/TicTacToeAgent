import csv
from itertools import product

WIN = 'Win'
FAIL = 'Fail'
DEAD = 'Dead'

class LearningAgent():

    def __init__(self):
        self.leaningMatrix = self.generateClearStateMatrix()
        self.steps = []
        self.map = ''
        self.player = 'O'
        self.Winning = 0 

    #Получение результата игры
    def getGameResult(self):
        rows = [self.map[:3], self.map[3:-3], self.map[-3:],
                self.map[::3], self.map[1::3], self.map[2::3],
                self.map[0::4], self.map[6:0:-2]]
        if any([row in [self.player*3] for row in rows]):
            return WIN
        elif any([row in ['XXX'] for row in rows]):     #Подумать над строгостью Х
            return FAIL
        else:
            return DEAD

    # Генерация стандартной матрицы состояний
    def generateClearStateMatrix(self):
        states = dict()
        for i in product(' XO', repeat=9):
            word = ''.join(i)
            value = 0.5
            states[word] = (len(states), value)
        return states

    # Сеттер для карты
    def setMap(self,map):
        self.map = map

    # Получение индексов пустых полей
    def getFree(self):
        free = []
        for i in range(len(self.map)):
            if self.map[i] == ' ':
                free.append(i)
        return free

    # Ход на основании матрицы состояний
    def step(self):
        free = self.getFree()
        value = -1
        preferedState = ''
        for index in free:
            state = self.map[:index] + self.player + self.map[index + 1:]
            stateValue = self.leaningMatrix[state]
            if stateValue[1] > value:
                value = stateValue[1]
                preferedState = state
        self.steps.append(preferedState)
        self.map = preferedState

    # Сохранение агента в файл
    def saveAgent(self,path):
        with open(path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for state in self.leaningMatrix.keys():
                value = self.leaningMatrix[state]
                writer.writerow((state,value[0],value[1]))

    # Загрузка агента из файла
    def loadAgent(self,path):
        with open(path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=';')
            for state in reader:
                self.leaningMatrix[state[0]] = (int(state[1]),float(state[2]))

    # Сброс шагов игры
    def restart(self):
        self.steps = []

    # Обучение на основании шагов и результата
    def learn(self):
        result = self.getGameResult()
        if result == WIN:
            self.Winning += 1
        for step in self.steps:
            temp = self.leaningMatrix[step]
            self.leaningMatrix[step] = (temp[0],temp[1]+0.4*((result==WIN)-temp[1]))