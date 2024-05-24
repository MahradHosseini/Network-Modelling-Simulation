import copy
import math
import random
import operator


class MMCSimulationServerFailureTask:

    def __init__(self, lambda_in, mhu_in, c_in, time_limit_in, ksi_in, eta_in):
        self.lambda_rate = lambda_in  # λ
        self.mhu = mhu_in  # μ
        self.c = c_in  # num of servers
        self.time_limit = time_limit_in  # how long sim should take
        self.clock = 0  # real time
        self.temp_time = 0
        self.ksi = ksi_in  # mean breakdown rate
        self.eta = eta_in  # mean repair rate
        self.rho = None
        self.p_0 = None
        self.l_queue = None
        self.w_queue = None
        self.w = None

        self.wait_list = []  # wait times
        self.busy_servers = []  # busy servers
        self.repairing_servers = []  # servers waiting for repair
        self.repaired_server = None  # current repaired server
        self.usable_servers = []  # free servers
        self.in_process_arrivals = []  # arrivals that are in a server
        self.arrivals = [{'time': 0,
                          'id': 0,
                          'service': 0,
                          'server_id': -1}]
        self.repairman = {'is_busy': False,
                          'server_id': None}
        self.servers = [{'free_operation_time': None,
                         'repair_time': None,
                         'id': i}
                        for i in range(self.c)]
        self.mean_arrival_time = None
        self.mean_service_time = 0
        self.num_of_service_times = 0

    def generate_service_time(self):
        value = random.expovariate(self.mhu)  # generate a single service time
        self.mean_service_time += value
        self.num_of_service_times += 1
        return value + self.clock

    def generate_arrival_time(self):
        i = 0                                                                   # index for the arrivals
        time_index = 0                                                          # time tracking
        while time_index < self.time_limit:                                     # while time limit isn't crossed
            arrival_time = random.expovariate(self.lambda_rate) + time_index    # arrival time is now + random
            if arrival_time > self.time_limit:                                  # if arrival time is greater than limit
                break                                                           # leave
            self.arrivals.append({'time': arrival_time,
                                  'id': i,
                                  'service': None,
                                  'server_id': None})                           # append the new arrival
            time_index = arrival_time                                           # time index is the arrival of new
            i += 1                                                              # index for arrival ++
        self.arrivals.sort(key=lambda x: x['time'])

    def print_arrivals(self):
        for arrival in self.arrivals:
            print("process arrival: ", arrival['time'])
            print("process length: ", arrival['service'])

    def run_simulation(self):
        self.generate_arrival_time()                # generate arrival times
        self.usable_servers = self.servers.copy()   # all servers are usable at first
        self.clock = 0                              # reset clock
        self.arrivals.pop(0)                        # remove initial dummy arrival

        while self.clock < self.time_limit or (self.arrivals or self.busy_servers or self.repairing_servers):
            next_arrival = min(self.arrivals, key=lambda x: x['time']) if self.arrivals else None
            next_failure_server = min(self.busy_servers, key=lambda x: x['free_operation_time']) if self.busy_servers else None
            next_repair = self.repaired_server if self.repaired_server else None
            next_freed_server = min(self.in_process_arrivals, key=lambda x: x['service']) if self.in_process_arrivals else None

            arrival_time = next_arrival['time'] if next_arrival is not None else math.inf
            server_failure_time = next_failure_server['free_operation_time'] if next_failure_server is not None else math.inf
            repair_time = next_repair['repair_time'] if next_repair is not None else math.inf
            freed_server_time = next_freed_server['service'] if next_freed_server is not None else math.inf

            next_event_time = min(arrival_time, server_failure_time, repair_time, freed_server_time)
            if len(self.usable_servers) != 0:
                if self.clock > next_event_time:
                    self.temp_time = next_event_time
                else:
                    self.clock = next_event_time
            else:
                self.clock = min(repair_time, freed_server_time, server_failure_time)

            if self.clock == arrival_time or self.temp_time == arrival_time:        # if time is next_arrival
                print("in arrival")
                if len(self.usable_servers) == 0:               # if no usable servers pass
                    print("no usable servers")
                    self.clock = min(repair_time, freed_server_time, server_failure_time)
                    continue
                else:
                    server = self.usable_servers.pop(0)         # pop from usable servers
                    server['free_operation_time'] = (random.expovariate(self.ksi)
                                                     + self.clock)  # generate op time for server
                    server['repair_time'] = None                # no need for repair
                    self.busy_servers.append(server)            # server added to busy_servers

                    arrival = self.arrivals.pop(0)
                    arrival['service'] = self.generate_service_time() + self.clock  # generated arrival service time
                    arrival['server_id'] = server['id']         # arrival's server id = server's
                    self.in_process_arrivals.append(arrival)    # append to in_process_arrivals
                    self.wait_list.append(self.clock - arrival['time'])

            elif (self.clock == next_failure_server['free_operation_time'] or self.temp_time ==
                  next_failure_server['free_operation_time']):  # if clock is freeOp time
                self.busy_servers.remove(next_failure_server)               # remove from busy_servers
                next_failure_server['free_operation_time'] = None           # no freeOp time for that
                next_failure_server['repair_time'] = random.expovariate(self.eta)  # generate repair time
                # find index of arrival which server held
                specific_arrival_obj = [arrival for arrival in self.arrivals if arrival['server_id']
                                        == next_failure_server['id']]
                index_val = next((index for index, arrival in enumerate(self.in_process_arrivals)
                                  if arrival['server_id'] == next_failure_server['id']), None)
                if index_val is not None:
                    # new service time of the arrival is remaining now
                    self.in_process_arrivals[index_val]['service'] = (
                            self.clock - self.in_process_arrivals[index_val]['time'])
                    self.in_process_arrivals[index_val]['server_id'] = None         # arrival's server_id is None
                    self.in_process_arrivals[index_val]['time'] = self.clock        # arrival time is clock
                    self.arrivals.append(self.in_process_arrivals.pop(index_val))   # pop and append to arrivals
                if not self.repairman['is_busy']:                               # if repairman is free
                    self.repairman['is_busy'] = True                            # now busy
                    self.repairman['server_id'] = next_failure_server['id']     # repairman's server_id is id
                    self.repaired_server = next_failure_server                  # repaired server is failure
                else:                                                           # if repairman is busy
                    self.repairing_servers.append(next_failure_server)          # add failure to queue

            elif (next_repair is not None and 'repair_time' in next_repair and self.clock == next_repair['repair_time']
                  or self.temp_time == next_repair):
                print("in repair finished")
                self.repaired_server['free_operation_time'] = (
                    random.expovariate(self.ksi))                               # generate op time
                self.repaired_server['repair_time'] = None                      # server doesn't need repair
                self.usable_servers.append(self.repaired_server)                # append server to usable
                if not self.repairing_servers:                                  # if no waiting repair
                    self.repairman['is_busy'] = False                           # repairman free
                    self.repairman['server_id'] = None                          # repairman has no server in
                else:                                                           # if waiting repairs
                    server = self.repairing_servers.pop(0)                      # pop FIFO
                    server['free_operation_time'] = 0                           # free op time is zero
                    self.repaired_server = server                               # server is now getting repaired

            elif next_freed_server is not None and 'service' in next_freed_server and self.clock == \
                    next_freed_server['service'] or self.temp_time == next_freed_server:
                print("in next freed server")

                arrival_server_id = next_freed_server['server_id']
                matching_server = next((server for server in self.busy_servers if server['id'] == arrival_server_id),
                                       None)

                matching_server['free_operation_time'] -= self.clock
                self.usable_servers.append(matching_server)

                self.in_process_arrivals = [arrival for arrival in self.in_process_arrivals if arrival['server_id'] !=
                                            arrival_server_id]
            self.temp_time = 0
            print(self.wait_list)
        self.calculations()

    def calculations(self):
        # average waiting times
        self.w_queue = sum(self.wait_list) / len(self.wait_list)
        # average waiting time for those who wait
        self.wait_list = [value for value in self.wait_list if value != 0.0]
        self.w = sum(self.wait_list) / len(self.wait_list)
        # new lambda
        self.lambda_rate = 1 / self.mean_arrival_time
        # mean service time
        self.mean_service_time = self.mean_service_time / self.num_of_service_times
        # new mhu
        self.mhu = 1 / self.mean_service_time
        # utilization / traffic intensity
        self.rho = self.lambda_rate / (self.c * self.mhu)
        # queue length calculations
        self.l_queue = self.lambda_rate * self.w_queues


lambda_rate = 0.8
mhu = 1
c = 2
ksi_rate = 0.001
eta_rate = 0.1
sim_time = 10

simulation = MMCSimulationServerFailureTask(lambda_rate, mhu, c, sim_time, ksi_rate, eta_rate)
simulation.run_simulation()
print("Utilization (ρ): ", simulation.rho)
print("lambda (λ): ", simulation.lambda_rate)
print("mhu (μ): ", simulation.mhu)
print("Mean Service Time: ", simulation.mean_service_time)
print("Mean queue length: ", simulation.l_queue)
print("Mean Waiting Time for Those Who Wait: ", simulation.w)
print("Mean Waiting Time: ", simulation.w_queue)
