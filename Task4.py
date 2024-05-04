import math

'''
Write a program (in C, C++, Java, Python or C#) to simulate an M/M/c queuing system
(Poisson arrivals, exponentially distributed service times and single server). Assume a
quasi-birth and death model with state-independent arrival and service rates λ and µ,
respectively. Compute the average waiting time, the average waiting time of those who
wait, the utilisation, and the mean queue length.
'''


def mmc_queue_analytics(lambda_rate, mhu):
    c = 1  # c: number of servers in parallel
    # µ mhu: mean service rate = 1 / E[Service - Time]

    # traffic intensity
    p = lambda_rate / (c * mhu)

    # p_0 probability system (queue + servers) is empty
    val = 0
    for m in range(c):
        a = ((c * p) ** m) / math.factorial(m)
        b = ((c * p) ** c) / (math.factorial(c) * (1 - p))
        d = a + b
        val += d
    p_0 = 1 / val

    # Lq: mean number of customers in the queue
    l_queue = (p_0 * ((lambda_rate / mhu) ** c) * p) / (math.factorial(c) * ((1 - p) ** 2))

    # average waiting time for queue
    w_queue = l_queue / lambda_rate

    # average waiting time
    w = w_queue + (1 / mhu)

    return {
        'Utilization (ρ)': p,
        'Mean queue length': l_queue,
        'Average Response Time in the System (W)': w,
        'Average Waiting Time in the Queue (Wq)': w_queue
    }


if __name__ == '__main__':
    # Rates are as Customer per Unit Time
    lambda_input, mu_rate = 0.8, 1.0
    analytics = mmc_queue_analytics(lambda_input, mu_rate)

    for key, value in analytics.items():
        print(f'{key}: {value:.2f}')
