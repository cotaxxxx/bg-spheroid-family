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

## Verified pins

No pins have yet been promoted in this repository.

## Candidate / pending references

Upstream prolate and oblate research histories exist, but their binding evidence locations and current immutable states must be verified before promotion here.

Do not infer certification from this section.

## Promotion rule

A reference moves from pending to verified only when all of the following hold:

1. the exact upstream repository and full Git commit are resolved;
2. the evidence manifest exists at that commit;
3. its SHA-256 identity is recorded;
4. the upstream certificate status is read from the pinned evidence;
5. the manuscript claim is no stronger than the upstream certified statement.

This repository remains `NOT_BINDING` regardless of how many upstream pins are verified.
