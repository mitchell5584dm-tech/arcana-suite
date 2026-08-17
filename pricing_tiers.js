export const subscriptionPlans = {
  starter: {
    name: "ARCANA Suite – Starter",
    description: "Essential tools for individuals and small teams.",
    monthly: {
      price: "$15/mo",
      stripeLink: "https://buy.stripe.com/fZu14m5Q2esA5ew0Fj5sA04",
    },
    annual: {
      price: "$99/yr",
      savings: "45% off",
      stripeLink: "https://buy.stripe.com/6oUdR8diu5W45ewafT5sA05",
    },
    limits: "Light usage, core ARCANA tools.",
    fine_print: "No tracking. No upsells.",
  },
  pro: {
    name: "ARCANA Suite – Pro",
    description: "Advanced features for growing teams. Priority processing and expanded toolset.",
    monthly: {
      price: "$39/mo",
      stripeLink: "https://buy.stripe.com/cNiaEWa6iackdL2gEh5sA06",
    },
    annual: {
      price: "$299/yr",
      savings: "36% off",
      stripeLink: "https://buy.stripe.com/fZu28q92e84ceP60Fj5sA07",
    },
    limits: "Full usage, priority processing.",
    fine_print: "No ads. No data selling.",
  },
  elite: {
    name: "ARCANA Suite – Elite",
    description: "Unlimited power for enterprise. White-glove onboarding and dedicated support.",
    monthly: {
      price: "$99/mo",
      stripeLink: "https://buy.stripe.com/00wfZgemyfwEeP61Jn5sA08",
    },
    annual: {
      price: "$790/yr",
      savings: "34% off",
      stripeLink: "https://buy.stripe.com/eVq6oG5Q298gcGYco15sA09",
    },
    limits: "Unlimited usage. All features unlocked.",
    fine_print: "No subscription traps. Cancel anytime.",
  },
};
