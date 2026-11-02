# SIMULATION METHODOLOGY & MATHEMATICAL FORMULATIONS

**Document ID:** SIM-ATLAS-001  
**Version:** 1.0.0  
**Phase:** Phase 0 Baseline  
**Author:** AI/ML Research Engineer & Principal Quant Architect  

---

## 1. Epistemological Framework: Separation of Truth Layers

In enterprise decision systems, mixing statistical predictions, accounting identities, and language model conjectures produces dangerous epistemic confusion. SARAS ATLAS enforces a strict **Epistemological Taxonomy**:

```
+-----------------------------------------------------------------------------------------+
|                              EPISTEMOLOGICAL TAXONOMY                                   |
+-------------------+---------------------------------------------+-----------------------+
| Tier              | Nature of Knowledge                         | Engine Component      |
+-------------------+---------------------------------------------+-----------------------+
| 1. Deterministic  | Exact GAAP accounting & inventory physics.   | Balance Equations &   |
|    Identities     | Zero variance. Mathematically indisputable. | Contribution Margin   |
+-------------------+---------------------------------------------+-----------------------+
| 2. Statistical    | Probabilistic lead-time distributions and   | Statsmodels Holt-     |
|    Estimations    | historical demand baselines with intervals. | Winters & SE Bounds   |
+-------------------+---------------------------------------------+-----------------------+
| 3. Prescriptive   | Mixed-Integer Linear Programming global     | Google OR-Tools       |
|    Optimization   | optima under user-defined constraints.      | MILP Solver           |
+-------------------+---------------------------------------------+-----------------------+
| 4. Counterfactual | Causal "what-if" branch evaluations under   | Multi-Echelon Discrete|
|    Simulations    | specific exogenous shock hypotheses.        | Difference Engine     |
+-------------------+---------------------------------------------+-----------------------+
| 5. Narrative      | Structured linguistic synthesis explaining  | Variance Decomposition|
|    Explanations   | mathematical outcomes to executives.        | Narrative Generator   |
+-------------------+---------------------------------------------+-----------------------+
```

---

## 2. Core Mathematical Formulas & Accounting Identities

### 2.1 Multi-Echelon Inventory Balance Equation
For SKU $i$ at warehouse node $w$ on simulation day $t \in \{1, \dots, H\}$:

$$I_{i,w}(t) = \max\left(0, \; I_{i,w}(t-1) + R_{i,w}(t) + X_{i,w}^{\text{in}}(t) - D_{i,w}(t) - X_{i,w}^{\text{out}}(t)\right)$$

Where:
- $I_{i,w}(t)$: On-hand available physical inventory at close of day $t$.
- $R_{i,w}(t)$: Received inbound purchase order receipts on day $t$:
  $$R_{i,w}(t) = \sum_{p \in \text{POs}} Q_{p,i} \cdot \mathbb{I}\left(t = \tau_p^{\text{arrival}}\right)$$
  Where $\tau_p^{\text{arrival}} = \tau_p^{\text{sched}} + \Delta L_p$ ($\Delta L_p$ = delay days).
- $X_{i,w}^{\text{in}}(t), X_{i,w}^{\text{out}}(t)$: Inter-warehouse stock transfers entering or departing node $w$ on day $t$.
- $D_{i,w}(t)$: Total customer order demand routed to node $w$ on day $t$.

