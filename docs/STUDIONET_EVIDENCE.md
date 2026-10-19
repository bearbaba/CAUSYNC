# CAUSYNC — Studionet Evidence Ledger

## Deployed instance
- Network: GenLayer Studionet (chain ID 61999).
- Contract: `0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea`
- Studio: https://studio.genlayer.com/?import-contract=0xe9224eE4b220a8eFdd6000d26bE2217bD59972Ea
- Source: https://github.com/bearbaba/CAUSYNC/blob/main/contracts/causync.py
- Local/GenVM CI: https://github.com/bearbaba/CAUSYNC/actions/runs/39215696385 (success)
- Deployment visible as `ACCEPTED` in provided screenshot; Explorer FINALIZED receipt not yet supplied.

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

**Observed permission readbacks supplied by the user on 2026-10-19:** `can_certify(1, A) = true`, `can_certify(1, B) = false`, `can_certify(1, C) = true`. This demonstrates the case-scoped consequence of the verdict. The user previously reported a finalized Case #1 creation, but **the resolution transaction hash and its Explorer FINALIZED receipt have not been supplied**. The readbacks are recorded as user-provided observations, not independently verified Explorer finality.

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

The `source_sha256` matches the immutable `evidence_sha256`; the on-chain result was `UNVERIFIABLE`, not a fabricated fault accusation. The empty support list and mask zero agree with that decision. This is a user-provided **readback**, not yet an independently confirmed `FINALIZED` resolution transaction. The three `can_certify(2, A/B/C)` results have not yet been supplied; the expected results under the deployed contract's logic are `false`, `false`, `false`.

## Remaining evidence

- [ ] Explorer `FINALIZED` deployment TX.
- [ ] Explorer `FINALIZED` Case #1 resolve transaction (Case #1 can_certify A/B/C readbacks already recorded).
- [ ] Explorer `FINALIZED` Case #2 resolve transaction; case_status(2) readback recorded.
- [ ] Three `can_certify(2, A/B/C)` readbacks (expected false/false/false).
- [ ] One unauthorized/invalid attempt and its receipt or rejection trace.

No real disputes, attestations of consent, or authentic third-party execution traces are asserted by these **synthetic demonstration cases**.
