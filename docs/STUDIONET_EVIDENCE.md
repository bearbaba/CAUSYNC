# CAUSYNC — Studionet Evidence Ledger

## Deployed instance
- Network: GenLayer Studionet (chain ID 61999).
- Contract: `0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea`
- Studio: https://studio.genlayer.com/?import-contract=0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea
- Source: https://github.com/bearbaba/CAUSYNC/blob/main/contracts/causync.py
- Local/GenVM CI: https://github.com/bearbaba/CAUSYNC/actions/runs/39215696385 (success)
- A later Studio screenshot (2026-10-19) displays the deployment and all six case-write transactions as **FINALIZED**. Full hashes are listed below; Explorer confirmation has not been independently fetched.

## Finalized transaction receipts — reported from GenLayer Studio (2026-10-19)

The user supplied all seven complete transaction hashes, and the Studio Transactions panel screenshot labels **each one FINALIZED**. The transaction-to-action mapping below follows the ordered Studio panel. These are screenshot-reported statuses; an independent Explorer receipt fetch has not been performed.

| Step | Studio status | Explorer transaction |
| --- | --- | --- |
| Deployment | **FINALIZED (Studio screenshot)** | [`0x667e61933e7223fbefcaf91e40b43fc5e5ab584bcd594a0f8c4efb8a3f920a29`](https://explorer-studio.genlayer.com/tx/0x667e61933e7223fbefcaf91e40b43fc5e5ab584bcd594a0f8c4efb8a3f920a29) |
| Case #1: create_case | **FINALIZED (Studio screenshot)** | [`0xcad9c673dd5b0a6fe7b7eb9fc63e76d33a276a80ad828954fc3811f5e840fa96`](https://explorer-studio.genlayer.com/tx/0xcad9c673dd5b0a6fe7b7eb9fc63e76d33a276a80ad828954fc3811f5e840fa96) |
| Case #1: submit_evidence | **FINALIZED (Studio screenshot)** | [`0x242364c9e2846e8cd133afc4aa6e2212575ac55eca7e4cc683697d9acbb9cc4c`](https://explorer-studio.genlayer.com/tx/0x242364c9e2846e8cd133afc4aa6e2212575ac55eca7e4cc683697d9acbb9cc4c) |
| Case #1: resolve_case | **FINALIZED (Studio screenshot)** | [`0x565478addfba9d7836c5e2541c6c33f9e8ca88cbfcf56777131ef991e186e42a`](https://explorer-studio.genlayer.com/tx/0x565478addfba9d7836c5e2541c6c33f9e8ca88cbfcf56777131ef991e186e42a) |
| Case #2: create_case | **FINALIZED (Studio screenshot)** | [`0x6e1ae2fabe8adb587d4470c85a6d5dc3c8887ddc4f6e438a3e04490b6cce7828`](https://explorer-studio.genlayer.com/tx/0x6e1ae2fabe8adb587d4470c85a6d5dc3c8887ddc4f6e438a3e04490b6cce7828) |
| Case #2: submit_evidence | **FINALIZED (Studio screenshot)** | [`0xb43d8fa1be646d34d9c7c8cb9ae133a8ff2b7620c16f446da94a369e4ae9d127`](https://explorer-studio.genlayer.com/tx/0xb43d8fa1be646d34d9c7c8cb9ae133a8ff2b7620c16f446da94a369e4ae9d127) |
| Case #2: resolve_case | **FINALIZED (Studio screenshot)** | [`0x7f162523c0c6613996881dae408b995d569d2e9459fcb44f838b0d9b2c2280bb`](https://explorer-studio.genlayer.com/tx/0x7f162523c0c6613996881dae408b995d569d2e9459fcb44f838b0d9b2c2280bb) |

## Case #1 — Proven agent breach

**User-provided public-method readback on 2026-10-19:**

| Field | Observed value |
| --- | --- |
| `case_id` | `1` |
| `chain_id` | `61999` |
| `state` | **`RESOLVED`** |
| `verdict` | **`AGENT_FAULT`** |
| `fault_mask` | **`2` — Agent B** |
| `owner` | `0x4C7cb73aC8F8999af21cfc9fF4cF2333a9508Dcb` |
| `agent_a` | `0x1111111111111111111111111111111111111111` |
| `agent_b` | `0x2222222222222222222222222222222222222222` |
| `agent_c` | `0x3333333333333333333333333333333333333333` |
| `spec_sha256` | `ff527852a66909b72f36865ed03a40ec6a5c36aad3439eb08ce22247ca1e9e77` |
| `evidence_sha256` | `f501541ffda08c2765dc4d0774f5076d4b8e1d5c40c8f7ef716cf289ec366a50` |
| `source_sha256` | `f501541ffda08c2765dc4d0774f5076d4b8e1d5c40c8f7ef716cf289ec366a50` |
| `support_sha256` | `1decd7194d8b3173ded83650ed3a2966e195010143ccd5f6fd48c0551f5fc749` |

Frozen evidence:
https://raw.githubusercontent.com/bearbaba/CAUSYNC/158573ff86c5a08334d8a4ab5354fecd61ad4309/examples/case_01_fault.txt

Consensus-supported responsibility:

- **Obligation:** `Agent B must implement the approved inventory totals without changing quantities.`
- **Trace:** `Agent B changed quantity 12 to 21 in the submitted implementation without authorization.`
- **Attributed participant:** Agent B (`fault_mask = 2`).

The `source_sha256` matches the pinned `evidence_sha256`. The contract stores excerpts and their `support_sha256`.

**Observed permission readbacks supplied by the user on 2026-10-19:** `can_certify(1, A) = true`, `can_certify(1, B) = false`, `can_certify(1, C) = true`. This demonstrates the case-scoped consequence of the verdict. The Case #1 resolution TX is now linked above and marked FINALIZED in the supplied Studio screenshot. The readbacks are user-provided observations; independent Explorer finality has not been checked.

## Case #2 — Insufficient evidence

**User-provided `case_status(2)` readback on 2026-10-19:**

| Field | Observed value |
| --- | --- |
| `case_id` | `2` |
| `chain_id` | `61999` |
| `state` | **`RESOLVED`** |
| `verdict` | **`UNVERIFIABLE`** |
| `fault_mask` | `0` |
| `owner` | `0x4C7cb73aC8F8999af21cfc9fF4cF2333a9508Dcb` |
| `agent_a` | `0x1111111111111111111111111111111111111111` |
| `agent_b` | `0x2222222222222222222222222222222222222222` |
| `agent_c` | `0x3333333333333333333333333333333333333333` |
| `spec_sha256` | `ff527852a66909b72f36865ed03a40ec6a5c36aad3439eb08ce22247ca1e9e77` |
| `evidence_sha256` | `56e937ad0d7cea6ebb768ba5a0bd028e50fe94145f1264abd02c897b2f28bdcc` |
| `source_sha256` | `56e937ad0d7cea6ebb768ba5a0bd028e50fe94145f1264abd02c897b2f28bdcc` |
| `support_sha256` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |
| `support` | `[]` |

Frozen example:
https://raw.githubusercontent.com/bearbaba/CAUSYNC/158573ff86c5a08334d8a4ab5354fecd61ad4309/examples/case_02_unverifiable.txt

The `source_sha256` matches the immutable `evidence_sha256`; the on-chain result was `UNVERIFIABLE`, not a fabricated fault accusation. The empty support list and mask zero agree with that decision. This is a user-provided **readback**. The Case #2 resolution TX is now linked above and marked FINALIZED in the Studio screenshot (not separately verified in Explorer). The user has now confirmed all three `can_certify(2, A/B/C)` readbacks returned `false / false / false` after being instructed to use full 42-character participant addresses. This is a user-reported observation; the exact submitted address input text was not separately captured. The all-denied result matches the terminal `UNVERIFIABLE` verdict.

## Remaining verification

- [x] Seven full transaction hashes recorded, all displayed as **FINALIZED** in the user's Studio screenshot.
- [x] Case #1 `can_certify` readbacks using complete agent addresses: `true / false / true`.
- [x] Both cases: `RESOLVED` readbacks, digest matches, verdicts and supporting evidence recorded.
- [x] Case #2 `can_certify(2, A/B/C)` all denied: `false / false / false` (user-confirmed after full-address guidance; exact input text not independently captured).
- [ ] Optionally cross-check receipt details directly in Explorer; linked URLs above come from the user-supplied hashes.
- [ ] One live unauthorized/invalid test if required to satisfy the original acceptance protocol; negative access tests already pass in CI.

No real disputes, attestations of consent, or authentic third-party execution traces are asserted by these **synthetic demonstration cases**.
