"""
SARAS ATLAS — Phase 8.2: Independent Optimization Optimality Verification Script.
Implements an exhaustive discrete global search and analytical knapsack derivation
completely independent of Google OR-Tools and SCIP.
"""

import sys
import numpy as np

def run_independent_verification():
    print("=" * 80)
    print("INDEPENDENT MATHEMATICAL OPTIMALITY VERIFICATION")
    print("=" * 80)

    # 1. Problem Parameters
    budget_ceiling = 40000.00
    c_air_cost = 12.50
    c_xfer_cost = 3.20
    unit_gross_cm = 71.33
    cross_zone_penalty = 13.00
    air_moq = 500
    air_max_cap = 3000
    xfer_max_cap = 800
    max_ad_throttle = 0.35
    net_deficit = 1968.0
    min_fill_rate = 0.95
    target_coverage = net_deficit * min_fill_rate  # 1869.6
    ad_cooling_factor = 1100.0
    ad_penalty = 2500.0

    r_air = unit_gross_cm - c_air_cost  # 58.83
    r_xfer = unit_gross_cm - c_xfer_cost + cross_zone_penalty  # 81.13

    print(f"Objective Coeffs: r_air = ${r_air:.2f}/unit, r_xfer = ${r_xfer:.2f}/unit, ad_penalty = -${ad_penalty:.2f}")
    print(f"Cost per unit: Air = ${c_air_cost:.2f}, Ground = ${c_xfer_cost:.2f}")
    print(f"Efficiency: Ground = ${r_xfer / c_xfer_cost:.4f}/$ vs Air = ${r_air / c_air_cost:.4f}/$")

    # 2. Exhaustive Discrete Global Search
    # Evaluate every integer x_xfer in [0..800]
    best_obj = -1e9
    best_sol = None
    feasible_count = 0

    xfer_range = np.arange(0, xfer_max_cap + 1)  # 0 to 800

    for x_xfer in xfer_range:
        rem_budget = budget_ceiling - (x_xfer * c_xfer_cost)
        if rem_budget < 0:
            continue

        # Max integer air units possible within remaining budget and factory cap
        max_air_from_budget = int(rem_budget // c_air_cost)
        max_air = min(air_max_cap, max_air_from_budget)

        # Candidates for x_air: either max_air (if >= MOQ), or 0 (if max_air < MOQ)
        air_candidates = []
        if max_air >= air_moq:
            air_candidates.append(max_air)
            # Also test MOQ boundary
            air_candidates.append(air_moq)
        # Also test x_air = 0
        air_candidates.append(0)

        for x_air in air_candidates:
            # Check MOQ constraint
            if x_air > 0 and x_air < air_moq:
                continue

            # Check budget
            total_cost = (x_air * c_air_cost) + (x_xfer * c_xfer_cost)
            if total_cost > budget_ceiling:
                continue

            # Determine minimal ad throttle required to satisfy service fill rate
            deficit_gap = target_coverage - (x_air + x_xfer)
            if deficit_gap <= 0:
                theta_ad = 0.0
            else:
                theta_ad = deficit_gap / ad_cooling_factor
                if theta_ad > max_ad_throttle:
                    continue  # Infeasible service level

            # Compute objective
            obj = (r_air * x_air) + (r_xfer * x_xfer) - (ad_penalty * theta_ad)
            feasible_count += 1

            if obj > best_obj:
                best_obj = obj
                best_sol = (x_air, x_xfer, theta_ad, total_cost)

    print(f"\n[METHOD 1: EXHAUSTIVE DISCRETE SEARCH]")
    print(f"  Feasible solutions evaluated: {feasible_count:,}")
    print(f"  GLOBAL MAXIMUM OBJECTIVE: ${best_obj:,.2f}")
    print(f"  Optimal Decision Vector:")
    print(f"    - Air Freight (x_air):    {best_sol[0]:,} units")
    print(f"    - Ground Transfer (x_xfer): {best_sol[1]:,} units")
    print(f"    - Ad Spend Throttle:       {best_sol[2]*100:.2f}%")
    print(f"    - Total Capital Outlay:    ${best_sol[3]:,.2f} (Slack: ${budget_ceiling - best_sol[3]:.2f})")

    # Verify matching SCIP solution
    assert best_sol[0] == 2995, f"Expected 2995, got {best_sol[0]}"
    assert best_sol[1] == 800, f"Expected 800, got {best_sol[1]}"
    assert best_sol[2] == 0.0, f"Expected 0.0, got {best_sol[2]}"
    assert abs(best_obj - 241099.85) < 0.01, f"Objective mismatch: {best_obj}"
    print("  --> EXACT IDENTITY TO SCIP SOLUTION CONFIRMED.")

    # 3. Method 2: Analytical Knapsack / Simplex Derivation
    print(f"\n[METHOD 2: ANALYTICAL KNAPSACK DUALITY & RELAXATION]")
    lp_xfer = 800.0
    lp_rem_cash = budget_ceiling - (lp_xfer * c_xfer_cost)
    lp_air = lp_rem_cash / c_air_cost  # 2995.2
    lp_upper_bound = (lp_xfer * r_xfer) + (lp_air * r_air)
    print(f"  Continuous LP Relaxation Optimum: x_xfer={lp_xfer}, x_air={lp_air:.2f}")
    print(f"  Continuous LP Upper Bound:        ${lp_upper_bound:,.3f}")
    print(f"  Integer Solution Value:           ${best_obj:,.2f}")
    duality_gap = lp_upper_bound - best_obj
    print(f"  Integer Discretization Gap:       ${duality_gap:.3f} ({duality_gap / best_obj * 100:.5f}%)")

    # 4. Method 3: Comparative Analysis against Alternative Feasible Policies
    print(f"\n[METHOD 3: COMPARISON AGAINST ALTERNATIVE FEASIBLE CANDIDATES]")
    candidates = [
        ("Candidate 1: SCIP Production Solution (Max Budget Buffer)", 2995, 800, 0.0),
        ("Candidate 2: Pure Deficit Coverage (JIT Exact 1,968 units)", 1168, 800, 0.0),
        ("Candidate 3: Ground Transfer Only + Max Ad Throttle", 0, 800, 0.35),
        ("Candidate 4: Air Freight Only (No Transfers)", 3000, 0, 0.0),
        ("Candidate 5: Budget Half Deployment ($20K Ceiling)", 1395, 800, 0.0),
    ]

    for name, c_air, c_xfer, c_th in candidates:
        c_cost = (c_air * c_air_cost) + (c_xfer * c_xfer_cost)
        c_cov = c_air + c_xfer + (c_th * ad_cooling_factor)
        c_obj = (r_air * c_air) + (r_xfer * c_xfer) - (ad_penalty * c_th)
        c_status = "FEASIBLE" if (c_cost <= budget_ceiling and c_cov >= target_coverage) else "INFEASIBLE"
        print(f"  * {name}:")
        print(f"      Allocation: Air={c_air:,} | Ground={c_xfer:,} | Throttle={c_th*100:.1f}%")
        print(f"      Capital: ${c_cost:,.2f} | Coverage: {c_cov:,.1f} units | Status: {c_status}")
        print(f"      Objective Value: ${c_obj:,.2f} (Delta to Optimum: -${best_obj - c_obj:,.2f})")

    print("\n" + "=" * 80)
    print("INDEPENDENT VERIFICATION COMPLETE: MATHEMATICALLY SOUND & OPTIMAL.")
    print("=" * 80)

if __name__ == "__main__":
    run_independent_verification()
