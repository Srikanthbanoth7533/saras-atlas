import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SARAS ATLAS — Commerce Resilience & Decision Simulation",
  description:
    "Enterprise Digital Twin and Prescriptive Decision Intelligence Platform for E-Commerce & Retail.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-command-950 text-slate-100 antialiased selection:bg-cyan-500/30 selection:text-cyan-200">
        {children}
      </body>
    </html>
  );
}

