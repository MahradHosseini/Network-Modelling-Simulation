import math


def mmc_queue_analytics():
    c = 1  # c: number of servers in parallel
    lambda_rate = 2
    mhu = 1  # µ mhu: mean service rate = 1 / E[Service - Time]

    # traffic intensity
    p = lambda_rate / (c * mhu)

    # p_0 probability system (queue + servers) is empty
    val = 0
    for m in range(c - 1):
        a = ((c * p) ** m) / math.factorial(m)
        b = ((c * p) ** c) / (math.factorial(c) * (1 - p))
        c = a + b
        val += c
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
