<div align="center">

<img src="./assets/arcana-logo.png" alt="ARCANA Suite Logo" width="180" />

# ARCANA Suite

**Advanced Reconnaissance, Case Analysis & Network Analytics**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Deploy on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render)](https://render.com)
[![Stripe Enabled](https://img.shields.io/badge/Payments-Stripe-635BFF?logo=stripe)](https://stripe.com)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

*A modular, professional-grade intelligence and case management suite — built for analysts, investigators, and operations teams.*

## EVIDRYX foundation

**EVIDRYX by Arcana Forensics** is now included as ARCANA Suite's offline-first,
defensive DFIR foundation for Windows, Linux, and Android evidence. It adds
read-only source hashing, local case and evidence metadata, integrity
verification, allowed-root enforcement, and a hash-chained audit trail without
removing or renaming existing ARCANA capabilities. See
[`docs/EVIDRYX_FOUNDATION.md`](docs/EVIDRYX_FOUNDATION.md) for its threat model,
authenticated deployment configuration, API workflow, audit findings, and roadmap.

[Overview](#overview) · [Modules](#module-map) · [Features](#features) · [Architecture](#architecture) · [Installation](#installation) · [Deployment](#render-deployment) · [Stripe](#stripe-integration) · [Screenshots](#screenshots) · [License](#license)

</div>

---

## Overview

**ARCANA Suite** is a full-stack intelligence platform designed to centralize the entire investigation lifecycle — from OSINT collection and digital artifact carving to timeline reconstruction, pain-point analysis, and secure case export. Built with modularity at its core, each component can be deployed independently or orchestrated together as a unified suite.

ARCANA is purpose-built for:
- **Digital forensics and incident response (DFIR)** teams
- **OSINT analysts** and threat intelligence researchers
- **Compliance and legal operations** requiring audit-ready case documentation
- **Subscription-based SaaS** delivery with Stripe-powered billing

> ⚠️ **Responsible Use Notice:** ARCANA Suite is intended strictly for lawful investigative use. Operators are solely responsible for ensuring compliance with applicable laws, regulations, and organizational policies. Unauthorized interception, collection, or analysis of data is prohibited.

---

## Module Map

```
arcana-suite/
├── core/                  → ARCANA Core          (orchestration, auth, shared services)
├── pain-point-resolver/   → PainPointResolver     (friction analysis & root-cause engine)
├── reliability-shield/    → ReliabilityShield     (uptime monitoring, failure detection)
├── opsec-validator/       → OPSEC Validator       (operational security scoring & audits)
├── subscription-flow/     → SubscriptionFlow      (Stripe billing, plans, webhooks)
├── mobile-artifact-carver/→ Mobile Artifact Carver(iOS/Android artifact extraction)
├── timeline-engine/       → Timeline Engine       (event reconstruction & visualization)
├── osint-collector/       → OSINT Collector       (automated open-source intelligence)
├── case-exporter/         → Case Exporter         (PDF/JSON/CSV audit-ready export)
├── assets/                → Logos, screenshots, diagrams
└── docs/                  → Extended documentation
```

| Module | Role | Status |
|---|---|---|
| **ARCANA Core** | Auth, routing, user mgmt, inter-module API bus | ✅ Stable |
| **PainPointResolver** | Identifies friction points across workflows and surfaces root causes | ✅ Stable |
| **ReliabilityShield** | Uptime, anomaly detection, failure-mode alerting | ✅ Stable |
| **OPSEC Validator** | Audits operational security posture; generates compliance scores | ✅ Stable |
| **SubscriptionFlow** | Stripe-powered plan management, metered billing, webhook handling | ✅ Stable |
| **Mobile Artifact Carver** | Parses iOS/Android artifacts — SQLite DBs, plists, cache files | 🔧 Beta |
| **Timeline Engine** | Reconstructs chronological event sequences from multi-source data | ✅ Stable |
| **OSINT Collector** | Orchestrates open-source intelligence gathering across configured sources | 🔧 Beta |
| **Case Exporter** | Packages investigation data into signed, audit-ready export bundles | ✅ Stable |

---

## Features

### 🧠 ARCANA Core
- Centralized JWT-based authentication and role-based access control (RBAC)
- Module-agnostic REST API bus with versioned endpoints
- Shared configuration management and environment injection
- Audit logging for every cross-module action

### 🔍 PainPointResolver
- Workflow friction scoring using configurable heuristics
- Root-cause drill-down with evidence attachment
- Integration with Timeline Engine for chronological correlation

### 🛡️ ReliabilityShield
- Real-time service health monitoring with configurable thresholds
- Failure-mode classification and escalation routing
- Dashboard widgets consumable by ARCANA Core UI

### 🔒 OPSEC Validator
- Structured OPSEC audit checklists with auto-scoring
- Deviation detection against defined operational baselines
- Exportable compliance reports via Case Exporter

### 💳 SubscriptionFlow
- Stripe Checkout and Billing Portal integration
- Metered and seat-based subscription models
- Webhook listener for real-time event processing (`invoice.paid`, `customer.subscription.deleted`, etc.)
- Plan enforcement hooks consumed by ARCANA Core

### 📱 Mobile Artifact Carver
- iOS artifact support: `sms.db`, `AddressBook.sqlitedb`, `KnowledgeC.db`, plists, cache manifests
- Android artifact support: `mmssms.db`, call logs, app databases, `contacts2.db`
- Structured output piped directly into Timeline Engine

### ⏱️ Timeline Engine
- Multi-source event ingestion (file system, mobile artifacts, logs, OSINT)
- Chronological reconstruction with conflict resolution
- Interactive timeline visualization (exportable as SVG/JSON)

### 🌐 OSINT Collector
- Configurable collection modules (social footprint, domain intel, email reputation)
- Rate-limited, respectful collection pipelines with source attribution
- Output normalized to ARCANA's common intelligence schema

### 📦 Case Exporter
- Export bundles in PDF, JSON, and CSV formats
- Cryptographic signing of export manifests for chain-of-custody integrity
- Redaction layer for sensitive PII before sharing

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      ARCANA Core                        │
│         (Auth · API Bus · Config · Audit Log)           │
└────────────────────────┬────────────────────────────────┘
                         │ REST / Internal Events
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼──────┐ ┌──────▼──────┐ ┌─────▼───────────┐
│PainPointRes.  │ │ReliabilityS.│ │ OPSEC Validator │
└───────────────┘ └─────────────┘ └─────────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼──────┐ ┌──────▼──────┐ ┌─────▼───────────┐
│OSINT Collector│ │Mobile Artif.│ │ Timeline Engine │
└───────┬───────┘ └──────┬──────┘ └────────┬────────┘
        │                │                  │
        └────────────────┼──────────────────┘
                         │
               ┌─────────▼──────────┐
               │    Case Exporter   │
               └─────────┬──────────┘
                         │
               ┌─────────▼──────────┐
               │  SubscriptionFlow  │
               │  (Stripe Gateway)  │
               └────────────────────┘
```

**Tech Stack**

| Layer | Technology |
|---|---|
| Backend | Node.js / Express (or Python / FastAPI per module) |
| Database | PostgreSQL (primary) · SQLite (artifact carving) |
| Auth | JWT + refresh tokens · RBAC |
| Payments | Stripe Billing + Webhooks |
| Hosting | Render (Web Services + Background Workers) |
| Storage | Render Disks / S3-compatible for case bundles |
| Frontend | React + Tailwind CSS |
| Export | PDFKit · json-stable-stringify · csv-writer |

---

## Installation

### Prerequisites

- **Node.js** ≥ 18 LTS (or Python ≥ 3.11 for Python modules)
- **PostgreSQL** ≥ 14
- **Stripe CLI** (for local webhook testing)
- **Git**

### 1 — Clone the Repository

```bash
git clone https://github.com/your-org/arcana-suite.git
cd arcana-suite
```

### 2 — Install Dependencies

Each module has its own `package.json` (or `requirements.txt`). Use the root-level install script to bootstrap all modules at once:

```bash
npm run install:all
# or individually:
cd core && npm install
cd ../subscription-flow && npm install
# ... repeat per module
```

### 3 — Configure Environment Variables

Copy the root example file and populate your values:

```bash
cp .env.example .env
```

**.env reference:**

```env
# ── Core ──────────────────────────────────────
NODE_ENV=development
PORT=3000
JWT_SECRET=your_jwt_secret_here
DATABASE_URL=postgresql://user:password@localhost:5432/arcana

# ── Stripe ────────────────────────────────────
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_STARTER=price_...
STRIPE_PRICE_ID_PRO=price_...
STRIPE_PRICE_ID_ENTERPRISE=price_...

# ── Render ────────────────────────────────────
RENDER_EXTERNAL_URL=https://arcana-suite.onrender.com

# ── OSINT Collector ───────────────────────────
OSINT_API_KEY=your_osint_api_key
OSINT_RATE_LIMIT_RPM=30

# ── Case Exporter ─────────────────────────────
EXPORT_SIGNING_KEY=your_signing_key
EXPORT_STORAGE_PATH=/data/exports
```

### 4 — Initialize the Database

```bash
npm run db:migrate
npm run db:seed   # optional: loads demo data
```

### 5 — Start in Development Mode

```bash
npm run dev
# All modules start via concurrently on configured ports
```

---

## Render Deployment

ARCANA Suite is optimized for deployment on **[Render](https://render.com)**. Each module maps to a Render **Web Service** or **Background Worker**.

### Recommended Service Configuration

| Service | Type | Start Command | Plan |
|---|---|---|---|
| `arcana-core` | Web Service | `npm start` | Starter+ |
| `subscription-flow` | Web Service | `npm start` | Starter |
| `timeline-engine` | Web Service | `npm start` | Starter |
| `osint-collector` | Background Worker | `npm run worker` | Starter |
| `case-exporter` | Web Service | `npm start` | Starter |
| `mobile-artifact-carver` | Background Worker | `npm run worker` | Starter |

### Deployment Steps

1. **Connect your GitHub repo** to Render and select `arcana-suite`.
2. **Create each Web Service / Background Worker** from the Render dashboard.
3. **Set Environment Variables** in each service's *Environment* tab — use the variables from `.env.example`.
4. **Attach a Render PostgreSQL database** and copy the `DATABASE_URL` into each service that requires it.
5. **Set `RENDER_EXTERNAL_URL`** to the public URL of `arcana-core`.
6. Deploy — Render will build and launch each service automatically.

> 💡 **Tip:** Use Render's *Secret Files* feature to mount `.env` safely rather than entering variables one by one.

### Health Checks

Each service exposes a `/health` endpoint. Configure Render health checks to:
- **Path:** `/health`
- **Interval:** 30s
- **Timeout:** 10s

---

## Stripe Integration

ARCANA's **SubscriptionFlow** module handles all billing via Stripe.

### Plans

| Plan | Stripe Price ID Env Var | Features |
|---|---|---|
| Starter | `STRIPE_PRICE_ID_STARTER` | Core + Timeline + Exporter |
| Pro | `STRIPE_PRICE_ID_PRO` | All modules, 5 seats |
| Enterprise | `STRIPE_PRICE_ID_ENTERPRISE` | Unlimited seats, SLA, OPSEC module |

### Webhook Configuration

1. In the [Stripe Dashboard](https://dashboard.stripe.com/webhooks), create a new webhook endpoint:
   ```
   https://arcana-suite.onrender.com/api/subscriptions/webhook
   ```
2. Subscribe to these events:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.paid`
   - `invoice.payment_failed`
3. Copy the **Webhook Signing Secret** into `STRIPE_WEBHOOK_SECRET`.

### Testing Webhooks Locally

```bash
stripe listen --forward-to localhost:3001/api/subscriptions/webhook
stripe trigger checkout.session.completed
```

### Billing Portal

Users can manage their subscriptions via the Stripe Customer Portal, accessible at:
```
GET /api/subscriptions/portal  →  redirects to Stripe-hosted portal
```

---

## Screenshots

> 📸 Replace placeholders below with actual screenshots from `/assets/screenshots/`.

| View | Preview |
|---|---|
| Dashboard | ![Dashboard](./assets/screenshots/dashboard.png) |
| Timeline Engine | ![Timeline](./assets/screenshots/timeline-engine.png) |
| OSINT Collector | ![OSINT](./assets/screenshots/osint-collector.png) |
| Mobile Artifact Carver | ![Carver](./assets/screenshots/mobile-carver.png) |
| Case Exporter | ![Exporter](./assets/screenshots/case-exporter.png) |
| OPSEC Validator | ![OPSEC](./assets/screenshots/opsec-validator.png) |
| Subscription Management | ![Billing](./assets/screenshots/subscription-flow.png) |

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

```bash
# Fork → branch → commit → PR
git checkout -b feature/your-feature-name
git commit -m "feat: describe your change"
git push origin feature/your-feature-name
```

**Branch naming conventions:**
- `feature/` — new functionality
- `fix/` — bug fixes
- `docs/` — documentation only
- `chore/` — maintenance, dependencies

---

## Roadmap

- [ ] Graph-based relationship mapping (entity link analysis)
- [ ] AI-assisted anomaly summarization in ReliabilityShield
- [ ] Native mobile app (React Native) for field investigators
- [ ] STIX/TAXII export format in Case Exporter
- [ ] Multi-tenant workspace isolation
- [ ] Two-factor authentication (TOTP)

---

## Security

Found a vulnerability? **Do not open a public issue.**
Email: `security@your-org.com` with subject line `[ARCANA] Security Disclosure`.

We follow responsible disclosure principles and will respond within 72 hours.

---

## License

```
MIT License

Copyright (c) 2026 ARCANA Suite Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

See [LICENSE](LICENSE) for the full text.

---

## Links

| Resource | URL |
|---|---|
| 🌐 Live App | https://arcana-suite.onrender.com |
| 📖 Documentation | https://docs.arcana-suite.io |
| 🐛 Issue Tracker | https://github.com/your-org/arcana-suite/issues |
| 💬 Discussions | https://github.com/your-org/arcana-suite/discussions |
| 💳 Stripe Dashboard | https://dashboard.stripe.com |
| ☁️ Render Dashboard | https://dashboard.render.com |

---

<div align="center">
  <sub>Built with precision by the ARCANA team · 2026</sub>
</div>
