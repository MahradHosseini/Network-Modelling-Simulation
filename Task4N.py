import math
import random

'''
Write a program (in C, C++, Java, Python or C#) to simulate an M/M/c queuing system
(Poisson arrivals, exponentially distributed service times and single server). Assume a
quasi-birth and death model with state-independent arrival and service rates λ and µ,
respectively. Compute the average waiting time, the average waiting time of those who
wait, the utilisation, and the mean queue length.
'''


class MMCSimulation:
    def __init__(self, lambda_in, mhu_in, c_in, time_limit_in):
        self.lambda_rate = lambda_in  # λ
        self.mhu = mhu_in  # μ
        self.c = c_in  # num of servers
        self.time_limit = time_limit_in  # how long sim should take
        self.clock = None  # real time
        self.services = []
        self.servers = []
        self.arrivals = []
        self.start = None
        self.rho = None
        self.p_0 = None
        self.l_queue = None
        self.w_queue = None
        self.w = None

    def generate_service_time(self):
        for _ in range(len(self.arrivals)):
            self.services.append(random.expovariate(self.mhu))

    def generate_arrival_time(self):
        while self.clock < self.time_limit:
            arrival_time = self.clock + random.expovariate(self.lambda_rate)
            if arrival_time > self.time_limit:
                break
            self.arrivals.append(arrival_time)
            self.clock = arrival_time

    def run_simulation(self):
        self.clock = 0
        self.generate_arrival_time()  # generate arrivals
        self.generate_service_time()
        while self.clock < self.time_limit and len(self.arrivals) !=0:
            if len(self.servers) == self.c:
                self.clock = min(self.servers)
                self.servers.remove(min(self.servers))
            else:
                self.clock += self.arrivals[0]
            service_time = self.services[0]
            departure_time = self.clock + service_time
            self.servers.append(departure_time)
            self.services.remove(service_time)

        self.calculations()

    def calculations(self):
        # traffic intensity
        self.rho = self.lambda_rate / (self.c * self.mhu)

        # p_0 probability system (queue + servers) is empty
        val = 0
        for m in range(self.c):
            a = ((self.c * self.rho) ** m) / math.factorial(m)
            b = ((self.c * self.rho) ** self.c) / (math.factorial(self.c) * (1 - self.rho))
            d = a + b
            val += d
        self.p_0 = 1 / val

        # Lq: mean number of customers in the queue
        self.l_queue = (self.p_0 * ((self.lambda_rate / self.mhu) ** self.c) * self.rho) / (
                math.factorial(self.c) * ((1 - self.rho) ** 2))

        # average waiting time for queue
        self.w_queue = self.l_queue / self.lambda_rate

        # average waiting time
        self.w = self.w_queue + (1 / self.mhu)


lambda_rate = 0.8
mhu = 1
c = 2
sim_time = 1000

simulation = MMCSimulation(lambda_rate, mhu, c, sim_time)
simulation.run_simulation()
print("Utilization (ρ)", simulation.rho)
print("Mean queue length", simulation.l_queue)
print("Average Response Time in the System (W):", simulation.w)
print("Average waiting time for queue:", simulation.w_queue)




