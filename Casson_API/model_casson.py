import numpy as np
from scipy.optimize import curve_fit
import math

def casson_model(gamma, tau_y, k):
    return np.square(np.sqrt(tau_y) + np.sqrt(k * gamma))

def fit_casson_model(shear_rates, shear_stresses, flow_rate, diameter, density):
    gamma = np.array(shear_rates)
    tau = np.array(shear_stresses)

    try:
        popt, _ = curve_fit(casson_model, gamma, tau, bounds=(0, np.inf), maxfev=10000)
        tau_y, k = popt
        predictions = casson_model(gamma, tau_y, k)
        residuals = tau - predictions
        ss_res = np.sum(residuals ** 2)
        ss_tot = np.sum((tau - np.mean(tau)) ** 2)
        r2 = 1 - (ss_res / ss_tot)
    except:
        tau_y, k, r2 = 0.0, 0.0, 0.0

    mu_app = predictions[-1] / gamma[-1] if gamma[-1] != 0 else 1.0
    mu = mu_app

    if flow_rate > 0 and diameter > 0 and density > 0:
        Q = flow_rate
        D = diameter
        rho = density
        Re = (4 * rho * Q) / (np.pi * D * mu)
    else:
        Re = None

    return {
        "model": "Casson",
        "tau0": tau_y,
        "k": k,
        "n": 1.0,
        "r2": r2,
        "mu_app": mu_app,
        "mu": mu,
        "re": Re,
        "equation": "τ² = τ₀² + 2·η·γ̇"
    }
