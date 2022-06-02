global seed
import random

random.seed(19) # 19

def rand(l, k):
    s = 0
    for i in range(k):
        s += random.expovariate(l)
    return s
