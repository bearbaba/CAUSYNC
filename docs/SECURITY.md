# CAUSYNC — Security model

CAUSYNC V1 is an evidence-bound GenLayer Intelligent Contract prototype. This document identifies observable guarantees, authority boundaries and remaining risks.

## Implemented invariants

1. Only the original contract owner can create a case, commit evidence or trigger resolution.
2. Three agent addresses are distinct, nonzero and immutable once a case is created.
3. The source URL and full SHA-256 are pinned before resolution; no caller-supplied alternative source can enter a resolution transaction.
4. Case ID, chain and agent identities must match the exact evidence header. Obligation text must hash to the on-chain spec digest.
5. The document is bounded to 8192 bytes, has canonical LF newlines and exactly one obligations and trace section.
6. No-fault positive certifications require evidence for all three participants. A blamed agent needs a matched pair of obligation and trace quotes.
7. Faults require a role-exact bitmask with no duplicated role or unsupported claim.
8. Unverifiable evidence denies all certifications. Source fetch or digest failures retain the `SUBMITTED` state, permitting retry without granting rights.
9. Successful resolutions cannot be changed or replayed against an already-resolved case.
10. Unknown or unrelated addresses never pass `can_certify`.

## Threats and residual assumptions

| Threat | Handling / limitation |
| --- | --- |
| Wrong chain/case/agent | Canonical envelope rejects the mismatching document before semantic analysis |
| Changed hosted bytes | Full SHA-256 mismatch returns `SOURCE_MISMATCH` and grants no permission |
| Unreachable host | `SOURCE_UNAVAILABLE`, no finalization, safe retry |
| Fabricated quote | Model outputs must quote verbatim from matching obligations/trace sections; a malformed candidate abstains |
| Unproven all-clear | NO_FAULT requires all three independent role citations |
| Malicious participant | No agent can create or resolve another owner's case unless they control the owner account |
| Malicious owner / forged trace | **Not solved**: owner may present self-authored claims, agents do not sign, and no independent provenance is cryptographically guaranteed |
| Prompt injection | Untrusted source is data, validators instructed to ignore commands; semantic manipulation is still possible |
| Validator/model disagreement | Consensus may fail/revert; no state change should be inferred from a pending or nonfinal transaction |
| Downstream overtrust | Consumer must check correct case owner, case ID, chain, actor and FINALIZED state before using a certification |

## Operational boundaries

Only use demo addresses and evidence with no private keys, passwords, real client data or funds. `can_certify` is a case-scoped permission view, not an automatic payout or reputation penalty. The project does not make any claim that the evidence is a signed agent-origin log. Audit externally retained source snapshots and receipts because storing source hashes on-chain does not preserve the complete historical document.

Review historical Explorer receipt `FINALIZED` and match the returned `case_status` after every write. An `ACCEPTED` consensus result alone is not proof of finality. Testnet conditions and GenVM rules can change.
