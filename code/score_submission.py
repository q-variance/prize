# scoring/score_submission.py 
# One single R² for the entire dataset (all stocks, all T)
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import json
from datetime import datetime

# The universal quantum law: variance = σ₀² + z²/2
def qvar(z, sigma0):
    return sigma0**2 + z**2 / 2

def compute_qvar_score(df, submission_name="Submission", author="Anonymous"):
    """
    df: prize_dataset.parquet loaded as DataFrame
        Must contain columns: ['ticker', 'date', 'T', 'z', 'sigma']
    Returns ONE global R² across ALL data points
    """
    # Convert volatility → variance
    data = df.copy()
    data["var"] = data["sigma"] ** 2

    print(f"Total data points: {len(data):,}")

    # Fixed binning
    zmax = 0.6
    delz = 0.025
    nbins = int(2 * zmax / delz + 1)
    bins = np.linspace(-zmax, zmax, nbins)

    # Bin ALL data together (this is the key)
    data["z_bin"] = pd.cut(data["z"], bins=bins, include_lowest=True)
    binned = (data.groupby("z_bin")
                 .agg(z_mid=("z", "mean"), var=("var", "mean"))
                 .dropna()
                 .reset_index(drop=True))

    print(f"Populated bins: {len(binned)}")

    if len(binned) < 10:
        r2_global = 0.0
        sigma0 = np.nan
    else:
        try:
            popt, _ = curve_fit(qvar, binned.z_mid.values, binned.var.values, p0=[0.08])
            sigma0 = popt[0]
            predicted = qvar(binned.z_mid.values, sigma0)
            ss_res = np.sum((binned.var - predicted)**2)
            ss_tot = np.sum((binned.var - binned.var.mean())**2)
            r2_global = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
        except Exception as e:
            print(f"Fit failed: {e}")
            r2_global = 0.0
            sigma0 = np.nan

    score = {
        "submission": submission_name,
        "author": author,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_points": len(data),
        "global_r2": round(r2_global, 5),
        "sigma0": round(sigma0, 4) if np.isfinite(sigma0) else None,
        "passed": r2_global >= 0.92,
        "message": "Q-Variance Prize: One Law to Rule Them All"
    }

    return score


# Auto-run for testing
if __name__ == "__main__":
    df = pd.read_parquet("prize_dataset.parquet")
    score = compute_qvar_score(df, "Quantum Baseline (Orrell & Wilmott 2025)", "David Orrell")
    
    print("\n" + "="*60)
    print("           Q-VARIANCE PRIZE — OFFICIAL RESULT")
    print("="*60)
    print(json.dumps(score, indent=2))
    print("="*60)
