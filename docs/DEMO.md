# CAUSYNC — Minimal Studionet demo

This procedure is **not yet claimed as completed**. The supplied two fixtures are illustrative, synthetically authored cases. No real AI agent's responsibility is asserted.

## Deployed Studio instance and exact fixture digests

- Studio link: https://studio.genlayer.com/?import-contract=0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea
- Deployment contract address: `0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea`.
- User-provided Studio screenshot (2026-10-19) displays **FINALIZED** for deployment plus all six case-write transactions. All seven full hashes are in [STUDIONET_EVIDENCE.md](STUDIONET_EVIDENCE.md). Independent Explorer fetch not yet completed.
- Verified CI run: https://github.com/bearbaba/CAUSYNC/actions/runs/39215696385
- Pinned fixture commit: `158573ff86c5a08334d8a4ab5354fecd61ad4309` (both fixture files present at this commit).

| Demo case | Case ID (expected) | `spec_sha256` | `evidence_sha256` |
| --- | ---: | --- | --- |
| Agent B breach | 1 | `ff527852a66909b72f36865ed03a40ec6a5c36aad3439eb08ce22247ca1e9e77` | `f501541ffda08c2765dc4d0774f5076d4b8e1d5c40c8f7ef716cf289ec366a50` |
| Insufficient trace | 2 | `ff527852a66909b72f36865ed03a40ec6a5c36aad3439eb08ce22247ca1e9e77` | `56e937ad0d7cea6ebb768ba5a0bd028e50fe94145f1264abd02c897b2f28bdcc` |

Use commit-pinned raw evidence to guarantee immutability across future `main` updates:
- Case 1: `https://raw.githubusercontent.com/bearbaba/CAUSYNC/158573ff86c5a08334d8a4ab5354fecd61ad4309/examples/case_01_fault.txt`
- Case 2: `https://raw.githubusercontent.com/bearbaba/CAUSYNC/158573ff86c5a08334d8a4ab5354fecd61ad4309/examples/case_02_unverifiable.txt`

Hashes above were taken directly from the successful GitHub Actions fixture validation output, not manually estimated. If `case_count()` was nonzero before the demo, these exact `CASE_ID`-bound documents must not be used unchanged.

## Fixed demo input

- Network: GenLayer Studionet, chain ID **61999**.
- Contract source: `contracts/causync.py`, class `Causync`.
- Example agents: `0x1111111111111111111111111111111111111111`, `0x2222222222222222222222222222222222222222`, `0x3333333333333333333333333333333333333333`.
- Case 1: `examples/case_01_fault.txt` — planned demonstrated breach by Agent B.
- Case 2: `examples/case_02_unverifiable.txt` — planned lack of primary evidence.
- Policy: use the exact pinned source **without edits after hash commitment**, keep HTTPS and no URL query or fragment.

## Prepare hashes offline

```bash
python scripts/prepare_case.py examples/case_01_fault.txt
python scripts/prepare_case.py examples/case_02_unverifiable.txt
```

The script prints two distinct values: `spec_sha256` = SHA-256 of the exact obligations text alone, `evidence_sha256` = SHA-256 of the complete document. Never interchange them.

## Execute in Studio (one deployed contract)

1. Import/deploy `contracts/causync.py` to Studionet with the parameterless constructor.
2. From the deployer/owner, call `create_case(A, B, C, spec_sha256)` for Case 1. Confirm returned ID **1** and case state `OPEN`.
3. Call `submit_evidence(1, "https://raw.githubusercontent.com/bearbaba/CAUSYNC/158573ff86c5a08334d8a4ab5354fecd61ad4309/examples/case_01_fault.txt", evidence_sha256)`. Confirm `SUBMITTED` and frozen URL/hash in `case_status(1)`.
4. Call `resolve_case(1)` using **Normal (Full Consensus)**. Wait for Explorer **FINALIZED**. The target result is `AGENT_FAULT` with mask `2`, but this is a model consensus outcome, not a guaranteed string. Validate source hashes, support excerpts, `case_status(1)`, `can_certify(1, A)=true`, `can_certify(1, B)=false`, `can_certify(1, C)=true`. Do not claim success if actual receipt differs.
5. Create Case 2 using the printed Case 2 `spec_sha256`, and confirm its actual returned ID **2**. Then submit its evidence URL `https://raw.githubusercontent.com/bearbaba/CAUSYNC/158573ff86c5a08334d8a4ab5354fecd61ad4309/examples/case_02_unverifiable.txt` plus Case 2 `evidence_sha256`.
6. Resolve Case 2 with full consensus; the expected semantic result is `UNVERIFIABLE`, mask `0`, and all three `can_certify` reads false. Confirm the actual transaction is **FINALIZED** before recording.
7. Negative case: Attempt an owner-only write from an unauthorized address **or** verify that an altered copy of the pinned evidence returns `SOURCE_MISMATCH` without resolving or granting permissions. Only one negative scenario is required for this phase.

If Studio assigns a different case ID, uses a chain other than 61999, or normalizes a different wallet representation, **do not reuse the sample hash/URL as-is**. Rebuild the fixture with the real case ID/chain/agent identities, re-run the offline helper and pin the resulting exact document.

## Evidence checklist (record only actual receipts)

Detailed Case #1 and Case #2 readbacks: [STUDIONET_EVIDENCE.md](STUDIONET_EVIDENCE.md).

| Artifact | Observed result | Explorer URL |
| --- | --- | --- |
| Deployment | **FINALIZED (Studio screenshot)** | [Transaction](https://explorer-studio.genlayer.com/tx/0x667e61933e7223fbefcaf91e40b43fc5e5ab584bcd594a0f8c4efb8a3f920a29) |
| Case 1 create | **FINALIZED (Studio screenshot)** | [Transaction](https://explorer-studio.genlayer.com/tx/0xcad9c673dd5b0a6fe7b7eb9fc63e76d33a276a80ad828954fc3811f5e840fa96) |
| Case 1 resolution | **FINALIZED (Studio screenshot)**; RESOLVED / AGENT_FAULT / mask 2 readback | [Transaction](https://explorer-studio.genlayer.com/tx/0x565478addfba9d7836c5e2541c6c33f9e8ca88cbfcf56777131ef991e186e42a) |
| Case 1 source digest + support | Exact digest matches; Agent B obligation and breach quotes recorded | — |
| Case 1 can_certify(A/B/C) | **true / false / true** (user-provided readbacks) | — |
| Case 2 create/submit/resolve | **FINALIZED (Studio screenshot)**; RESOLVED / UNVERIFIABLE / mask 0 readback | [Resolution](https://explorer-studio.genlayer.com/tx/0x7f162523c0c6613996881dae408b995d569d2e9459fcb44f838b0d9b2c2280bb) |
| Case 2 all-denied permission reads | **false / false / false** confirmed by user after full-address instructions | — |
| Unauthorized non-owner `resolve_case(1)` | **FINALIZED / ERROR; 5/5 validators `[rollback] owner only`**, confirmed in user's Studio transaction detail screenshot | [Transaction](https://explorer-studio.genlayer.com/tx/0x2a1161b31c645cbfffe15d20ba7385833b10ab3b56f21525eb4f69be6d7c0ba2) |
| Final CI for deployed commit | Verify Green | — |

**Exit:** Two substantive `FINALIZED` resolutions and one scoped negative check with inspectable readbacks, plus passing CI and evidence documentation. No extra adversarial campaigns unless a genuine blocker appears.
