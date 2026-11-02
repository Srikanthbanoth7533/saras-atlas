import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatCurrency(amount: number | null | undefined): string {
  if (amount === null || amount === undefined || isNaN(amount)) return "$0.00";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

export function formatShortCurrency(amount: number | null | undefined): string {
  if (amount === null || amount === undefined || isNaN(amount)) return "$0";
  const abs = Math.abs(amount);
  if (abs >= 1_000_000) {
    return `${amount < 0 ? "-" : ""}$${(abs / 1_000_000).toFixed(2)}M`;
  }
  if (abs >= 1_000) {
    return `${amount < 0 ? "-" : ""}$${(abs / 1_000).toFixed(1)}k`;
  }
  return formatCurrency(amount);
}

export function formatPercent(rate: number | null | undefined, decimals = 1): string {
  if (rate === null || rate === undefined || isNaN(rate)) return "0.0%";
  return `${(rate * 100).toFixed(decimals)}%`;
}

export function formatNumber(num: number | null | undefined): string {
  if (num === null || num === undefined || isNaN(num)) return "0";
  return new Intl.NumberFormat("en-US").format(num);
}

