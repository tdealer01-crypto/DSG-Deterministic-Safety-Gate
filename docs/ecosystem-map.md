# Ecosystem Map

This document consolidates the repositories in the broader DSG ecosystem that materially improve the effectiveness of this core repository.

## Primary Repositories

### 1. DSG Core Gate
- Repository: `tdealer01-crypto/DSG-Deterministic-Safety-Gate`
- Role: protocol, reference node, SDKs, CLI, policy engine, release surface
- Why it matters: this is the source of truth for execution decisions and developer-facing integrations

### 2. DSG Control Plane
- Repository: `tdealer01-crypto/tdealer01-crypto-dsg-control-plane`
- Role: operator-facing product surface
- Current value:
  - Next.js app router
  - Stripe checkout/webhook routes
  - Supabase admin integration
  - health check route
- How to use it with DSG core:
  - connect dashboard actions to `/execute`
  - visualize `/ledger` and `/metrics`
  - expose billing, org, and operator controls around DSG runtime

### 3. Deterministic Audit Layer
- Repository: `tdealer01-crypto/dsg-deterministic-audit`
- Role: higher-order deterministic audit and cross-cloud verification framing
- Current value:
  - cross-cloud invariant language
  - entropy gating concept
  - determinism matrix dashboard language
- How to use it with DSG core:
  - extend ledger into region-aware audit proofs
  - add state-hash comparison endpoints
  - promote deterministic audit as a separate subsystem

### 4. Governance / Formal Framing
- Repository: `tdealer01-crypto/dsg-Legal-Governance`
- Role: ecosystem narrative, legal-governance positioning, formal safety framing
- Current value:
  - modular ecosystem framing
  - formal verification language
  - research and governance positioning
- How to use it with DSG core:
  - reuse terminology in docs and whitepapers
  - define policy update governance model
  - document long-term safety automaton and protocol commitments

## Secondary Repositories

### DSG Architect Mobile
- Repository: `tdealer01-crypto/dsg-architect-mobile`
- Role: possible mobile/operator UX surface
- Current value: product framing for mobile collaboration and project operations
- Use case: future mobile control plane or operator console

### CCDAI Governance Engine
- Repository: `tdealer01-crypto/ccdai-governance-engine`
- Role: placeholder for governance automation
- Use case: future rule update workflow, policy governance, voting or approval process

## Recommended Integration Order

1. Treat `DSG-Deterministic-Safety-Gate` as the protocol and runtime core
2. Treat `tdealer01-crypto-dsg-control-plane` as the product/control-plane layer
3. Fold deterministic audit ideas from `dsg-deterministic-audit` into ledger evolution
4. Fold governance language and lifecycle rules from `dsg-Legal-Governance` into policy governance
5. Use mobile and governance-engine repos as future surfaces, not current sources of truth

## Design Rule

Do not duplicate logic across repositories.

- Put execution truth here
- Put operator UX in the control plane repo
- Put cross-cloud determinism and advanced audit models in the audit repo
- Put governance, legal framing, and research articulation in the governance repo
