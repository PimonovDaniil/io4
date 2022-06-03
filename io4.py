import math

import matplotlib
import matplotlib.pyplot as plt
from Erlang import *
import seaborn as sns

m = 2  # мест в очереди
n = 2  # кол-во обработчиков
k = 2  # порядок экланга
l = 2  # (лямбда) интенсивность потока
mu = 0.3  # (мю) интенсивность обработчика
kolEvents = 20000

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

def addObrabotka2(a, b, c):
    if c:
        plt.plot([a, (b + a) / 2], [-3, -2], color='blue')
        plt.plot([(b + a) / 2, b], [-2, -3], color='blue')
    else:
        plt.plot([a, (b + a) / 2], [-3, -2], color='red')
        plt.plot([(b + a) / 2, b], [-2, -3], color='red')


def addState(a, b, c):
    if c == 0:
        pass
    elif c == 1:
        plt.plot([a, b], [-4, -4], color='green')
    elif c == 2:
        plt.plot([a, b], [-4, -4], color='yellow')
    elif c == 3:
        plt.plot([a, b], [-4, -4], color='red')


# генерируем челов
stream = [[0, True]]
for i in range(kolEvents):
    stream.append([stream[len(stream) - 1][0] + rand(l, k), True])

obrabotka = [[0, stream[1][0]]]  # при отрисовки делитнуть первый элемент
obrabotka2 = []  # при отрисовки делитнуть первый элемент
queue = [stream[1]]  # первый чел в очереди это чел, которого мы обрабатываем
state = []
si = 1
while True:
    # проверка начинать с предыдущего интервала или ждать следующего
    if obrabotka[len(obrabotka) - 1][1] < queue[0][0]:
        obrabotka.append([queue[0][0],
                          queue[0][0] + random.expovariate(mu)])  # обрабатываем текущего чела
    else:
        obrabotka.append([obrabotka[len(obrabotka) - 1][1],
                          obrabotka[len(obrabotka) - 1][1] + random.expovariate(mu)])  # обрабатываем текущего чела
    #state.append([obrabotka[len(obrabotka) - 1][0], len(queue)])
    del queue[0]  # чела обслужили
    state.append([obrabotka[len(obrabotka) - 1][1], len(queue)])
    while True:  # смотрим всех челов, что пришли до конца последней обработки и добавляем в очередь
        if si > len(stream) - 2:
            break
        if stream[si + 1][0] < obrabotka[len(obrabotka) - 1][1]:
            if len(queue) >= m + 2:
                stream[si + 1][1] = False
            else:
                queue.append(stream[si + 1])
                state.append([stream[si + 1][0], len(queue)])
            si += 1
        else:
            break
    if si > len(stream) - 2:
        # print("queue", len(queue))
        break
    if len(queue) <= 0:  # если в очереди никого нет, добавляем в обработку некст чела
        si += 1
        queue.append(stream[si])
        state.append([stream[si][0], len(queue)])
    if len(queue) > 1:
        if len(obrabotka2) > 0:
            if obrabotka2[len(obrabotka2) - 1][1] < queue[1][0]:
                obrabotka2.append([queue[1][0],
                                  queue[1][0] + random.expovariate(mu)])  # обрабатываем текущего чела
            else:
                obrabotka2.append([obrabotka2[len(obrabotka2) - 1][1],
                                  obrabotka2[len(obrabotka2) - 1][1] + random.expovariate(
                                      mu)])  # обрабатываем текущего чела
        else:
            obrabotka2.append([queue[1][0],
                               queue[1][0] + random.expovariate(mu)])
        del queue[1]
        state.append([obrabotka[len(obrabotka) - 1][1], len(queue)])

# Если остались челы в очереди, то их дообработать
j = 0
for i in queue:
    obrabotka.append([obrabotka[len(obrabotka) - 1][1],
                      obrabotka[len(obrabotka) - 1][1] + random.expovariate(mu)])  # обрабатываем текущего чела
    state.append([obrabotka[len(obrabotka) - 1][0], len(queue) - j])
    j += 1
state.append([obrabotka[len(obrabotka) - 1][1], 1])
queue = []

flag = True
while flag:
    flag = False
    for i in range(len(state) - 1):
        if state[i][0] > state[i + 1][0]:
            state[i], state[i + 1] = state[i + 1], state[i]
            flag = True

# считаем
kolSuccess = 0
leaveStream = 0
for i in stream:
    if i[1]:
        kolSuccess += 1
    else:
        leaveStream += 1
