# Reproducible Studio walkthrough — SplitProof

The steps below describe expected checks. Actual executed cases and results are
recorded separately in [DEPLOYMENT.md](DEPLOYMENT.md); a procedure is not evidence
that it has passed. Use only synthetic records and transaction value 0 GEN. Network fees are separate.
Perform these checks in Normal / Full Consensus with simulation disabled.

Do not switch selected Studio contracts while a write displays **Sending...**.
Wait until the transaction has been submitted to the intended address. An
`ACCEPTED` transaction containing a GenVM error is not a successful method call.
Read the resulting contract state and record the actual outcome and transaction.

## 1. Source and deployment

Verify the current Studio runtime and dependency pin; schema-check this exact
`SplitProof.py`, then deploy with no constructor arguments. Require GenVM SUCCESS.
Compare the complete deployed Explorer Code view with the tracked source.
Read `get_stats()`: expect version `1.0.1`, schema `splitproof-v1`, all counts zero.
The first `open_pool` write exercises the timestamp adapter; schema loading and
constructor success alone do not establish that host-clock compatibility.
Record actual network, chain ID, source commit/hash, address and deployment tx.
Do not copy an address from another contract or invent a successful transaction.

## 2. Register a finite pool

Call `open_pool`:

```text
title: Synthetic mentoring allocation
purpose: Allocate declared session tokens to requested topics.
units_json:
[{"unit_id":"a","description":"One session covering CSV export and JSON import.","capacity":1},{"unit_id":"b","description":"One session covering CSV export only.","capacity":1}]
```

On a fresh deployment the returned `pool_id` should be `0`; use the actual return.
Read `get_pool(pool_id)` and `get_snapshot(pool_id)`. The initial epoch is `0`
and remaining capacity is `a:1, b:1`. Copy the **actual snapshot hash**.

## 3. Freeze the requirements and beneficiary

Call `open_batch` as the pool owner:

```text
pool_id: actual pool ID
expected_epoch: 0
expected_snapshot_hash: exact hash from get_snapshot
beneficiary: actual current Studio account address
requirements_json:
["A session explaining CSV export.","A session explaining JSON import."]
validity_seconds: 3600
```

Using the current account as beneficiary makes the baseline one-wallet flow
reproducible. A separate beneficiary account is useful for checking role guards.
Never enter a textual placeholder in an address field. Read `get_batch` and
confirm the exact full frozen request and beneficiary before assessment.

## 4. Assess, without consuming

Call `assess_batch(batch_id)`. A clear interpretation is:

| Requirement | Unit a | Unit b |
| --- | --- | --- |
| CSV export | ELIGIBLE | ELIGIBLE |
| JSON import | ELIGIBLE | INELIGIBLE |

The deterministic matching should therefore assign requirement `0` to `b` and
requirement `1` to `a`. A naive first-choice greedy plan would fail; the contract
backtracks. The whole-allocation assessment must independently confirm that this
exact plan is `COHERENT`, or the contract must not authorize it.

Read `get_batch` and `get_attempt(batch_id,1)`. For a successful positive example,
require `READY`, `allocation_allowed:true`, `semantic_complete:true`, both
`truncated:false` flags and the expected full assignment. Copy the actual
`receipt_hash`. Read the pool again: epoch and capacities must remain unchanged.

These are expected checks, not guaranteed live-model outputs. If the transaction
does not reach agreement, record that outcome. Do not call a leader return a
persisted accepted certificate. Do not use Leader Only mode to manufacture proof.

## 5. Consume the exact receipt

From the exact beneficiary account call:

```text
allocate(batch_id, exact receipt_hash)
```

Read `get_allocation`, `get_batch` and `get_pool`. Successful allocation records
the immutable assignment, receipt hash, beneficiary and before/after snapshot
hashes; the batch is `ALLOCATED`, pool epoch is `1`, and both capacities are zero.
The same receipt cannot be allocated again. Preserve the actual transaction and
stored record; do not infer these values merely from a local unit test.

## 6. Concurrent-batch stale-snapshot case

Create a **new pool** using the same synthetic units. Open two batches before
either allocation, each requiring `["A session explaining CSV export."]`, using
the same current epoch/snapshot and actual beneficiary. Assess both. If both
become `READY`, allocate the first. The second must fail as **stale** even if a
different unused token remains in the pool. That conservative serialization is
intentional: its whole semantic assessment covered an older complete snapshot.
Read state after failure and confirm no second allocation or partial capacity
decrement. A newly created batch at the new epoch may use remaining capacity.

## 7. Other useful checks

- Use an unauthorized account for opening, assessment, cancellation or consumption;
  ensure the documented role boundary is enforced.
- Try a wrong receipt hash, expiry exactly at `valid_until`, replay, cancellation
  or retirement. Confirm capacity remains unchanged after a rejected call.
- Essential uncertain cells without a certified complete matching must produce
  `INCONCLUSIVE`; an optimistic graph that still cannot match is `INSUFFICIENT`.
  Neither branch may issue an allocation or invoke the whole-allocation prompt.
- A source describing a single service slot that can run one of two incompatible
  services must never authorize a simultaneous requirement for both. The model
  might refuse at matrix or whole-plan stage; report the actual stored branch.
- A whole-plan `CONFLICT`/`UNCERTAIN` must not be replaced with another convenient
  assignment or a new verdict within the same immutable batch.

These optional cases are procedures only until actually run. Record separately
which were exercised locally, read-only on the network, or by actual write txs.

## Release evidence checklist

1. Publish this exact source, tests, README, walkthrough and license.
2. Attach the repository and immutable tracked source as formal Portal evidence.
3. Attach the exact matching Explorer **address** URL, not only a transaction URL.
4. Include a successful actual assessment and allocation transaction in the
   deployment record, with any failed/undetermined attempts described accurately.
5. Select the actual contribution date and correct weekly slot after the reset.
6. Keep expected procedures separate from the deployment record's observed outcomes.
