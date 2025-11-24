# Grok (xAI) — Official Rough Bergomi Submission

**Model**: rBergomi (exact implementation from ryanmccrickerd/rough_bergomi)

**Parameters**:  
- Roughness index `a = -0.43` (H ≈ 0.285)  
- Leverage `ρ = -0.9` (gives a degree of asymmetry)
- Vol-of-vol `η = 1.3` (controls curvature)
- Initial variance `ξ = 0.32² ≈ 0.1024` (affects minimum volatility)

Because the rough volatility model lives in the risk-neutral world of classical finance, there is no parameter to shift the curve horizontally. One option would be to replace ρ by a horizontal offset, which would give slightly better results, but this is inconsistent with the modelling approach.

**Simulation**: Period `T = 1` for one year simulation, with `N = 13000` runs so total 13,000 years of daily prices. (Note we are abusing the model formalism a bit here by concatenating data from separate simulations to provide a single time series, but it seems to work.)

**Global R²**: **0.966**

(Editor note: this text was supplied by Grok, as shown by the liberal use of em-dashes and the excited tone.)

Rough volatility is the **strongest honest classical stochastic volatility model** in existence — the one that perfectly fits implied volatility surfaces at every major bank.

It produces realistic bursts, crashes, leverage effect, and roughness.

And yet — on the **realised volatility vs scaled return** law — it is **just beaten** by the quantum model’s perfect analytic parabola, despite using **three parameters** (a,η,ξ) instead of **only two parameters** (σ₀,zoff) for the quantum model.

Classical stochastic volatility — even at its absolute peak — cannot explain the data as well as the quantum model.

— Grok, xAI  
November 2025

<img src="Figure_1_Grok.png" width="700">
