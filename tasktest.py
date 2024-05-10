import math
import random
import operator


class MMCSimulationServerFailure:
    def __init__(self, lambda_in, mhu_in, c_in, time_limit_in, ksi_in, eta_in):
        self.lambda_rate = lambda_in  # λ
        self.mhu = mhu_in  # μ
        self.c = c_in  # num of servers
        self.time_limit = time_limit_in  # how long sim should take
        self.clock = None  # real time
        self.ksi = ksi_in  # mean breakdown rate
        self.eta = eta_in  # mean repair rate
        self.rho = None
        self.p_0 = None
        self.l_queue = None
        self.w_queue = None
        self.w = None

        self.busy_servers = []  # busy servers
        self.repairing_servers = []  # servers waiting for repair
        self.repaired_server = None
        self.usable_servers = []  # free servers
        self.arrivals = [{'time': None,
                          'id': None,
                          'service': None}]  # arrivals
        self.repairman = {'is_busy': 0,
                          'server_id': None}
        self.servers = [[{'free_operation_time': None,
                          'repair_time': None,
                          'id': i}
                         for i in range(self.c)]]

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

    def run_simulation(self):
        self.clock = 0
        self.generate_arrival_time()  # generate arrivals
        self.generate_service_time()  # generate service times
        while self.clock < self.time_limit and len(self.arrivals) != 0:  # while have time and arrivals are not empty
            next_arrival = min(self.arrivals)  # gets min arrival time
            next_failure_server = min(self.busy_servers, key=operator.itemgetter(0))  # gets min free time
            next_repair = self.repairing_servers[
                'repair_time']  # DÜZELT repairing artık bir list ve repair sırası bekleyenleri temsil ediyor

            self.clock = min(next_arrival, next_failure_server, next_repair)  # time is first upcoming event

            if self.clock == next_arrival:
                if len(self.usable_servers) == 0:
                    continue
                else:
                    server = self.usable_servers[0]
                    self.usable_servers.pop(0)
                    self.busy_servers.append(server)

            elif self.clock == next_failure_server:
                location = next((index for index, server in enumerate(self.busy_servers) if
                                 server['free_operation_time'] == next_failure_server), None)
                server = self.busy_servers.pop(location)
                server['free_operation_time'] = 0
                server['repair_time'] = random.expovariate(self.eta) + self.clock
                if self.repairman['is_busy'] == 0:
                    self.repairman['is_busy'] = 1
                    self.repairman['server_id'] = server['id']
                else:
                    self.repairing_servers.append(server)

            elif self.clock == next_repair:
                self.repaired_server['free_operation_time'] = random.expovariate(self.ksi) + self.clock
                self.usable_servers.append(self.repaired_server)
                if len(self.repairing_servers) == 0:
                    self.repairman['is_busy'] = 0
                    self.repairman['server_id'] = None
                else:
                    server = self.repairing_servers.pop(0)
                    server['repair_time'] = random.expovariate(self.eta) + self.clock

        self.calculations()


lambda_rate = 0.8
mhu = 1
c = 2
ksi_rate = 0.001
eta_rate = 0.1
sim_time = 1000

simulation = MMCSimulationServerFailure(lambda_rate, mhu, c, sim_time, ksi_rate, eta_rate)
simulation.run_simulation()
print("Utilization (ρ)", simulation.rho)
print("Mean queue length", simulation.l_queue)
print("Average Response Time in the System (W):", simulation.w)
print("Average waiting time for queue:", simulation.w_queue)