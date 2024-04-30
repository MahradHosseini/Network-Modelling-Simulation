def mm1_queue_analytics(lambda_rate, mu_rate):
    if lambda_rate >= mu_rate:
        raise ValueError("The system is unstable, use a λ < µ")

    # Utilization (P or rho)
    rho = lambda_rate / mu_rate

    # Mean Queue Length (L)
    L = rho / (1 - rho)

    # Mean Customers in Queue (Lq)
    Lq = L * rho

    # Avg Response Time (W)
    W = 1 / (mu_rate - lambda_rate)

    # Avg Wait Time in Queue (Wq)
    Wq = Lq / lambda_rate

    # Throughput (theta)
    theta = lambda_rate  # TODO

    return {
        'Utilization (ρ)': rho,
        'Mean Queue Length (L)': L,
        'Mean Number in Queue (Lq)': Lq,
        'Throughput (theta)': theta,
        'Average Response Time in the System (W)': W,
        'Average Waiting Time in the Queue (Wq)': Wq
    }


if __name__ == '__main__':
    # Rates are as Customer per Unit Time
    lambda_rate, mu_rate = 0.8, 1.0
    analytics = mm1_queue_analytics(lambda_rate, mu_rate)

    for key, value in analytics.items():
        print(f'{key}: {value:.2f}')
