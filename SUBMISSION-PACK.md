# SplitProof Portal submission package

Release authorized 2026-11-03. The matching deployment, successful two-stage
assessment and separate allocation are recorded in [DEPLOYMENT.md](DEPLOYMENT.md).

Category: **Builder → Intelligent Contracts**

## Title

SplitProof: Capacity-Constrained Evidence Allocation with Consensus-Gated Consumption

## Notes / Description

SplitProof allocates a fixed pool of declared evidence units without overspending their agreed capacities. An owner locks complete unit descriptions and token limits; each batch freezes requirements, beneficiary, expiry and the full remaining-capacity snapshot. Independent GenLayer validators assess every requirement-unit cell. Deterministic backtracking finds a complete capacity-respecting matching, then a second full-source assessment checks that exact allocation for joint contradictions. Essential uncertainty blocks authorization. READY alone consumes nothing: the beneficiary must commit the exact receipt under an epoch and full-snapshot compare-and-swap. Concurrent batches cannot spend the same pool's capacity. Validators bind every persisted receipt field, including both complete prompt budgets and hashes. It holds no funds and does not prove external authenticity or global originality. Includes adversarial tests and a reproducible Studio walkthrough.

## Formal evidence — fill only after release

| Evidence type | Status |
| --- | --- |
| GitHub Repository | https://github.com/zakazaka95/SplitProof |
| GitHub File | https://github.com/zakazaka95/SplitProof/blob/main/SplitProof.py |
| GenLayer Explorer Contract | https://explorer-studio-next.genlayer.com/address/0x46eb745bDF73565dE0C54301EF529dd63d568Df5 |
| Other | https://explorer-studio-next.genlayer.com/tx/0x3f81bdb5376474f2f563f215ac63a90d8c553f9ba3af51a218476505846cfe3a — FINALIZED; stored batch `0` is `READY` |

Local checks: 37 deterministic tests passed with controlled model outputs.
Deployment and actual live outcomes are tracked separately in [DEPLOYMENT.md](DEPLOYMENT.md).
Do not represent local checks as network or model-accuracy evidence.
When attaching GitHub File evidence, prefer the same source file at its actual
immutable GitHub commit after publication. The raw deployed-source fingerprint
is fixed in the deployment record; the commit link must come from GitHub.
