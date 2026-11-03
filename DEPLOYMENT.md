# SplitProof deployment record

Release authorized **2026-11-03**. The source-matched version `1.0.1` deployment
and observed demonstration progress are recorded below.

## Current release evidence

| Item | Observed record |
| --- | --- |
| Source version / receipt schema | `1.0.1` / `splitproof-v1` |
| Exact local source SHA-256 | `6f86b3ed8002b6ced7b3cad680c35c96609803b660c742c15592129a42240f7b` |
| Local/Explorer normalized source SHA-256 | MATCH: `39eb3aa4ad74f146d2c84fd3c8890eb2ca653c7958d76ab5185219b37d5039e3` |
| Runtime dependency | `py-genlayer:babwp9t37jw9g4j2bccgn14g6x7x9s1f7dsmh7emvz735pz4zxa0` |
| Local deterministic tests | 37 passed using controlled model/storage doubles |
| Public repository | https://github.com/zakazaka95/SplitProof |
| Tracked source file | [SplitProof.py](https://github.com/zakazaka95/SplitProof/blob/main/SplitProof.py), bound by the raw source fingerprint above |
| Deployed Explorer contract | [0x46eb745bDF73565dE0C54301EF529dd63d568Df5](https://explorer-studio-next.genlayer.com/address/0x46eb745bDF73565dE0C54301EF529dd63d568Df5) |
| Deployment transaction | [0x721f3f726ccc6ff4519a3e350742ef280273d5aa6cb93960bc275d53b33ac2cf](https://explorer-studio-next.genlayer.com/tx/0x721f3f726ccc6ff4519a3e350742ef280273d5aa6cb93960bc275d53b33ac2cf) |
| Deployment result | FINALIZED; Explorer constructor execution SUCCESS |
| Complete Explorer Code comparison | MATCH with local version `1.0.1` after the normalization below |
| First timestamp-using write | `open_pool` FINALIZED; pool `0` persisted with expected initial capacity |
| Live semantic assessment / stored receipt | FINALIZED; batch `0` stored `READY` with the complete coherent allocation |
| Live allocation / persisted capacity change | FINALIZED; pool `0` epoch `1`, allocation count `1`, both capacities zero |

All writes use synthetic records and transaction value 0 GEN; devnet network fees
are separate. Local tests are not network or semantic-model accuracy evidence.

## Runtime clock adapter

Version `1.0.1` uses `datetime.now(timezone.utc).timestamp()` only in deterministic
public methods. Model receipt reconstruction never reads time. This replaces the
newer SDK `GetTimestamp` operation after it failed with `SystemError 2: inval`
during the initial IntentMutex live write on the observed Studio host. The same
WASI datetime path had already been exercised by November 1 DeltaPermit. Local
executor source inspection explains the adapter choice; it does not establish
that a live host is byte-identical to the local checkout. SplitProof's own
successful deployment and first timestamp-using write are recorded here. The
allocation logic and receipt schema remain unchanged.

## Observed demonstration progress

The synthetic units and requirements follow [STUDIO-TEST.md](STUDIO-TEST.md).
The first `open_pool` transaction,
[0x76a8f3b5e9f689bf51dd2ed44181b3a780c47cea5d4e3bfbbac41a1470a917d8](https://explorer-studio-next.genlayer.com/tx/0x76a8f3b5e9f689bf51dd2ed44181b3a780c47cea5d4e3bfbbac41a1470a917d8),
was observed FINALIZED. `get_snapshot(0)` succeeded with epoch `0`, remaining
capacity `a: 1, b: 1`, pool hash
`7a0b99d31c9878d95e6e2c6905352148edb02d848519bec98bb31386fdf18252`
and snapshot hash
`acf17c111473c067daee771397ce56dc85ca7aa87247dd0064cb8d1c2502fcd4`.

The `open_batch` transaction,
[0x5e57590a3646bb283fe49c1da31f475b52915212018a7a439425b4ddf7e30805](https://explorer-studio-next.genlayer.com/tx/0x5e57590a3646bb283fe49c1da31f475b52915212018a7a439425b4ddf7e30805),
was observed ACCEPTED for batch `0`, with beneficiary
`0x3996827f07D3CE7b32cECDf974a0c63fda912Fa2`.

The `assess_batch(0)` transaction,
[0x3f81bdb5376474f2f563f215ac63a90d8c553f9ba3af51a218476505846cfe3a](https://explorer-studio-next.genlayer.com/tx/0x3f81bdb5376474f2f563f215ac63a90d8c553f9ba3af51a218476505846cfe3a),
was observed FINALIZED. `get_batch(0)` returned stored status `READY`, attempts
`1` and `allocation_id: -1` before consumption. The complete matrix was:

| Requirement | Unit a | Unit b |
| --- | --- | --- |
| `0`: CSV export | `ELIGIBLE` | `ELIGIBLE` |
| `1`: JSON import | `ELIGIBLE` | `INELIGIBLE` |

The exact deterministic assignment was requirement `0` to `b`, requirement `1`
to `a`, with `used_tokens: {a: 1, b: 1}`. The stored whole-allocation result was
`COHERENT`, `allocation_allowed: true`, `semantic_complete: true` and
`uncertainty_blocks: false`. Both prompt truncation flags were false. The matrix
prompt had `2563` characters / UTF-8 bytes, and the whole prompt had `2662`.

| Stored field | Observed value |
| --- | --- |
| Receipt hash | `7d18e7a9146b95efeb05ec1d97145423ca75ba076ae8a77525db9dc5edc7c6a1` |
| Exact allocation hash | `63c7b71de2c6a6db8788fb1aa459581eec0cc1f65b985f1429f474afb4ade150` |

This records the live assessment and greedy-trap resolution for the supplied
synthetic fixture. Separate `allocate(0, receipt_hash)` transaction
[0x1a2ff960abd2e245021dbb371fecbc1f93bd85aa9787bf8dbb4943bb7fa27055](https://explorer-studio-next.genlayer.com/tx/0x1a2ff960abd2e245021dbb371fecbc1f93bd85aa9787bf8dbb4943bb7fa27055)
was observed FINALIZED. `get_pool(0)` returned epoch `1`, allocation count `1` and
remaining capacity `a: 0, b: 0`. `get_allocation(0)` preserved the exact assignment
of requirement `0` to `b` and requirement `1` to `a`, the same validated receipt
hash, and `created_at: 1793743915`.

| Stored consumption field | Observed value |
| --- | --- |
| Before epoch / snapshot | `0` / `acf17c111473c067daee771397ce56dc85ca7aa87247dd0064cb8d1c2502fcd4` |
| After epoch / snapshot | `1` / `63367e37a174e63403adae4ff2ec5e0a47626b4420b84ee775f079f8909ad46f` |
| Immutable allocation record hash | `9308be65c3b16c5a65f2ea4f91e043b8b9cc68c95482c4e83f8035321fcecdbe` |

The concurrent-batch stale case, rejected allocation, expiry, retirement and
semantic-negative cases in the walkthrough were not run onchain for this record.
Their controlled-output unit coverage is separate from this successful live
positive path. These observations concern the supplied synthetic fixture and do
not establish general semantic-model accuracy. Portal review and awarded points
are not claimed by this deployment record.

## Source comparison

The raw fingerprint above is the exact local file-byte SHA-256. The complete
Explorer Code-view text and local source matched after replacing CRLF with LF
and trimming leading/trailing whitespace, preserving internal whitespace. The
distinct normalized fingerprint is recorded above; this rendering comparison
does not claim raw file-byte equality.

Record actual IDs, transaction status, GenVM result and stored-state reads for
every exercised case. Retain failed or undetermined attempts honestly. A leader
output alone is not a stored consensus receipt, and an accepted transaction can
still contain a GenVM error.