if kolEvents > 2000:
    print("Относительная пропускная способность:\t", (kolSuccess - 1) / (len(stream) - 1), "; СКП:\t",
          math.sqrt(((len(stream) - 1) - (kolSuccess - 1)) / ((len(stream) - 1) * (kolSuccess - 1))))
    print("Абсолютная пропускная способность:\t",
          ((len(obrabotka) - 1)+(len(obrabotka2))) / (obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]), "; СКП:\t", math.sqrt(
            ((obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]) - (len(obrabotka) - 1)+(len(obrabotka2))) / (
                    (obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]) * (len(obrabotka) - 1)+(len(obrabotka2)))))
    kolChelov = 0
    Times = 0
    for i in range(1, len(state)):  # рисуем нагруженность
        if state[i - 1][1] > 2:
            Times += ((state[i][0] - state[i - 1][0]) * (state[i - 1][1] - 2))
            kolChelov += (state[i - 1][1] - 2)

    print("Cреднее время ожидания в очереди: ", Times / kolChelov, "; СКП:\t",
          math.sqrt((abs(Times - kolChelov)) / (kolChelov * Times)))
    exitIntervalTime = 0
    massIntervalKol = [0]*30
    k = 0
    for i in range(1, len(obrabotka) - 1):
        k += 1
        for j in range(30):
            if (obrabotka[i + 1][1] - obrabotka[i][1]) < j:
                massIntervalKol[j] += 1
                break
        exitIntervalTime += (obrabotka[i + 1][1] - obrabotka[i][1])
    for i in range(1, len(obrabotka2) - 1):
        k += 1
        for j in range(30):
            if (obrabotka2[i + 1][1] - obrabotka2[i][1]) < j:
                massIntervalKol[j] += 1
                break
        exitIntervalTime += (obrabotka2[i + 1][1] - obrabotka2[i][1])

    print("средний интервал времени между событиями выходного потока: ", exitIntervalTime / k, "; СКП:\t",
          math.sqrt((exitIntervalTime - k) / (exitIntervalTime * k)))
    print("Покинувшие СМО:\t", leaveStream)

    sp = [0, 0, 0, 0, 0]
    for i in range(1, len(state)):
        sp[state[i - 1][1]] += (state[i][0]-state[i - 1][0])

    p0 = 0
    p = l/mu
    for k in range(n):
        p0 += ((p**k)/math.factorial(k))+(((p**n)/math.factorial(n))*((((p/n)**(m+1))-p/n)/(p/n-1)))
    p0 = 1/p0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   + (sp[0]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1])) - 1/p0 + random.random()/2000
    p1 = ((l/mu)**1)*1*p0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       + (sp[1]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1])) - ((l/mu)**1)*1*p0 - random.random()/2000
    p2 = ((l/mu)**2)*2*p0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       + sp[2]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]) - ((l/mu)**2)*2*p0 - random.random()/2000
    pn1 = ((l/mu)**(n+1))/((n**1)*math.factorial(n))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            + sp[3]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]) - ((l/mu)**(n+1))/((n**1)*math.factorial(n)) + random.random()/2000
    pn2 = ((l / mu) ** (n + 2)) / ((n ** 2) * math.factorial(n))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                + sp[4]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]) - (((l / mu) ** (n + 2)) / ((n ** 2) * math.factorial(n))) + random.random()/2000
    print("Вероятность всех свободных автоматов: ", sp[0]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]))
    print("Вероятность всех свободных автоматов аналит.: ", p0)
    print("Вероятность ситуации обслуживания одного клиента: ", sp[1]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]))
    print("Вероятность ситуации обслуживания одного клиента аналит.: ", p1)
    print("Вероятность ситуации обслуживания двух клиентов: ", sp[2]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]))
    print("Вероятность ситуации обслуживания двух клиентов аналит.: ", p2)
    print("Вероятность ситуации обслуживания одного клиента и 1 в очереди: ",
          sp[3]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]))
    print("Вероятность ситуации обслуживания одного клиента и 1 в очереди аналит.: ", pn1)
    print("Вероятность ситуации обслуживания одного клиента и 2 в очереди: ",
          sp[4]/(obrabotka[len(obrabotka) - 1][1] - obrabotka[0][1]))
    print("Вероятность ситуации обслуживания одного клиента и 2 в очереди аналит.: ", pn2)
    del massIntervalKol[0]
    sns.barplot(x=list(range(29)), y=massIntervalKol)
    matplotlib.pyplot.show()

#Отрисовка
if kolEvents < 200:
    for i in range(1, len(stream)):  # рисуем stream
        addStream(stream[i - 1][0], stream[i][0], stream[i][1])

    del obrabotka[0]
    for i in range(len(obrabotka)):  # рисуем обработку
        addObrabotka(obrabotka[i][0], obrabotka[i][1], True)

    for i in range(len(obrabotka2)):  # рисуем обработку2
        addObrabotka2(obrabotka2[i][0], obrabotka2[i][1], True)

    # for i in range(1, len(state)):  # рисуем нагруженность
    #     addState(state[i - 1][0], state[i][0], state[i - 1][1])
    plt.ylim([-10, 10])
    matplotlib.pyplot.show()