### 2.2 Unmet Demand, Backorders & Stockout Days
If requested demand $D_{i,w}(t)$ exceeds available inventory $I_{i,w}(t-1) + R_{i,w}(t)$:
$$S_{i,w}^{\text{unmet}}(t) = \max\left(0, \; D_{i,w}(t) - \left(I_{i,w}(t-1) + R_{i,w}(t)\right)\right)$$
- If cross-zone fallback fulfillment is enabled, $S_{i,w}^{\text{unmet}}(t)$ is transferred to secondary warehouse $w'$ subject to available stock at $w'$.
- Any remaining unfulfilled orders are logged as **Unmet Demand (Lost Orders)**:
  $$U_{i,w}(t) = S_{i,w}^{\text{unmet}}(t) - X_{i, w \leftarrow w'}^{\text{fallback}}(t)$$
- **Stockout State Indicator:**
  $$\Omega_{i,w}(t) = \begin{cases} 1 & \text{if } I_{i,w}(t) = 0 \text{ and } D_{i,w}(t) > 0 \\ 0 & \text{otherwise} \end{cases}$$

### 2.3 Days of Inventory Coverage (DoC)
Calculated based on backward-looking exponential moving average daily sales $\bar{D}_{i,w}$:
$$\text{DoC}_{i,w}(t) = \frac{I_{i,w}(t)}{\bar{D}_{i,w}(t)}$$
Where:
$$\bar{D}_{i,w}(t) = \alpha D_{i,w}(t-1) + (1-\alpha) \bar{D}_{i,w}(t-1), \quad \alpha = 0.10$$

### 2.4 Stockout Risk Probability ($P_{\text{stockout}}$)
Under stochastic lead time $\tilde{L} \sim \mathcal{N}(\mu_L, \sigma_L^2)$ and daily demand $\tilde{D} \sim \mathcal{N}(\mu_D, \sigma_D^2)$:
$$\text{Demand During Lead Time: } \mu_{\text{DDLT}} = \mu_L \mu_D$$
$$\sigma_{\text{DDLT}} = \sqrt{\mu_L \sigma_D^2 + \mu_D^2 \sigma_L^2}$$
$$Z_{i,w}(t) = \frac{I_{i,w}(t) - \mu_{\text{DDLT}}}{\sigma_{\text{DDLT}}}$$
$$P_{\text{stockout}, i, w}(t) = 1 - \Phi\left(Z_{i,w}(t)\right)$$
Where $\Phi(\cdot)$ is the standard normal cumulative distribution function.

---

## 3. Financial Mechanics: Unit Economics & Contribution Margin

SARAS ATLAS tracks exact **GAAP-compliant unit economics** across every fulfilled order line:

$$\text{Net Contribution Margin } (\text{CM}) = \text{Net Revenue} - \text{Total Variable Operational Costs}$$

```
+---------------------------------------------------------------------------------+
|                        UNIT CONTRIBUTION MARGIN WATERFALL                       |
+---------------------------------------------------------------------------------+
  Gross Selling Price (RSP)                                              $180.00
  (-) Customer Discounts & Promotions                                    -$10.00
  =================================================================================
  (=) Net Sales Revenue                                                  $170.00
  ---------------------------------------------------------------------------------
  (-) Supplier FOB Product Cost (COGS)                                   -$42.00
  (-) Inbound Ocean Freight & Drayage                                     -$6.00
  (-) Customs Tariffs & Port Duties (7.5%)                                -$3.15
  (-) 3PL Inbound Receiving Fee                                           -$0.75
  (-) 3PL Pick & Pack Warehouse Fee                                       -$4.50
  (-) Outbound Parcel Carrier Shipping (Zone-dependent: $8.50 - $21.50)  -$10.88
  (-) Payment Gateway & Merchant Fees (2.9% + $0.30)                      -$5.23
  (-) Allocated Direct Marketing Ad Spend (Target CAC)                   -$45.00
  =================================================================================
  (=) Net Contribution Margin ($)                                         $52.49
  (=) Net Contribution Margin (%)                                         30.88%
+---------------------------------------------------------------------------------+
```

### 3.1 Cross-Zone Out-of-Zone Shipping Penalty
When warehouse $w$ stocks out and order is fulfilled from out-of-zone warehouse $w'$:
$$\text{Freight Penalty: } \Delta C_{\text{shipping}} = C_{\text{carrier}}\left(w', \text{dest}\right) - C_{\text{carrier}}\left(w, \text{dest}\right)$$
For West Coast customer fulfilled from East Coast 3PL:
$$\Delta C_{\text{shipping}} = \$21.50 (\text{Zone 8}) - \$8.50 (\text{Zone 2}) = +\$13.00 \text{ per unit penalty}$$
This directly erodes Contribution Margin by $13.00 / \$170.00 = 7.65\text{ percentage points}$.

---

## 4. Working Capital & Cash Flow Dynamics

Working capital liquidity is tracked daily over the simulation horizon:

$$WC(t) = WC(t-1) + \text{Cash Inflows}(t) - \text{Cash Outflows}(t)$$

Where:
- **Cash Inflows:** Cash received from customer orders (settled in $t - 2$ days via Stripe/Shopify Payments).
- **Cash Outflows:**
  1. *Supplier Inbound Payments:* Paid according to terms (e.g. Net 60 from PO departure or 30% deposit / 70% Bill of Lading receipt).
  2. *Emergency Air Freight Payments:* Cash paid immediately ($t+0$) to freight forwarder.
  3. *3PL Warehouse Invoices:* Settled bi-weekly.
  4. *Parcel Carrier Freight Bills:* Settled weekly.
  5. *Digital Advertising Spend:* Charged daily on corporate credit cards.

**Cash Crunch Warning:** When projected $WC(t) < \text{Liquidity Buffer}$ ($\$50,000$), the system flags an emergency cash insolvency warning.

---

## 5. Discrete Difference Simulation Algorithm

The simulation engine evaluates all $H$ days across all $N$ nodes using vectorized NumPy operations:

```
Algorithm 1: Multi-Echelon Shock Simulation (Vectorized)
Input: Baseline State S_0, Inbound Pipeline PO, Demand Array D[T, N], Shock Levers (ΔL, β_freight, α_demand)
Output: Inventory Matrix I[T, N], Financial Matrix FIN[T], Stockout Metrics M

1. Apply Demand Shocks: D_sim[t, n] = D[t, n] * α_demand[t, n]
2. Shift PO Arrival Dates: Arrival(p) = ScheduledArrival(p) + ΔL(p)
3. For day t = 1 to H:
     a. Apply Inbound Arrivals: I[t, n] = I[t-1, n] + Receipts(t, n)
     b. Fulfill Primary Demand: Fulfilled_pri = min(I[t, n], D_sim[t, n])
     c. Record Unmet Demand: Unmet = D_sim[t, n] - Fulfilled_pri
     d. Route Cross-Zone Fallbacks: Fulfilled_cz = min(Stock(OtherNodes), Unmet)
     e. Update Remaining Inventory: I[t, n] -= (Fulfilled_pri + Shipped_out_cz)
     f. Compute Daily Financials:
          Revenue[t] = Σ (Fulfilled * UnitPrice)
          COGS[t] = Σ (Fulfilled * UnitLandedCost)
          Freight[t] = Σ (Fulfilled_pri * BaseFreight * β_freight + Fulfilled_cz * CrossZoneFreight)
          AdSpend[t] = Σ (Fulfilled * CAC_allocated)
          Margin[t] = Revenue[t] - (COGS[t] + Freight[t] + AdSpend[t] + Fees[t])
          WorkingCapital[t] = WorkingCapital[t-1] + CashIn[t] - CashOut[t]
4. Return aggregated metrics and timeseries matrices.
```

- **Computational Complexity:** $\mathcal{O}(H \times N \times K)$ where $H=90$ days, $N=3$ warehouses, $K=50$ SKUs. Total operations: $13,500$ daily state transitions, executing in $< 80\text{ milliseconds}$ in compiled NumPy.

