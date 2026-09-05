# Upstream Evidence Pins

Status: **NOT_BINDING registry**

This file is the sole manuscript-level registry for immutable upstream evidence references used by `bg-spheroid-family`.

## Rules

A pin may be promoted into the verified table only after the referenced upstream state has been checked directly.

Required fields:

| Field | Requirement |
|---|---|
| Regime | prolate / sphere / oblate |
| Repository | exact `owner/repository` |
| Git commit | full 40-character SHA |
| Evidence manifest | exact path |
| Manifest SHA-256 | full 64-hex digest |
| Upstream status | exact certification status |
| Verification note | what was independently checked |

A branch name, tag without resolved commit, short SHA, manuscript prose, or value copied into this repository is not a binding pin.

For retention auditing, a pinned commit need not be an ancestor of the upstream default branch. A historical or implementation-line commit may be retained by any named ref. Named-ref reachability is a preservation check only: it does not replace full-SHA identity, manifest SHA-256 verification, or direct reading of the upstream status.

## Verified pins

No pins have yet been promoted in this repository.

## Candidate / pending references

Upstream prolate and oblate research histories exist, but their binding evidence locations and current immutable states must be verified before promotion here.

Do not infer certification from this section.

## Oblate named-ref retention audit — not promoted

Repository: `cotaxxxx/bg-oblate-spheroid`  
Former repository name: `cotaxxxx/Oblate-Spheroid-Research`  
Retaining named ref checked: `implementation/gt-boundary-two-chart`  
Ref tip at this audit: `c0449a341cb1e67942ed1f080626cb758d857c7b`

Each commit below was resolved from the supplied short prefix to a full 40-character SHA and independently checked to be an ancestor of the named ref above. This table establishes retention/reachability only. It does **not** promote any row into `Verified pins` and does not change the status recorded by the upstream artifact.

| Prefix | Full commit SHA | Upstream role / artifact at that commit | Status read from upstream artifact |
|---|---|---|---|
| `a439fe7c` | `a439fe7cb983ac89134b2d03d253a0d6e89d5f74` | gt-boundary external Judge request / symbolic-audit submission | `SUBMITTED_FOR_JUDGE / NOT_BINDING` |
| `3e2dfb04` | `3e2dfb04293d7a5c92fcd3ed164b164fe33115a6` | lower slab + `31/32` edge machine receipt | `MACHINE_GATING_PASS / NOT_AUDITED / NOT_BINDING` |
| `d0c36a9f` | `d0c36a9f379c3ad77f941a0e786b70e364be0f16` | lower slab + `31/32` edge Judge request | `EXTERNAL_JUDGE_REQUESTED / NOT_BINDING` |
| `a078ec5a` | `a078ec5ac74379ca95609ecaf9511a5c96169185` | local-entry Judge-receipt template lineage; adds unconditional quantitative boundary convergence | template/update commit; no independent promotion inferred here |
| `e56b751f` | `e56b751fe3864eb6e9ba3e2249608ae05217d11f` | contract A / center-axis coefficient Judge receipt | `JUDGE_PASS / CERTIFIED_WITHIN_SCOPE` |
| `0af9d6e1` | `0af9d6e11117c9183951eaf60506682b1de6f608` | contract B / center-pitchfork machine receipt | `AUDITED_SOURCE / CHAT_RAW_AUDIT_PASS / MACHINE_GATING_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING` |
| `a30f640d` | `a30f640d7f6441ba1a424d6e6c0825d9f730dcd9` | contract B external Judge request | `EXTERNAL_JUDGE_PENDING / NOT_BINDING` |
| `a2590b4c` | `a2590b4c7ae426b382782f67e9c4428e64ae43bf` | C0 machine receipt + Judge request | machine: `CHAT_RAW_AUDIT_PASS / MACHINE_GATING_PASS / EXTERNAL_JUDGE_PENDING / NOT_BINDING`; Judge request pending |
| `7f34c95d` | `7f34c95d15199bd82f738b393911354744a126f8` | C1a machine receipt | `MACHINE_PASS / C1A_CLOSED / NOT_EXTERNAL_JUDGE_BINDING` |
| `49cdcbb6` | `49cdcbb6c0ed77f6471926aaa990d598ad3cae25` | C1c Judge receipt | `MACHINE_GATING_PASS / JUDGE_PASS / ASSEMBLY_PENDING_C1B / NOT_BINDING` |
| `189ccc6d` | `189ccc6dc93e5e3b980d1d6a2d1a2c9b4534c5b4` | C1b `B_ob` bridge machine receipt | `MACHINE_PASS / C1B_SUBGATE_ONLY / FULL_C1B_NOT_YET_CLOSED` |

### Local-entry nested identifiers still pending

The supplied identifiers `aa6a1a17` and `7cb9b809`, described as lemma pins associated with the local-entry lineage, did not resolve as Git commit prefixes in the repository during this audit. They may be blob/object identifiers or may require a different exact provenance path. They are therefore **not recorded as verified commit pins** here. Their object type, full identity, path, and relation to the local-entry receipt must be resolved before any promotion depending on them.

### Retention note

The branch ref is mutable and can in principle be force-pushed or deleted. The full commit SHAs above are the immutable identities used for audit records; the named ref is recorded only to establish current retention. Before manuscript freeze or promotion, named-ref reachability should be rechecked together with the required manifest and SHA-256 validation.

## Promotion rule

A reference moves from pending to verified only when all of the following hold:

1. the exact upstream repository and full Git commit are resolved;
2. the evidence manifest exists at that commit;
3. its SHA-256 identity is recorded;
4. the upstream certificate status is read from the pinned evidence;
5. the manuscript claim is no stronger than the upstream certified statement.

This repository remains `NOT_BINDING` regardless of how many upstream pins are verified.
