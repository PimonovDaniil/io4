global seed
import random

# random.seed(0)

def rand(l, k):
    s = 0
    for i in range(k):
        s += random.expovariate(l)
    return s
