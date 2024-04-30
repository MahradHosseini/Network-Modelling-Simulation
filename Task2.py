import numpy as np

LAMBDA = 0.5


def generate_exponential(lambda_rate):
    U = np.random.uniform(0, 1)  # Generate a uniform random number
    return -np.log(U) / lambda_rate  # Apply the inverse transform


if __name__ == '__main__':
    np.random.seed(0)
    for n in range(0, 100):
        x = generate_exponential(LAMBDA)
        print(x)
