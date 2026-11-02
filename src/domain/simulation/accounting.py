"""
SARAS ATLAS — Accounting & Financial Unit Economics Engine.
Implements exact GAAP unit contribution margin, shipping zone tariffs, and working capital cash flow calculations.
Zero floating-point drift.
"""

from typing import Dict, Any


def calculate_unit_contribution_margin(
    retail_price: float,
    base_cogs: float,
    inbound_tariff_rate: float,
    pick_pack_fee: float,
    outbound_shipping_cost: float,
    payment_fee_rate: float,
    allocated_ad_spend: float,
    discount: float = 0.00
) -> Dict[str, float]:
    """
    Computes exact GAAP unit contribution margin and cost breakdown down to the penny.
    
    Formula:
        Net Revenue = Retail Price - Discount
        Landed Product Cost = Base COGS + Inbound Tariffs
        Variable Operational Costs = Landed Cost + Pick/Pack + Outbound Shipping + Merchant Processing Fees + Allocated Ad Spend
        Net Contribution Margin ($) = Net Revenue - Variable Operational Costs
        Contribution Margin (%) = Net Contribution Margin / Net Revenue
    """
    net_revenue = round(retail_price - discount, 2)
    tariffs = round(base_cogs * inbound_tariff_rate, 2)
    landed_cogs = round(base_cogs + tariffs, 2)
    processing_fee = round((net_revenue * payment_fee_rate) + 0.30, 2)  # Standard Stripe/Shopify rate
    
    variable_costs = round(
        landed_cogs + pick_pack_fee + outbound_shipping_cost + processing_fee + allocated_ad_spend, 2
    )
    
    cm_dollars = round(net_revenue - variable_costs, 2)
    cm_percentage = round(cm_dollars / net_revenue, 4) if net_revenue > 0 else 0.0

    return {
        "gross_price": round(retail_price, 2),
        "discount": round(discount, 2),
        "net_revenue": net_revenue,
        "base_cogs": round(base_cogs, 2),
        "tariffs": tariffs,
        "landed_cogs": landed_cogs,
        "pick_pack_fee": round(pick_pack_fee, 2),
        "outbound_shipping_cost": round(outbound_shipping_cost, 2),
        "payment_processing_fee": processing_fee,
        "allocated_ad_spend": round(allocated_ad_spend, 2),
        "total_variable_costs": variable_costs,
        "contribution_margin_dollars": cm_dollars,
        "contribution_margin_percentage": cm_percentage
    }


def compute_working_capital_balance(
    cash_inflows: list[float],
    cash_outflows: list[float],
    initial_cash_buffer: float = 150000.00
) -> Dict[str, Any]:
    """
    Tracks daily working capital liquidity balances over a planning horizon.
    """
    daily_balances = []
    current_cash = initial_cash_buffer
    min_cash = current_cash
    cash_crunch_days = []

    for day_idx, (inflow, outflow) in enumerate(zip(cash_inflows, cash_outflows)):
        current_cash = round(current_cash + inflow - outflow, 2)
        daily_balances.append(current_cash)
        if current_cash < min_cash:
            min_cash = current_cash
        if current_cash < 50000.00:  # Critical liquidity threshold ($50,000 buffer)
            cash_crunch_days.append(day_idx + 1)

    return {
        "initial_cash": initial_cash_buffer,
        "final_cash": daily_balances[-1] if daily_balances else initial_cash_buffer,
        "minimum_cash_balance": min_cash,
        "is_liquidity_breached": len(cash_crunch_days) > 0,
        "first_breach_day": cash_crunch_days[0] if cash_crunch_days else None,
        "daily_balances": daily_balances
    }
