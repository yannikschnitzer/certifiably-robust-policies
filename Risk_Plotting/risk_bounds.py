import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.stats import binom
from scipy.optimize import bisect

def binom_cdf_diff(p, n, k, alpha):
    """
    Computes the difference between the binomial CDF and the given threshold alpha.

    Parameters:
        p (float): Probability of success.
        n (int): Number of trials.
        k (int): Number of successes.
        alpha (float): Threshold value.

    Returns:
        float: Difference between the CDF and alpha.
    """
    return binom.cdf(k, n, p) - alpha

def compute_optimal_risk(n, gamma, eta):
    """
    Computes the optimal risk bound (epsilon) for a given sample size and parameters.

    Parameters:
        n (int): Number of verification samples.
        gamma (float): Failure probability of individual verification.
        eta (float): Desired reliability level (1 - eta).

    Returns:
        float: Optimal risk bound (epsilon).
    """
    min_epsilon = 1
    optimal_k = 0

    for k in range(max(1, int(n * 0.7)), n + 1):
        p = 1 - binom.cdf(k, n, 1 - gamma)
        if p < 1 - eta:
            continue

        beta = p - (1 - eta)
        epsilon = bisect(binom_cdf_diff, 0, 1, args=(n, n - k, beta))

        if epsilon < min_epsilon:
            min_epsilon = epsilon
            optimal_k = k

    print(f"N: {n}, K: {optimal_k}, Risk Bound (epsilon): {min_epsilon}")
    return min_epsilon

def compute_optimal_risk_with_discard(n, max_discard, gamma, eta):
    """
    Computes the optimal risk bound (epsilon) with discarded samples.

    Parameters:
        n (int): Total number of samples.
        max_discard (int): Maximum number of discarded samples.
        gamma (float): Failure probability of individual verification.
        eta (float): Desired reliability level (1 - eta).

    Returns:
        float: Optimal risk bound (epsilon).
    """
    min_epsilon = 1

    for k in range(max(1, int(n * 0.7)), n + 1 - max_discard):
        p = 1 - binom.cdf(k, n - max_discard, 1 - gamma)
        if p < 1 - eta:
            continue

        beta = p - (1 - eta)
        epsilon = bisect(binom_cdf_diff, 0, 1, args=(n, n - k, beta))

        if epsilon < min_epsilon:
            min_epsilon = epsilon

    print(f"N: {n}, Risk Bound (epsilon): {min_epsilon}")
    return min_epsilon

def compute_risks(N, gamma, eta, discarding=False):
    """
    Computes the risk bounds over a range of sample sizes.

    Parameters:
        N (int): Maximum number of samples.
        gamma (float): Failure probability of individual verification.
        eta (float): Desired reliability level (1 - eta).
        discarding (bool): Whether to include discarded samples.

    Returns:
        tuple: Sample sizes and corresponding risk bounds.
    """
    sample_sizes = []
    risks = []

    print("\n Computing risks according to Theorems 1/2 with Gamma =",gamma, "Eta =", eta)
    for n in (range(4, N + 1, 20) if discarding else range(1, N + 1)):
        sample_sizes.append(n)
        if discarding:
            max_discard = max(0, int(0.05 * n - 1))
            risks.append(compute_optimal_risk_with_discard(n, max_discard, gamma, eta))
        else:
            risks.append(compute_optimal_risk(n, gamma, eta))

    return sample_sizes, risks

def plot_risk_bounds(gamma, etas, N, discarding=False):
    """
    Plots the risk bounds for varying sample sizes and reliability levels.

    Parameters:
        gamma (float): Failure probability of individual verification.
        etas (list): List of reliability levels (1 - eta).
        N (int): Maximum number of samples.
        discarding (bool): Whether to include discarded samples.
    """
    xs = []
    ys = []

    for eta in etas:
        x, y = compute_risks(N, gamma, eta, discarding)
        xs.append(x)
        if not discarding:
            ys.append(gaussian_filter1d(y, sigma=6))
        else: 
            ys.append(gaussian_filter1d(y, sigma=0.5))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

    plt.figure(figsize=(7, 3))

    for i, eta in enumerate(etas):
        plt.plot(xs[i], ys[i], label=f'$1-\\eta$ = {eta}', color=colors[i], linewidth=3.5)

    plt.legend(loc='upper right', frameon=True, fontsize=14)
    plt.ylim(0, 0.6)
    plt.xlim(0, N)
    plt.xlabel('Verification Samples $N$', fontsize=18)
    plt.ylabel(r'Risk Bound $\varepsilon$', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.grid(visible=True, linestyle="--", color="lightgray", linewidth=0.6)

    if discarding:
        plt.axhline(y=0.05, color='gray', linestyle='--')

    if not os.path.exists("risk_plots"):
        os.mkdir("risk_plots")
    plt.savefig(f'risk_plots/risk_discarding={discarding}.pdf', format="pdf", bbox_inches="tight")

if __name__ == "__main__":
    GAMMA = 0.0001
    ETAS = [0.1, 0.01, 0.001]
    N = 501

    print("Plotting risk bounds without discarding:")
    plot_risk_bounds(GAMMA, ETAS, N, discarding=False)

    print("\nPlotting risk bounds with discarding:")
    plot_risk_bounds(GAMMA, ETAS, N, discarding=True)