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
    def __init__(self, lambda_in, mhu_in, c_in, sim_time_in):
        self.lambda_rate = lambda_in  # λ
        self.mhu = mhu_in  # μ
        self.c = c_in  # num of servers
        self.sim_time = sim_time_in  # how long sim should take
        self.clock = None  # real time
        self.arrivals = []
        self.services = []
        self.servers = []
        self.start = None
        self.rho = None
        self.p_0 = None
        self.l_queue = None
        self.w_queue = None
        self.w = None

    def generate_arrival_time(self):
        a = 0
        while a < self.sim_time:
            a += random.expovariate(self.lambda_rate)
            self.arrivals.append(a)

    def generate_service_time(self):
        for _ in range(len(self.arrivals)):
            self.services.append(random.expovariate(self.mhu))

    def run_simulation(self):
        self.clock = 0
        self.generate_arrival_time()
        self.generate_service_time()
        while self.clock < self.sim_time:
            self.clock = self.arrivals[0]
            if len(self.servers) >= self.c:
                self.start = min(self.servers)
                self.servers.pop(0)
            else:
                self.start = self.arrivals[0]
            service_time = self.services[0]
            departure_time = self.start + service_time
            self.services.pop(0)
            self.servers.append(departure_time)
            self.arrivals.pop(0)
            if len(self.arrivals) == 0:
                break

            while len(self.servers) > 0:
                if min(self.servers) < self.arrivals[0]:
                    self.servers.remove(min(self.servers))
                else:
                    break
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
        return {
            'Utilization (ρ)': self.rho,
            'Mean queue length': self.l_queue,
            'Average Response Time in the System (W)': self.w,
            'Average Waiting Time in the Queue (Wq)': self.w_queue
        }


lambda_rate = 0.8
mhu = 1
c = 1
sim_time = 1000

simulation = MMCSimulation(lambda_rate, mhu, c, sim_time)
simulation.run_simulation()
simulation.calculations()
print("Utilization (ρ)", simulation.rho)
print("Mean queue length", simulation.l_queue)
print("Average Response Time in the System (W):", simulation.w)
print("Average waiting time for queue:", simulation.w_queue)
