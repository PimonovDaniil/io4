import math
import random
from Erlang import *

m = 2  # мест в очереди
n = 3  # кол-во обработчиков
k = 2  # порядок экланга
l = 0.5  # (лямбда) интенсивность потока
mu = 0.4  # (мю) интенсивность обработчика
queue = []
stream = [0]
for i in range(10):
    stream.append(stream[len(stream)-1] + rand(l, k))
print(stream)

# queue.append(1)
# queue.append(2)
# queue.append(3)
# print(queue)
# del  queue[0]
# print(queue)

