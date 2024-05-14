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
        self.clock = 0          # real time
        self.services = []      # service times
        self.servers = []       # servers
        self.arrivals = []      # arrival times
        self.wait_list = []     # wait times
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
        self.generate_arrival_time()  # generate arrivals
        self.generate_service_time()  # generate service times
        self.clock = 0  # clock is 0
        while self.clock < self.time_limit and (len(self.arrivals) != 0 or len(self.servers) != 0):
            if len(self.servers) == self.c:                                 # if servers are busy
                self.clock = min(self.servers)                                  # time is when it is free
                self.servers.remove(min(self.servers))                          # remove server from busy
            else:                                                           # if there are free servers
                if len(self.arrivals) != 0:
                    if self.clock <= self.arrivals[0]:                              # if the time is before the arrival
                        self.clock = self.arrivals.pop(0)                           # make it new arrival's
                        self.wait_list.append(0)
                    else:                                                       # if time == or > than the arrival
                        self.wait_list.append(self.clock - self.arrivals[0])
                        self.arrivals.pop(0)                                        # just pop and do not touch time
                    service_time = self.services.pop(0)                         # service time is taken
                    departure_time = self.clock + service_time                  # departure is clock + service
                    self.servers.append(departure_time)                         # append to servers
                else:
                    break
            # if len(self.arrivals) != 0:
                # print("next arrival: ", self.arrivals[0])
            # print("time is now: ", self.clock)
            # print("servers are: ", self.servers)
        # print("wait-list: ", self.wait_list)
        self.calculations()

    def calculations(self):
        # average waiting times
        self.w_queue = sum(self.wait_list)/len(self.wait_list)
        self.w = self.w_queue - (1/self.lambda_rate)

        # utilization / traffic intensity
        self.rho = self.lambda_rate / (self.c * self.mhu)

        # queue length calculations
        self.l_queue = self.lambda_rate*self.w_queue

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
