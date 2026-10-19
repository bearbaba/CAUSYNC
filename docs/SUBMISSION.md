# CAUSYNC — Intelligent Contracts submission (19/10/2026)

## Form
- Contribution Type: **Builder**
- Category: **Intelligent Contracts**
- Date: **19/10/2026**
- Title: **CAUSYNC — Consensus-Based Fault Attribution**
- Notes / Description: **966/1000 characters**

CAUSYNC is a GenLayer Intelligent Contract for evidence-bound fault attribution in multi-agent workflows. Cases pin agent identities, obligations and an evidence SHA-256. Independent validators fetch the same source and use comparative consensus to distinguish proven breaches, shared responsibility, no fault and insufficient evidence. Equivalence checks the source hash, fault mask and verbatim obligation/trace citations.

Resolved cases expose can_certify(case_id, agent), turning consensus into a case-scoped eligibility decision. Inconclusive evidence denies certification; changed or unavailable sources cannot finalize a verdict. Owner-only writes and immutable outcomes secure the lifecycle.

Two FINALIZED Studionet resolutions produced AGENT_FAULT (Agent B; true/false/true) and UNVERIFIABLE (false/false/false). A separate unauthorized call was rejected with "owner only", agreed by all five validators. Source, tests and transaction receipts are public.

## Evidence & Supporting Information

1. **CAUSYNC repository** (GitHub Repository)
   https://github.com/bearbaba/CAUSYNC

2. **Intelligent Contract source** (GitHub File)
   https://github.com/bearbaba/CAUSYNC/blob/main/contracts/causync.py

3. **Deployed contract in Studio** (GenLayer Studio)
   https://studio.genlayer.com/?import-contract=0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea

4. **Case #1 AGENT_FAULT resolution FINALIZED** (GenLayer transaction)
   https://explorer-studio.genlayer.com/tx/0x565478addfba9d7836c5e2541c6c33f9e8ca88cbfcf56777131ef991e186e42a

5. **Case #2 UNVERIFIABLE resolution FINALIZED** (GenLayer transaction)
   https://explorer-studio.genlayer.com/tx/0x7f162523c0c6613996881dae408b995d569d2e9459fcb44f838b0d9b2c2280bb

6. **Unauthorized resolve_case blocked 5/5 validators** (GenLayer transaction)
   https://explorer-studio.genlayer.com/tx/0x2a1161b31c645cbfffe15d20ba7385833b10ab3b56f21525eb4f69be6d7c0ba2

7. **Full Studionet receipts and readbacks** (GitHub File)
   https://github.com/bearbaba/CAUSYNC/blob/main/docs/STUDIONET_EVIDENCE.md

8. **Architecture and validator/equivalence policy** (GitHub File)
   https://github.com/bearbaba/CAUSYNC/blob/main/docs/ARCHITECTURE.md

9. **Security model** (GitHub File)
   https://github.com/bearbaba/CAUSYNC/blob/main/docs/SECURITY.md

10. **CI passing with official GenVM/DirectVM** (GitHub Actions)
   https://github.com/bearbaba/CAUSYNC/actions/runs/39228270410

## Evidence accuracy

- The user supplied Studio screenshots showing seven lifecycle transactions marked FINALIZED, plus readbacks: Case #1 `RESOLVED/AGENT_FAULT` with `can_certify(A/B/C) = true/false/true`; Case #2 `RESOLVED/UNVERIFIABLE` with `false/false/false`.
- The non-owner transaction is a FINALIZED **execution ERROR**; its Studio transaction details show five validators recording `[rollback] owner only` with `Agree`. Do not label this error transaction a successful method execution.
- Links to Explorer are built from exact user-supplied transaction hashes. Independent Explorer receipt inspection is not claimed.
- Source and architecture describe a case-scoped primitive; evidence fixtures are synthetic examples. No agent signatures or third-party proof of execution are implied.
- Do not claim the submission itself is complete until the contribution portal acknowledges it.
