import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import math

def casson_model(gamma_dot, tau0, k):
    # Casson model: τ = (τ0^0.5 + (k * γ̇)^0.5)^2
    return (np.sqrt(tau0) + np.sqrt(k * gamma_dot)) ** 2

def fit_casson(shear_rates, shear_stresses, flow_rate=1, diameter=1, density=1, re_critical=4000):
    x = np.array(shear_rates)
    y = np.array(shear_stresses)

    try:
        popt, _ = curve_fit(casson_model, x, y, bounds=(0, np.inf), maxfev=10000)
        tau0, k = popt
    except Exception:
        tau0, k = 0, 0

    y_pred = casson_model(x, tau0, k)
    r2 = r2_score(y, y_pred)

    # Apparent viscosity: μ_app = τ / γ̇ using median γ̇
    gamma_median = np.median(x)
    tau_median = casson_model(np.array([gamma_median]), tau0, k)[0]
    mu_app = tau_median / gamma_median if gamma_median != 0 else 0

    # Reynolds number: Re = (ρ * v * D) / μ_app
    area = math.pi * (diameter ** 2) / 4
    velocity = flow_rate / area if area != 0 else 0
    re = (density * velocity * diameter) / mu_app if mu_app != 0 else 0

    # Critical flow rate: q_critical = (π·d²/4)·(Re_critical·μ_app / (ρ·d))
    if density != 0 and diameter != 0:
        q_critical = (math.pi * diameter ** 2 / 4) * (re_critical * mu_app / (density * diameter))
    else:
        q_critical = 0

    equation = f"√τ = √{tau0:.3f} + √({k:.3f}·γ̇)"


    return {
        "equation": equation,
        "tau0": round(float(tau0), 6),
        "k": round(float(k), 6),
        "n": 1,
        "r2": round(float(r2), 6),
        "mu_app": round(float(mu_app), 6),
        "re": round(float(re), 6),
        "re_critical": re_critical,
        "q_critical": round(float(q_critical), 6)
    }
