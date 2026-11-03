# SplitProof

SplitProof allocates a finite pool of declared evidence or deliverable units to
requirements, combining independent semantic eligibility judgments with exact
capacity accounting and irreversible onchain consumption.

**Verified deployment — November 3, 2026.** Version `1.0.1` is deployed at
[0x46eb745bDF73565dE0C54301EF529dd63d568Df5](https://explorer-studio-next.genlayer.com/address/0x46eb745bDF73565dE0C54301EF529dd63d568Df5).
Its full source matches the local file after documented text normalization.
The synthetic demo stored `READY` with the complete greedy-trap assignment, then
separately consumed the exact receipt and both declared capacity tokens.
[DEPLOYMENT.md](DEPLOYMENT.md) records the actual transactions and persisted state.

## The useful boundary

A program can count tokens but cannot reliably decide whether a natural-language
unit description supports a differently worded requirement, including exceptions.
A model can suggest a matching but cannot safely own capacity accounting.
SplitProof separates those jobs:

1. The pool owner freezes complete unit descriptions and explicit token capacities.
2. A batch freezes the complete current pool, remaining capacities, purpose,
   beneficiary, requirements, epoch and expiry.
3. GenLayer independently assesses **every requirement–unit cell**.
4. Deterministic backtracking finds the lexicographically first complete matching
   over certified `ELIGIBLE` cells, respecting all remaining capacities.
5. A second complete-source semantic assessment checks that **exact allocation as
   a whole**. A valid matrix and counts do not override joint contradictions.
6. The exact beneficiary separately consumes a validated `READY` receipt. An
   epoch and full-snapshot compare-and-swap prevents simultaneous batches from
   spending the same capacity.

For example, suppose unit `a` can cover CSV or JSON training and unit `b` can
cover CSV training only, each with one token. A greedy allocator could give `a`
to the CSV requirement and incorrectly reject JSON. SplitProof backtracks and
assigns CSV to `b`, JSON to `a`. Assessment alone consumes nothing.

Use cases include capacity-limited milestone evidence, declared training or
review entitlements, and workflows whose agreed rules prohibit reusing the same
evidence allowance across applications. The primitive does not require a frontend.

## Explicit scope

The owner supplies the units, descriptions and capacities. Those capacities are
**agreed contract rules**, not proof of physical inventory or external delivery.
A capacity of two permits two tokens by definition; the contract never infers
that a description proves two real-world objects. The unit IDs identify the
declared pool. The primitive does not establish global originality, authenticity,
ownership, absence of duplicates outside the pool, truth or legal enforceability.
An integrating application must authenticate its source material separately.
Consumption is scoped to this exact contract and pinned pool ID/hash. An owner
can open a different pool describing the same outside artifact; SplitProof does
not prevent that. Integrations must pin the approved pool rather than treating
all pools or deployments as one global evidence registry.
All text and resulting receipts are public. Use synthetic or already-public data.
The contract holds no funds and executes no external work or payments.

## State and finality

```text
Pool: ACTIVE -- irreversible allocation --> ACTIVE at epoch + 1
             -- owner retirement -------> RETIRED

Batch: PROPOSED / RETRYABLE
         -> READY -------- beneficiary allocation ------> ALLOCATED
         -> INSUFFICIENT
         -> INCONCLUSIVE
         -> CONFLICT
         -> RETRYABLE -> ... -> UNRESOLVED_FINAL (3 accepted attempts)
       PROPOSED / RETRYABLE / READY -- owner cancellation --> CANCELED
```

`READY` is an assessment, not a reservation. A stale or expired batch cannot be
assessed or consumed, regardless of its displayed historical status. Create a
new batch against the current snapshot; old receipts are never rewritten.
Retirement prevents new batches, assessments and allocations while preserving
all existing history. A canceled or allocated batch cannot be reused.
Capacity is never replenished or released. There is no refund or recycling path.

If certified `ELIGIBLE` cells cannot form a complete matching, a second
**deterministic optimistic matching** treats `UNCERTAIN` cells as eligible only
to diagnose the blockage:

- If that hypothetical matching could work, the final decision is `INCONCLUSIVE`.
- If even that matching cannot work, the final decision is `INSUFFICIENT`.

Neither branch authorizes allocation or invokes the whole-allocation prompt.
`INSUFFICIENT` concerns the supplied descriptions and declared capacity graph;
it is not proof that real-world evidence or alternatives cannot exist.

For a complete certified matching, the whole-allocation result is `COHERENT`,
`CONFLICT` or `UNCERTAIN`. Only `COHERENT` produces `READY`. A conflict or unclear
joint effect is final for that batch. The contract does not silently search for a
different matching after a semantic refusal, so another valid plan could exist.

## Consensus and receipt validation

The leader and every validating execution independently rebuild both semantic
stages, the complete matrix, deterministic matching, token counts and receipt.
Validation requires exact canonical JSON equality for the **entire persisted
payload**, not merely a verdict, digest or selected fields. No model-written
narrative is persisted. A differing model graph or whole verdict prevents
agreement; successful convergence or semantic correctness is not guaranteed.

Receipts bind the full frozen request, beneficiary and expiry, complete capacity
snapshot, every matrix cell, exact assignment, token counts, hashes, both prompt
character/UTF-8 counts and hashes, truncation flags, semantic-completion status,
attempt number and final authorization flag. Accepted malformed-output or model
failure receipts are retryable up to three accepted attempts. A network-level
consensus failure does not count as an accepted contract attempt.

All source strings are untrusted data. Source text is preserved exactly as valid
UTF-8 without stripping or slicing. Both complete prompts are budget-checked
before a batch is stored, using a conservative upper bound for the second
prompt. The actual complete prompts are checked again before inference.
Time is captured only in deterministic public methods with
`datetime.now(timezone.utc)`, using the Studio-compatible clock path. Model
receipt reconstruction never reads a clock. Version `1.0.1` changes only this
runtime clock adapter; receipt schema remains `splitproof-v1`.

## Public API

### Writes

```text
open_pool(title, purpose, units_json) -> pool_id
open_batch(pool_id, expected_epoch, expected_snapshot_hash,
           beneficiary, requirements_json, validity_seconds) -> batch_id
assess_batch(batch_id) -> complete_receipt
allocate(batch_id, expected_receipt_hash) -> allocation_id
cancel_batch(batch_id)
retire_pool(pool_id)
```

The pool owner opens batches, cancels unallocated batches and retires the pool.
The owner or exact beneficiary can assess a batch. Only the exact beneficiary
can consume it. All writes use transaction value **0 GEN**; network fees remain
separate.

### Reads

```text
get_pool(pool_id)
get_snapshot(pool_id) -> {snapshot, snapshot_hash}
get_batch(batch_id)
get_allocation(allocation_id)
get_attempt(batch_id, attempt)
get_stats()
```

### Bounds and input formats

- Units: 1–6, sorted by unique ASCII `unit_id` (1–40 lowercase letters, digits,
  hyphen or underscore). Each description is 1–600 nonblank characters.
- Each capacity: integer 1–3. Booleans are rejected as integers.
- Requirements: 1–6 nonblank strings, each at most 400 characters. Each consumes
  one token from exactly one unit.
- Pool title: 120 characters; purpose: 700 characters.
- Batch validity: 60–86,400 seconds; expiry is exclusive (`now >= expiry` fails).
- Each complete prompt: at most 24,000 characters and 65,000 UTF-8 bytes.
- Expected hashes: exactly 64 lowercase hexadecimal characters.
- Beneficiary: a nonzero `0x` EVM address, normalized to lowercase.

```json
[{"unit_id":"a","description":"One session covering CSV export and JSON import.","capacity":1},
 {"unit_id":"b","description":"One session covering CSV export only.","capacity":1}]
```

```json
["A session explaining CSV export.","A session explaining JSON import."]
```

## Local verification

From this directory:

```text
python -m unittest -v test_splitproof.py
```

**37 deterministic tests passed locally.** The test double supplies controlled
model outputs and storage; it is not GenVM execution or an LLM-accuracy benchmark.
Cases include greedy-trap matching, capacities above one, essential versus
irrelevant uncertainty, joint conflict, full-receipt tampering, cross-batch CAS,
snapshot-hash protection independent of epoch, authorization, expiry, finality,
complete maximum-size Unicode/escaped prompts, failed-write atomicity and the
real clock helper with a guard against reads inside model callbacks.

The source is self-contained for GenLayer Studio. Its runner pin was used by the
previously deployed November 1 contracts; that prior result is not proof that a
new contract or host call works. See [STUDIO-TEST.md](STUDIO-TEST.md) for the
reproducible network walkthrough, [SUBMISSION-PACK.md](SUBMISSION-PACK.md) for the
Portal text and [DEPLOYMENT.md](DEPLOYMENT.md) for observed release evidence.
