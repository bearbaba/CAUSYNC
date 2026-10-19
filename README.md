# CAUSYNC

**From evidence to accountable decisions.**

*Consensus-based fault attribution for multi-agent AI workflows.*

CAUSYNC is a standalone GenLayer Intelligent Contract primitive for resolving responsibility in workflows with three participating AI agents. An owner registers each case with a frozen obligations digest; after the owner commits a full evidence-document SHA-256, independent GenLayer validators review the same source and agree on a structured attribution verdict.

**Contract goal:** make a disputed outcome consequential through an immutable, case-scoped eligibility view, while treating missing or inconclusive evidence as **UNVERIFIABLE**, never as proof of failure.

## Scope (V1)

- One reusable contract, multiple case IDs; three distinct agent addresses per case.
- Immutable, on-chain spec SHA-256 and full evidence SHA-256 (the source URL is pinned at submission).
- Deterministic chain/case/agent envelope checks before semantic reasoning.
- Comparative consensus on decision, fault bitmask, document digest and verbatim supporting quotes.
- Verdicts: `NO_FAULT`, `AGENT_FAULT`, `SHARED_FAULT`, `UNVERIFIABLE`.
- Terminal, immutable verdict per case: `can_certify(case_id, agent)` denies blamed agents and denies everyone for inconclusive evidence.
- `NO_FAULT` requires affirmative obligation/trace evidence for all three agents; missing evidence can never grant a positive certificate.
- Network fetch failures and changed source hashes are **retriable** observations (`SOURCE_UNAVAILABLE`, `SOURCE_MISMATCH`), not terminal fault verdicts.
- Every terminal verdict is bound to the already pinned full-document SHA-256.
- No deposits or automated penalties. Each consumer decides how to use the **case-scoped** eligibility view.

## Verification milestones (fixed exit criteria)

1. Contract, bounded fixture format and local state/security tests.
2. GenVM lint and SDK DirectVM test green.
3. **Two** substantive finalized Studionet cases: proven fault and insufficient evidence.
4. One explicit invalid/unauthorized source or actor test, readable audit and finality receipts.
5. Link the contract, tests and evidence in a concise reviewer submission; stop. No frontend requirement.

## Repository and contract identity

- Repository: `bearbaba/CAUSYNC`
- Contract class: `Causync`
- Evidence envelope: `CAUSYNC_CASE_V1`
- Public API is unchanged from the initial prototype.

## Project files

- `contracts/causync.py` — standalone deployable GenLayer contract
- `tests/test_local.py` — deterministic state and evidence checks using a mocked GenLayer environment
- `tests/test_direct_genvm.py` — official SDK DirectVM smoke test
- `docs/ARCHITECTURE.md` — validator/evidence boundary, verdict state machine and integrator contract
- `docs/SECURITY.md` — defenses, residual threats and authority model
- `docs/DEMO.md` — bounded two-case Studio walkthrough, no invented receipts
- `docs/STUDIONET_EVIDENCE.md` — observed on-chain case results, immutable source hashes and receipt checklist
- `examples/case_01_fault.txt`, `examples/case_02_unverifiable.txt` — pinned test cases
- `scripts/prepare_case.py` — offline SHA-256 preparation for exact Studio inputs
- `LICENSE` — MIT license

## Core workflow

1. Owner: `create_case(agent_a, agent_b, agent_c, spec_sha256)`.
2. Owner: `submit_evidence(case_id, evidence_url, evidence_sha256)`.
3. Owner: `resolve_case(case_id)`; validators independently read, verify and classify.
4. Any caller: `case_status(case_id)`, `case_count()`, `can_certify(case_id, agent)`.

**Boundary:** a pinned digest establishes integrity, not the real-world truth of a log or publisher identity. In V1 the owner defines the workflow and pins evidence; participating agents do not cryptographically co-sign. AI agreement does not prove the trace really occurred. `can_certify()` attests only to that owner's evidence-bound case and must not be treated as global reputation. `UNVERIFIABLE` denies all certifications.

**Verification:** CI compiles sources, validates both fixtures, exercises mocked state/security tests and runs official GenVM lint and SDK DirectVM tests. See the [live demo protocol](docs/DEMO.md) for the remaining acceptance gate.

**Studionet progress (2026-10-19):** deployed instance `0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea` has user-provided on-chain readbacks for **Case #1: RESOLVED / AGENT_FAULT / fault mask 2** (with `can_certify(A/B/C) = true/false/true`) and **Case #2: RESOLVED / UNVERIFIABLE / mask 0**. The exact full evidence digests match in both cases. All seven complete transaction hashes have now been supplied and marked **FINALIZED** in a user-provided GenLayer Studio screenshot; receipt links appear in the Studionet evidence ledger. Case #2 `can_certify(A/B/C) = false/false/false` was confirmed by the user following full-address instructions; the exact input text was not independently captured. A separate non-owner `resolve_case(1)` test is documented with **FINALIZED / ERROR** and **5/5 validators reporting `[rollback] owner only`** in GenLayer Studio transaction details; [security receipt](https://explorer-studio.genlayer.com/tx/0x2a1161b31c645cbfffe15d20ba7385833b10ab3b56f21525eb4f69be6d7c0ba2). Independent Explorer fetching and a post-rejection state readback remain optional checks. See [Studionet evidence](docs/STUDIONET_EVIDENCE.md). This is not a mainnet security audit.

MIT License.
