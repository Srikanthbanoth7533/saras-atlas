# SARAS ATLAS — Prescriptive Optimization Methodology & Duality Proof

## 1. Mathematical Formulation
The prescriptive decision engine optimizes multi-echelon supply chain mitigation interventions under capital constraints using Mixed-Integer Linear Programming (MILP) solved via **Google OR-Tools SCIP**.

---

## 2. Formal Mixed-Integer Program

### 2.1 Decision Variables
- $x_{\text{air}} \in \mathbb{Z}_{\ge 0}$: Integer units expedited via international air freight from Vietnam backup supplier.
- $x_{\text{xfer}} \in \mathbb{Z}_{\ge 0}$: Integer units transferred via domestic LTL ground from Allentown DC.
- $\theta_{\text{ad}} \in [0, 0.35]$: Continuous fraction of paid ad spend throttled to dampen demand.
- $z_{\text{moq}} \in \{0, 1\}$: Binary decision variable enforcing factory air minimum order quantity.

### 2.2 Objective Function
Maximize net contribution margin preserved across the 90-day horizon:
$$\max Z = 58.83 \cdot x_{\text{air}} + 81.13 \cdot x_{\text{xfer}} - 2500.00 \cdot \theta_{\text{ad}}$$

Where:
- $\$58.83/\text{unit}$: Net margin earned per air-freighted unit ($180 retail - $45.15 COGS - $12.50 air - $18.52 processing/outbound - $45 ad).
- $\$81.13/\text{unit}$: Net margin earned per ground-transferred unit ($180 retail - $45.15 COGS - $3.20 ground - $5.52 processing - $45 ad).
- $-\$2500.00$: Commercial penalty for customer acquisition momentum lost due to ad throttling.

### 2.3 Operational Constraints
1. **Treasury Budget Ceiling**:
   $$12.50 \cdot x_{\text{air}} + 3.20 \cdot x_{\text{xfer}} \le 40,000.00$$
2. **Ground Transfer Capacity Ceiling**:
   $$x_{\text{xfer}} \le 800$$
   *(Enforced to preserve Allentown DC origin safety stock and avoid secondary East Coast stockouts)*.
3. **Air Freight Capacity Ceiling**:
   $$x_{\text{air}} \le 3,000$$
4. **Air Freight Minimum Order Quantity (Big-M)**:
   $$500 \cdot z_{\text{moq}} \le x_{\text{air}} \le 3,000 \cdot z_{\text{moq}}, \quad z_{\text{moq}} \in \{0, 1\}$$
5. **Customer Fill Rate Floor (95% SLA)**:
   $$x_{\text{air}} + x_{\text{xfer}} + 1,100 \cdot \theta_{\text{ad}} \ge 1,869.60 \quad (95\% \times 1,968\text{ unit deficit})$$
6. **Marketing Throttle Upper Bound**:
   $$0 \le \theta_{\text{ad}} \le 0.35$$

---

## 3. Solution Derivation & Duality Analysis

### 3.1 Unit Efficiency Ratios (Greedy Knapsack Metric)
$$\rho_{\text{xfer}} = \frac{\$81.13}{\$3.20} = \$25.3531 \text{ margin per dollar spent}$$
$$\rho_{\text{air}} = \frac{\$58.83}{\$12.50} = \$4.7064 \text{ margin per dollar spent}$$

Since $\rho_{\text{xfer}} > \rho_{\text{air}}$ by a factor of $5.39\times$, the optimal policy must saturate ground transfer to its upper bound before deploying capital into air freight.

### 3.2 Step-by-Step Allocation
1. **Saturate Ground Transfer**:
   $$x_{\text{xfer}}^* = 800 \text{ units} \implies \text{Cost} = 800 \times \$3.20 = \$2,560.00$$
2. **Residual Budget**:
   $$B_{\text{residual}} = \$40,000.00 - \$2,560.00 = \$37,440.00$$
3. **Saturate Air Freight**:
   $$x_{\text{air}}^* = \left\lfloor \frac{\$37,440.00}{\$12.50} \right\rfloor = \lfloor 2,995.20 \rfloor = 2,995 \text{ units}$$
4. **Air Outlay & Budget Slack**:
   $$\text{Air Outlay} = 2,995 \times \$12.50 = \$37,437.50$$
   $$\text{Total Capital Outlay} = \$2,560.00 + \$37,437.50 = \$39,997.50$$
   $$\text{Slack} = \$40,000.00 - \$39,997.50 = \$2.50$$
5. **Demand Dampening**:
   $$\theta_{\text{ad}}^* = 0.00\% \quad (\text{Coverage } 3,795 \ge 1,968, \text{ penalty avoided})$$

### 3.3 Continuous LP Relaxation & Duality Gap
- Continuous Upper Bound:
  $$Z_{\text{LP}}^* = 800 \times 81.13 + 2,995.20 \times 58.83 = \$241,111.616$$
- Discrete Integer Optimum:
  $$Z_{\text{IP}}^* = 800 \times 81.13 + 2,995 \times 58.83 = \$241,099.85$$
- **Duality Discretization Gap**:
  $$\text{Gap} = \frac{\$241,111.616 - \$241,099.85}{\$241,111.616} = 0.00488\%$$

---

## 4. Reconciling Operational Budget ($40k) vs Governance Threshold ($25k)
- **$40,000.00 Budget**: Operational working capital ceiling allocated to the mitigation team.
- **$25,000.00 Two-Man Rule Threshold**: Compliance governance policy requiring dual executive signoff (VP Operations + CFO) whenever an approved disbursement exceeds $25,000.00.
- Since $\$39,997.50 > \$25,000.00$, dual signoff is mandatory.
