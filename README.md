# TRACEJURY

**Consensus-based fault attribution for multi-agent workflows.**

TRACEJURY is a standalone GenLayer Intelligent Contract primitive for resolving responsibility in workflows with three participating AI agents. An owner registers each case with a frozen obligations digest; after the owner commits a full evidence-document SHA-256, independent GenLayer validators review the same source and agree on a structured attribution verdict.

**Contract goal:** make a disputed outcome consequential through an immutable, case-scoped eligibility view, while treating missing or inconclusive evidence as **UNVERIFIABLE**, never as proof of failure.

## Scope (V1)

- One reusable contract, multiple case IDs; three distinct agent addresses per case.
- Immutable, on-chain spec SHA-256 and full evidence SHA-256 (the source URL is pinned at submission).
- Deterministic chain/case/agent envelope checks before semantic reasoning.
- Comparative consensus on decision, fault bitmask, document digest and verbatim supporting quotes.
- Verdicts: `NO_FAULT`, `AGENT_FAULT`, `SHARED_FAULT`, `UNVERIFIABLE`.
- Permanent outcome per case; `can_certify(case_id, agent)` denies blamed agents and denies everyone when unverified.
- No tokens, deposits or automated punishment. The consumer decides how to use the eligibility view.

## Verification milestones (fixed exit criteria)

1. Contract, bounded fixture format and local state/security tests.
2. GenVM lint and SDK DirectVM test green.
3. **Two** substantive finalized Studionet cases: proven fault and insufficient evidence.
4. One explicit invalid/unauthorized source or actor test, readable audit and finality receipts.
5. Link the contract, tests and evidence in a concise reviewer submission; stop. No frontend requirement.

## Project files

- `contracts/tracejury.py` — standalone deployable GenLayer contract
- `tests/test_local.py` — deterministic state and evidence checks using a mocked GenLayer environment
- `tests/test_direct_genvm.py` — official SDK DirectVM smoke test
- `docs/ARCHITECTURE.md` — trust model and validation protocol
- `docs/DEMO.md` — live verification and evidence recording procedure
- `examples/` — local illustrative evidence fixtures, not authority for actual cases

## Core workflow

1. Owner: `create_case(agent_a, agent_b, agent_c, spec_sha256)`.
2. Owner: `submit_evidence(case_id, evidence_url, evidence_sha256)`.
3. Owner: `resolve_case(case_id)`; validators independently read, verify and classify.
4. Any caller: `case_status(case_id)`, `case_count()`, `can_certify(case_id, agent)`.

**Boundary:** a pinned digest establishes integrity, not the real-world truth of a log or publisher identity. Caller authorization and immutable hashes do not prove a document was genuine. AI agreement alone does not guarantee causal truth. The prototype deliberately makes `UNVERIFIABLE` deny positive certifications.

Current status: source-development phase. Do not claim a successful deployment or FINALIZED receipt before evidence exists.

MIT License.
