# CAUSYNC — Minimal Studionet demo

This procedure is **not yet claimed as completed**. The supplied two fixtures are illustrative, synthetically authored cases. No real AI agent's responsibility is asserted.

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
3. Call `submit_evidence(1, "https://raw.githubusercontent.com/bearbaba/CAUSYNC/main/examples/case_01_fault.txt", evidence_sha256)`. Confirm `SUBMITTED` and frozen URL/hash in `case_status(1)`.
4. Call `resolve_case(1)` using **Normal (Full Consensus)**. Wait for Explorer **FINALIZED**. The target result is `AGENT_FAULT` with mask `2`, but this is a model consensus outcome, not a guaranteed string. Validate source hashes, support excerpts, `case_status(1)`, `can_certify(1, A)=true`, `can_certify(1, B)=false`, `can_certify(1, C)=true`. Do not claim success if actual receipt differs.
5. Create Case 2 using the printed Case 2 `spec_sha256`, and confirm its actual returned ID **2**. Then submit its evidence URL `https://raw.githubusercontent.com/bearbaba/CAUSYNC/main/examples/case_02_unverifiable.txt` plus Case 2 `evidence_sha256`.
6. Resolve Case 2 with full consensus; the expected semantic result is `UNVERIFIABLE`, mask `0`, and all three `can_certify` reads false. Confirm the actual transaction is **FINALIZED** before recording.
7. Negative case: Attempt an owner-only write from an unauthorized address **or** verify that an altered copy of the pinned evidence returns `SOURCE_MISMATCH` without resolving or granting permissions. Only one negative scenario is required for this phase.

If Studio assigns a different case ID, uses a chain other than 61999, or normalizes a different wallet representation, **do not reuse the sample hash/URL as-is**. Rebuild the fixture with the real case ID/chain/agent identities, re-run the offline helper and pin the resulting exact document.

## Evidence checklist (record only actual receipts)

| Artifact | Observed result | Explorer URL |
| --- | --- | --- |
| Deployment | PENDING | — |
| Case 1 create/submit/resolve | PENDING | — |
| Case 1 audit + permission reads | PENDING | — |
| Case 2 create/submit/resolve | PENDING | — |
| Case 2 all-denied permission reads | PENDING | — |
| Unauthorized/invalid negative case | PENDING | — |
| Final CI for deployed commit | Verify Green | — |

**Exit:** Two substantive `FINALIZED` resolutions and one scoped negative check with inspectable readbacks, plus passing CI and evidence documentation. No extra adversarial campaigns unless a genuine blocker appears.
