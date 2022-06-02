import math
import random
import matplotlib
import matplotlib.pyplot as plt
from Erlang import *

m = 2  # мест в очереди
n = 3  # кол-во обработчиков
k = 2  # порядок экланга
l = 0.5  # (лямбда) интенсивность потока
mu = 0.3  # (мю) интенсивность обработчика


def addStream(a, b, c):
    if c:
        plt.plot([a, (b + a) / 2], [0, 1], color='blue')
        plt.plot([(b + a) / 2, b], [1, 0], color='blue')
    else:
        plt.plot([a, (b + a) / 2], [0, 1], color='red')
        plt.plot([(b + a) / 2, b], [1, 0], color='red')


def addObrabotka(a, b, c):
    if c:
        plt.plot([a, (b + a) / 2], [-2, -1], color='blue')
        plt.plot([(b + a) / 2, b], [-1, -2], color='blue')
    else:
        plt.plot([a, (b + a) / 2], [-2, -1], color='red')
        plt.plot([(b + a) / 2, b], [-1, -2], color='red')


# генерируем челов
stream = [[0, True]]
for i in range(5):
    stream.append([stream[len(stream) - 1][0] + rand(l, k), True])

# queue.append(1)
# del  queue[0]
obrabotka = [[0, stream[1][0]]]  # при отрисовки делитнуть первый элемент
queue = [stream[1]]  # первый чел в очереди это чел, которого мы обрабатываем
si = 1
while True:
    if obrabotka[len(obrabotka) - 1][1] < queue[0][0]:
        obrabotka.append([queue[0][0],
                          queue[0][0] + random.expovariate(mu)])  # обрабатываем текущего чела
    else:
        obrabotka.append([obrabotka[len(obrabotka) - 1][1],
                          obrabotka[len(obrabotka) - 1][1] + random.expovariate(mu)])  # обрабатываем текущего чела
    del queue[0]  # чела обслужили
    while True:  # смотрим всех челов, что пришли до конца последней обработки и добавляем в очередь
        if si > len(stream) - 2:
            print("queue", len(queue))
            break
        if stream[si + 1][0] < obrabotka[len(obrabotka) - 1][1]:
            if len(queue) >= m + 1:
                stream[si + 1][1] = False
            else:
                queue.append(stream[si + 1])
            si += 1
        else:
            break
    if si > len(stream) - 2:
        print("queue", len(queue))
        break
    if len(queue) <= 0:  # если в очереди никого нет, добавляем в обработку некст чела
        si += 1
        queue.append(stream[si])
# Если остались челы в очереди, то их дообработать
for i in queue:
    obrabotka.append([obrabotka[len(obrabotka) - 1][1],
                      obrabotka[len(obrabotka) - 1][1] + random.expovariate(mu)])  # обрабатываем текущего чела
queue = []


# Отрисовка
for i in range(1, len(stream)):  # рисуем stream
    addStream(stream[i - 1][0], stream[i][0], stream[i][1])

del obrabotka[0]
for i in range(len(obrabotka)):  # рисуем stream
    addObrabotka(obrabotka[i][0], obrabotka[i][1], True)

plt.ylim([-10, 10])
matplotlib.pyplot.show()
