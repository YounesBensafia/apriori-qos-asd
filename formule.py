import numpy as np

def qos_asd(P_A_and_B, P_A_and_not_B, P_not_A_and_B, alpha=1.5, beta=1.0, epsilon=1e-5):
    numerator = P_A_and_B + epsilon
    denominator = alpha * P_A_and_not_B + beta * P_not_A_and_B + epsilon
    return np.log(abs(numerator / denominator))


alphas = [0.5, 1.0, 1.5, 2.0]
betas = [0.5, 1.0, 1.5, 2.0]