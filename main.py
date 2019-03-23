import random
import numpy as np
from time import sleep
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class Agent:
    def __init__(self, length):
        self.string = ''.join(str(random.randint(0,1)) for _ in xrange(length))
        self.fitness = -1

    def __str__(self):
        return 'String: ' + str(self.string) + ' Fitness: ' + str(self.fitness)

def funcInit(x, a, b, c, d, e ,f):
    return a + b*x + c*x**2 + d*x**3 + e*x**4 + f*x**5

def func(x,a,b,c,d,e,f,g):
    return \
    int(string[0])*a      + int(string[1])*b*x     + int(string[2])*c*x**2 + \
    int(string[3])*d*x**3 + int(string[4])*e*x**4  + int(string[5])*f*np.sin(x) + \
    int(string[6])*g*np.exp(g*x)

in_str = None
in_str_len = None
population = 6
generations = 50
threshold = 0.999

xdata = np.linspace(0, 6, 100)
y = funcInit(xdata, 50, 20, -9.5/2,0,0,0)
np.random.seed(42)
y_noise = 0.2 * np.random.normal(size=xdata.size)
ydata = y + y_noise

# Code to evolve
def ga():
    agents = init_agents(population, in_str_len)

    for generation in xrange(generations):
        print 'Generation: ' + str(generation)

        plt.plot(xdata, ydata, 'b-', linewidth=4, label='data')
        agents = fitness(agents)
        agents = selection(agents)
        agents = crossover(agents)
        agents = mutation(agents)

        plt.title('Generation %d' % (generation))
        plt.xlabel('x')
        plt.ylabel('y')
        #plt.legend()
        plt.ylim(0,80)
        plt.savefig('gen%d.png' % (generation), transparent=True)
        plt.show()

        if any(agent.fitness >= threshold for agent in agents):
            print 'k x x^2 x^3 x^4 sin exp'
            print 'Threshold has been met!'
            exit(0)

def init_agents(population, length):
    return [Agent(length) for _ in xrange(population)]

def fitness(agents):
    for agent in agents:
        global string
        string = agent.string
        popt, pcov = curve_fit(func, xdata, ydata)
        residuals = ydata - func(xdata, *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((ydata-np.mean(ydata))**2)
        r_squared = 1 - (ss_res / ss_tot)
        penalty = 1/(1+np.exp(5*(string.count('1') - len(string)+2)))
        fitness = r_squared * penalty
        agent.fitness = fitness

        if fitness > threshold:
            plt.plot(xdata, func(xdata, *popt), 'g-', linewidth=2, label='Fit: %5.4f'%(r_squared))
        else:
            plt.plot(xdata, func(xdata, *popt), 'r-', label='Fit: %5.4f'%(r_squared))

    return agents

def selection(agents):
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True)
    print '\n'.join(map(str, agents))

    # Natural selection
    kill_param = 0.2 # take the top 20% of the individuals
    agents = agents[:int(kill_param * len(agents))]
    return agents

def crossover(agents):
    offspring = []

    for _ in xrange((population - len(agents))/2):
        # TODO: don't breed parents that are the same
        parent1 = random.choice(agents)
        parent2 = random.choice(agents)

        child1 = Agent(in_str_len)
        child2 = Agent(in_str_len)
        split = random.randint(0,in_str_len)
        child1.string = parent1.string[0:split] + parent2.string[split:in_str_len]
        child2.string = parent2.string[0:split] + parent1.string[split:in_str_len]

        offspring.append(child1)
        offspring.append(child2)

    agents.extend(offspring)
    return agents

def mutation(agents):
    chance_of_mutation = 0.20
    for agent in agents:
        for idx, param in enumerate(agent.string):
            if random.uniform(0.0,1.0) <= chance_of_mutation:
                agent.string = agent.string[0:idx] + str(random.randint(0,1)) + agent.string[idx+1:in_str_len]
    return agents

if __name__ == '__main__':
    in_str = '1010010'
    in_str_len = len(in_str)
    ga()
