import math
import random
import matplotlib
import matplotlib.pyplot as plt
from Erlang import *

m = 2  # мест в очереди
n = 3  # кол-во обработчиков
k = 2  # порядок экланга
l = 0.9  # (лямбда) интенсивность потока
mu = 0.1  # (мю) интенсивность обработчика


def addStream(a, b, c):
    if c:
        plt.plot([a, (b + a) / 2], [0, 1], color='blue')
        plt.plot([(b + a) / 2, b], [1, 0], color='blue')
    else:
        plt.plot([a, (b + a) / 2], [0, 1], color='red')
        plt.plot([(b + a) / 2, b], [1, 0], color='red')


# генерируем челов
stream = [[0, True]]
for i in range(20):
    stream.append([stream[len(stream) - 1][0] + rand(l, k), True])

# queue.append(1)
# del  queue[0]
obrabotka = [[0, stream[1][0]]] # при отрисовки делитнуть первый элемент
queue = [stream[1]] # первый чел в очереди это чел, которого мы обрабатываем
si = 1
while True:
    if si > len(stream)-2:
        break
    obrabotka.append([obrabotka[len(obrabotka) - 1][1],
                      obrabotka[len(obrabotka) - 1][1] + random.expovariate(mu)])  # обрабатываем текущего чела
    del queue[0] # чела обслужили
    while True: # смотрим всех челов, что пришли до конца последней обработки и добавляем в очередь
        if si > len(stream)-2:
            break
        si += 1
        # print("stream", stream[si][0])
        # print("obrabotka", obrabotka[len(obrabotka) - 1][1])
        if stream[si][0] < obrabotka[len(obrabotka) - 1][1]:
            if len(queue) >= m + 1:
                stream[si][1] = False
            else:
                queue.append(stream[si])
        else:
            break
    if len(queue) <= 0: # если в очереди никого нет, добавляем в обработку некст чела
        queue.append(stream[si])
    #фигарим в очередь до m+1 тех кто подошёл за время прошлого выполения потом, если равна 0, то фигарим туды следующую.


# Отрисовка
for i in range(1, len(stream)):
    addStream(stream[i - 1][0], stream[i][0], stream[i][1])
plt.ylim([-10,10])
matplotlib.pyplot.show()
