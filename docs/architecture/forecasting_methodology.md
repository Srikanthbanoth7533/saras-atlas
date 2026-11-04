# SARAS ATLAS — Forecasting Methodology & Prediction Intervals

## 1. Overview
The Forecasting Studio within SARAS ATLAS provides multi-horizon predictive demand intelligence. It decomposes historical order patterns into trend, seasonality, and promotional lifts, generating forward projections with statistically rigorous uncertainty bounds.

---

## 2. Statistical Framework

### 2.1 Classical Time-Series Decomposition
Historical demand $Y(t)$ is decomposed additively:
$$Y(t) = T(t) + S(t) + P(t) + \epsilon(t)$$
Where:
- $T(t)$: Underlying multi-week macro growth trend.
- $S(t)$: 7-day day-of-week seasonality (peaking Friday–Sunday for DTC e-commerce).
- $P(t)$: Promotional shocks and marketing-driven demand campaigns.
- $\epsilon(t) \sim \mathcal{N}(0, \sigma^2)$: Residual white noise error.

### 2.2 Holt-Winters Exponential Smoothing
For forward horizons $h \in \{1, \dots, 30\}$ days:
$$\hat{Y}(t + h) = \ell_t + h \cdot b_t + s_{t - m + (h \pmod m)}$$
With level ($\ell_t$), trend ($b_t$), and seasonal ($s_t$) updates tuned via smoothing parameters $(\alpha, \beta, \gamma)$.

---

## 3. Nested Prediction Interval Hierarchy
To provide actionable risk bounds for inventory safety planning, SARAS ATLAS calculates strictly nested confidence ribbons:
- **Point Forecast ($\hat{Y}$)**: Expected baseline trajectory.
- **80% Prediction Interval ($[L_{80}, U_{80}]$)**: Operational tolerance band for routine reordering:
  $$\hat{Y} \pm 1.282 \times \hat{\sigma}_h$$
- **95% Prediction Interval ($[L_{95}, U_{95}]$)**: Buffer ceiling for black-swan stockout prevention:
  $$\hat{Y} \pm 1.960 \times \hat{\sigma}_h$$

Where $\hat{\sigma}_h = \sigma \sqrt{1 + \sum_{i=1}^{h-1} \psi_i^2}$ accounts for error accumulation over multi-day horizons.

---

## 4. Verification of Interval Nesting
The test suite validates that for all predicted horizons $h$:
$$L_{95}(h) \le L_{80}(h) \le \hat{Y}(h) \le U_{80}(h) \le U_{95}(h)$$
This ensures risk sentinels never generate inverted confidence bounds.
