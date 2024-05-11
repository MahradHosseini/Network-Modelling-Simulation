import math
import random
import operator


class MMCSimulationServerFailure:
    def __init__(self, lambda_in, mhu_in, c_in, time_limit_in, ksi_in, eta_in):
        self.lambda_rate = lambda_in  # λ
        self.mhu = mhu_in  # μ
        self.c = c_in  # num of servers
        self.time_limit = time_limit_in  # how long sim should take
        self.clock = 0  # real time
        self.ksi = ksi_in  # mean breakdown rate
        self.eta = eta_in  # mean repair rate
        self.rho = None
        self.p_0 = None
        self.l_queue = None
        self.w_queue = None
        self.w = None

        self.busy_servers = []  # busy servers
        self.repairing_servers = []  # servers waiting for repair
        self.repaired_server = None  # current repaired server
        self.usable_servers = []  # free servers
        self.in_process_arrivals = []  # arrivals that in a server
        self.arrivals = []
        self.repairman = {'is_busy': False,
                          'server_id': None}
        self.servers = [{'free_operation_time': None,
                         'repair_time': None,
                         'id': i}
                        for i in range(self.c)]

    def generate_service_time(self):
        return random.expovariate(self.mhu)  # generate a single service time

    def generate_arrival_time(self):
        i = 0  # index for the arrivals
        time_index = 0  # time tracking
        while time_index < self.time_limit:  # while time limit isn't crossed
            arrival_time = time_index + random.expovariate(self.lambda_rate)  # arrival time is now + random
            if arrival_time > self.time_limit:  # if arrival time is greater than limit
                break  # leave
            self.arrivals.append({'time': arrival_time,
                                  'id': i,
                                  'service': 0,
                                  'server_id': None})  # append arrival
            time_index = arrival_time  # time index is the arrival of new
            i += 1  # index for arrival ++

    def print_arrivals(self):
        for arrival in self.arrivals:
            print(arrival['time'])

    def run_simulation(self):
        self.generate_arrival_time()
        self.usable_servers = self.servers.copy()  # generate arrivals
        self.clock = 0  # reset clock
        self.print_arrivals()
        while self.clock < self.time_limit and len(self.arrivals) != 0:  # while have time or events to process
            # next_arrival: mi time valued arrival in arrivals
            next_arrival = min(self.arrivals, key=lambda x: x['time']) if self.arrivals else None
            # next_failure_server: min free op timed server in busy_servers
            next_failure_server = min(self.busy_servers,
                                      key=operator.itemgetter('free_operation_time')) if self.busy_servers else None
            # next_repair: repair ending time
            next_repair = self.repaired_server if self.repaired_server else None
            # next_freed_server: min service timed in process arrival
            next_freed_server = min(self.in_process_arrivals,
                                    key=lambda x: x['service']) if self.in_process_arrivals else None

            arrival_time = next_arrival['time'] if next_arrival is not None else math.inf
            server_failure_time = next_failure_server[
                'free_operation_time'] if next_failure_server is not None else math.inf
            repair_time = next_repair['repair_time'] if next_repair is not None else math.inf
            freed_server_time = next_freed_server['service'] if next_freed_server is not None else math.inf
            '''print(arrival_time)
            print(server_failure_time)
            print(repair_time)
            print(freed_server_time)'''
            # finding next event
            next_event_time = min(arrival_time, server_failure_time, repair_time, freed_server_time)
            if next_event_time == math.inf:
                break
            print("time is: ", self.clock)
            # time is now at next event
            self.clock = next_event_time
            if self.clock == next_arrival['time']:  # if time is next_arrival
                if len(self.usable_servers) == 0:  # if no usable servers pass
                    print("no usable servers")
                    continue
                else:
                    print("arrived with id: ", next_arrival['id'])
                    server = self.usable_servers.pop(0)  # pop from usable servers
                    server['free_operation_time'] = (random.expovariate(self.ksi)
                                                     + self.clock)  # generate op time for server
                    print("server ", server['id'], " will operate until ",
                          server['free_operation_time'])
                    server['repair_time'] = None  # no need for repair
                    self.busy_servers.append(server)  # server added to busy_servers
                    next_arrival['service'] = self.generate_service_time()  # generated arrival service time
                    next_arrival['server_id'] = server['id']  # arrival's server id = server's
                    self.in_process_arrivals.append(next_arrival)  # append to in_process_arrivals
                    self.arrivals.remove(next_arrival)  # remove from arrivals

            elif self.clock == next_failure_server['free_operation_time']:  # if clock is freeOp time
                print("next_failure_server")
                self.busy_servers.remove(next_failure_server)  # remove from busy_servers
                next_failure_server['free_operation_time'] = None  # no freeOp time for that
                next_failure_server['repair_time'] = random.expovariate(self.eta)  # generate repair time
                # find index of arrival which server held
                index_val = next((index for index, arrival in enumerate(self.in_process_arrivals)
                                  if arrival['server_id'] == next_failure_server['id']), None)
                # new service time of the arrival is remaining now
                self.in_process_arrivals[index_val]['service'] = (
                        self.clock - self.in_process_arrivals[index_val]['time'])
                self.in_process_arrivals[index_val]['server_id'] = None  # arrival's server_id is None
                self.in_process_arrivals[index_val]['time'] = self.clock  # arrival time is clock
                self.arrivals.append(self.in_process_arrivals.pop(index_val))  # pop and append to arrivals
                if not self.repairman['is_busy']:  # if repairman is not busy
                    self.repairman['is_busy'] = True  # now busy
                    self.repairman['server_id'] = next_failure_server['id']  # repairman's server_id is id
                    self.repaired_server = next_failure_server  # repaired server is failure
                else:  # if repairman is busy
                    self.repairing_servers.append(next_failure_server)  # add failure to queue


            elif next_repair is not None and 'repair_time' in next_repair and self.clock == next_repair['repair_time']:
                print("next_repair")
                self.repaired_server['free_operation_time'] = (
                    random.expovariate(self.ksi))  # generate op time
                self.repaired_server['repair_time'] = None  # server doesn't need repair
                self.usable_servers.append(self.repaired_server)  # append server to usable
                if not self.repairing_servers:  # if no waiting repair
                    self.repairman['is_busy'] = False  # repairman free
                    self.repairman['server_id'] = None  # repairman has no server in
                else:  # if waiting repairs
                    server = self.repairing_servers.pop(0)  # pop FIFO
                    server['free_operation_time'] = 0  # free op time is zero
                    self.repaired_server = server  # server is now getting repaired


            elif next_freed_server is not None and 'free_operation_time' in next_freed_server and self.clock == \
                    next_freed_server['service']:
                print("nxt freed")
                next_freed_server['free_operation_time'] -= self.clock
                self.usable_servers.append(next_freed_server)
                self.in_process_arrivals = list(filter(lambda arrival: arrival['server_id'] != next_freed_server['id'],
                                                       self.in_process_arrivals))

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
ksi_rate = 0.001
eta_rate = 0.1
sim_time = 10

simulation = MMCSimulationServerFailure(lambda_rate, mhu, c, sim_time, ksi_rate, eta_rate)
simulation.run_simulation()
print("Utilization (ρ)", simulation.rho)
print("Mean queue length", simulation.l_queue)
print("Average Response Time in the System (W):", simulation.w)
print("Average waiting time for queue:", simulation.w_queue)
