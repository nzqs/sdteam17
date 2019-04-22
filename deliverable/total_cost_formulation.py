import torch
from random import random, shuffle
from statistics import mean

# Dummy data
# data = [8,4,6,7,8,6,10,9,11,4,3,5,8,9,4,6,12,4,7,10]
# data = [5,5,5,100,100,100,100,100,100,100,100]
# data = [random()*10 for i in range(30)]
data = [5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0,50.0]

p = torch.tensor(mean(data), requires_grad = True)
shuffle(data)
X = torch.tensor(data, requires_grad = True)
# X = torch.tensor([7,7,7,7,7,1])

# Parameters
theta = 300 # Downtime cost/hr
delta = 20 # Excess out cost/hr
learning_rate = 1e-6 # Should never see Xi > 50 or so
epochs = 500

def calc_cost(p, X, theta, delta, simple = True):
    Ei = lambda Xi: max(p - Xi, 0)
    Ti = lambda Xi: max(Xi - p, 0)
    D = []
    O = [0] # Allow O_0 to be 0
    for i, Xi in enumerate(X):
        D.append(max(Ei(Xi) - O[i], 0))
        O.append(max(O[i] + Ti(Xi) - Ei(Xi), 0))
    cost = sum(theta * D + delta * O)
    if simple:
        return cost
    else:
        return cost, D, O

for iteration in range(epochs):
    loss = calc_cost(p, X, theta, delta)
    if iteration % 10 == 0:
        print(iteration, loss)
    loss.backward() # Calculate gradients

    with torch.no_grad():
        p -= learning_rate * p.grad

    p.grad.zero_() # Reset gradients

print("Final p: %s" % p)
print(calc_cost(20, X, theta, delta))
print(calc_cost(mean(data), X, theta, delta))
print(calc_cost(p, X, theta, delta))
print(calc_cost(28, X, theta, delta))
print(mean(data))
