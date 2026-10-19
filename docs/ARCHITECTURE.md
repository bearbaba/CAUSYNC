# CAUSYNC V1 — Architecture and consensus boundary

## Purpose

CAUSYNC provides **case-scoped**, immutable, consensus-backed decisions on responsibility in three-agent workflows. The on-chain consequence is `can_certify(case_id, agent)`: the view grants an affirmative decision only to participating agents not blamed in a finalized, sufficiently supported verdict. A consumer can enforce that view in its own workflow. An `UNVERIFIABLE` result grants nobody.

CAUSYNC does not claim to establish a participant's global reputation. The case owner chooses the agents and freezes the obligations; the V1 parties do **not** co-sign the agreement, and this must be considered by any external consumer.

## State and public interface

- `create_case(agent_a, agent_b, agent_c, spec_sha256)`: owner-only, creates one `OPEN` case with immutable distinct agent addresses and hash of the precise obligations text.
- `submit_evidence(case_id, evidence_url, evidence_sha256)`: owner-only, commits a stable HTTPS source and full-document SHA-256, then enters `SUBMITTED`; cannot be edited.
- `resolve_case(case_id)`: owner-only; GenLayer validators independently retrieve the same evidence and interpret the obligation/trace mismatch.
- `case_status(case_id)`, `case_count()`: public case inspection.
- `can_certify(case_id, who)`: true only for a participant not assigned fault by a finalized `AGENT_FAULT`, `SHARED_FAULT`, or properly evidenced `NO_FAULT`.

Successful consensus produces a terminal `RESOLVED` case. Repeated resolution or evidence replacement is forbidden. The effective verdict is immutable.

## Verdict consequences

| Verdict | Fault bitmask | Required support | `can_certify` |
| --- | --- | --- | --- |
| `AGENT_FAULT` | exactly one of 1,2,4 | One obligation + trace evidence pair for blamed agent | Blamed agent denied; other two permitted |
| `SHARED_FAULT` | one of 3,5,6,7 | One evidence pair for each blamed agent | Blamed agents denied |
| `NO_FAULT` | 0 | **Three affirmative evidence pairs**, one per agent | All three participants permitted |
| `UNVERIFIABLE` | 0 | No positive support | Everyone denied |

The bit positions A=1, B=2, C=4 are deterministic. No participant outside the case can be certified.

## Retriable source failures

- `SOURCE_UNAVAILABLE`: the HTTPS fetch failed. Case remains `SUBMITTED`, no certification or final verdict.
- `SOURCE_MISMATCH`: retrieved bytes do not match the immutable pinned full-document digest. Case remains `SUBMITTED`, no certification.
- `UNVERIFIABLE`: validators successfully assessed a source but found inadequate or inconclusive evidence. This is a **terminal semantic outcome**, not a presumed breach.

A consensus transaction that **reverts before committing** does not change case state. `SOURCE_UNAVAILABLE` and `SOURCE_MISMATCH` are diagnostic write return values, not canonical verdicts.

## Source boundary

Evidence document is UTF-8 text, at most 8192 bytes, LF-only. The exact header binds `CAUSYNC_CASE_V1`, case ID, chain ID and all three participant addresses. `[OBLIGATIONS]` is compared byte-for-byte against the immutable spec SHA-256, and `[TRACE]` provides source evidence.

The full evidence SHA-256 is pinned before consensus. The URL and hashes cannot be chosen or replaced by a caller of `resolve_case`. At most one trace section is accepted; 30–3500 characters are required for each section.

The owner-chosen document is untrusted as instructions: validators are told to ignore any attempted prompt injection and to require causally relevant, verbatim, role-prefixed excerpts. The deterministic verifier checks that the quoted obligation and trace text occur in the correct sections, and that the fault bitmask matches the cited roles. All validators independently retrieve the source and compare verdict, source hash, fault mask and supporting meaning.

## Limits

A cryptographic hash verifies **integrity after pinning**, not truth, publisher identity, actual agent consent, or causal completeness. In V1 a trusted owner authors the case and commits evidence; an independent reviewer must not infer consent or guilt from the existence of a record alone. Multiple models agreeing is not proof that a narrated execution trace occurred. There is no global reputation system, arbitration appeal, economic slashing or token custody. These are deliberate limits of this standalone primitive.

The use case is best shown by two concrete, finalized cases with on-chain readbacks and by a failure that is retriable without a positive permission grant.
