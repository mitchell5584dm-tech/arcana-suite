import React, { useState } from "react";
import { subscriptionPlans } from "./pricing_tiers";

const tierOrder = ["starter", "pro", "elite"];

const highlights = {
  starter: ["Core ARCANA tools", "Light usage", "Email support", "No tracking"],
  pro:     ["Full ARCANA toolset", "Priority processing", "Priority support", "No ads"],
  elite:   ["All features unlocked", "Unlimited usage", "Dedicated support", "White-glove onboarding"],
};

const badges = {
  starter: null,
  pro:     "Most Popular",
  elite:   "Best Value",
};

export default function SubscriptionPanel() {
  const [billing, setBilling] = useState("monthly");

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem", maxWidth: 960, margin: "0 auto" }}>
      <h2 style={{ textAlign: "center", marginBottom: "0.5rem" }}>ARCANA Suite Plans</h2>
      <p style={{ textAlign: "center", color: "#666", marginBottom: "1.5rem" }}>
        No tracking. No upsells. Cancel anytime.
      </p>

      {/* Billing toggle */}
      <div style={{ display: "flex", justifyContent: "center", gap: "0.5rem", marginBottom: "2rem" }}>
        {["monthly", "annual"].map((b) => (
          <button
            key={b}
            onClick={() => setBilling(b)}
            style={{
              padding: "0.4rem 1.2rem",
              borderRadius: 999,
              border: "1px solid #333",
              background: billing === b ? "#111" : "#fff",
              color: billing === b ? "#fff" : "#111",
              cursor: "pointer",
              fontWeight: 600,
              fontSize: "0.9rem",
            }}
          >
            {b === "monthly" ? "Monthly" : "Annual"}
            {b === "annual" && (
              <span style={{ marginLeft: "0.4rem", color: billing === "annual" ? "#7effa0" : "#2a9d2a", fontSize: "0.8rem" }}>
                Save up to 45%
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Tier cards */}
      <div style={{ display: "flex", gap: "1.5rem", flexWrap: "wrap", justifyContent: "center" }}>
        {tierOrder.map((key) => {
          const plan = subscriptionPlans[key];
          const current = plan[billing];
          const badge = badges[key];

          return (
            <div
              key={key}
              style={{
                border: key === "pro" ? "2px solid #111" : "1px solid #ddd",
                borderRadius: 12,
                padding: "1.5rem",
                flex: "1 1 260px",
                maxWidth: 300,
                position: "relative",
                background: "#fff",
                boxShadow: key === "pro" ? "0 4px 24px rgba(0,0,0,0.12)" : "none",
              }}
            >
              {badge && (
                <span
                  style={{
                    position: "absolute",
                    top: "-12px",
                    left: "50%",
                    transform: "translateX(-50%)",
                    background: "#111",
                    color: "#fff",
                    fontSize: "0.75rem",
                    fontWeight: 700,
                    padding: "2px 12px",
                    borderRadius: 999,
                    whiteSpace: "nowrap",
                  }}
                >
                  {badge}
                </span>
              )}

              <h3 style={{ margin: "0 0 0.25rem" }}>{plan.name}</h3>
              <p style={{ color: "#666", fontSize: "0.85rem", margin: "0 0 1rem" }}>{plan.description}</p>

              <div style={{ fontSize: "2rem", fontWeight: 800, marginBottom: "0.25rem" }}>
                {current.price}
              </div>
              {billing === "annual" && current.savings && (
                <div style={{ color: "#2a9d2a", fontSize: "0.85rem", marginBottom: "0.75rem", fontWeight: 600 }}>
                  {current.savings} off vs monthly
                </div>
              )}

              <ul style={{ paddingLeft: "1.1rem", margin: "0 0 1.5rem", color: "#444", fontSize: "0.9rem" }}>
                {highlights[key].map((f) => <li key={f} style={{ marginBottom: "0.3rem" }}>{f}</li>)}
              </ul>

              <a
                href={current.stripeLink}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: "block",
                  textAlign: "center",
                  padding: "0.65rem 1rem",
                  borderRadius: 8,
                  background: key === "pro" ? "#111" : "transparent",
                  color: key === "pro" ? "#fff" : "#111",
                  border: "2px solid #111",
                  fontWeight: 700,
                  textDecoration: "none",
                  fontSize: "0.95rem",
                }}
              >
                Get {plan.name.split("\u2013")[1]?.trim() ?? plan.name}
              </a>

              <p style={{ textAlign: "center", color: "#999", fontSize: "0.75rem", marginTop: "0.6rem" }}>
                {plan.fine_print}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
