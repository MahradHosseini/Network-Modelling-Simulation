import math

'''
Write a program (in C, C++, Java, Python or C#) to compute performance evaluation
measures (mean queue length, throughput, response time, etc.) of an M/M/c queuing
system (Poisson arrivals, exponentially distributed service times and a multi-server) analytically. 
Use well-known queuing theory formulae. Assume a quasi-birth and death model with state-independent 
arrival and service rates λ and µ, respectively.
'''


def mmc_queue_analytics(lambda_rate, mhu, c_value):
    if lambda_rate >= mu_rate:
        raise ValueError("The system is unstable, use a λ < µ")

    # traffic intensity
    p = lambda_rate / (c_value * mhu)

    # p_0 probability system (queue + servers) is empty
    val = 0
    for m in range(c_value):
        a = ((c_value * p) ** m) / math.factorial(m)
        b = ((c_value * p) ** c_value) / (math.factorial(c_value) * (1 - p))
        d = a + b
        val += d
    p_0 = 1 / val

    # Lq: mean number of customers in the queue
    l_queue = (p_0 * ((lambda_rate / mhu) ** c_value) * p) / (math.factorial(c_value) * ((1 - p) ** 2))

    # average waiting time for queue
    w_queue = l_queue / lambda_rate

    # average waiting time
    w = w_queue + (1 / mhu)

    return {
        'Utilization (ρ)': p,
        'Mean queue length': l_queue,
        'Average Response Time in the System (W)': w,
        'Average Waiting Time in the Queue (Wq)': w_queue,
        'Throughput (λ)': lambda_rate
    }


if __name__ == '__main__':
    lambda_input, mu_rate, c = 0.8, 1.0, 2
    analytics = mmc_queue_analytics(lambda_input, mu_rate, c)

    for key, value in analytics.items():
        print(f'{key}: {value:.2f}')

