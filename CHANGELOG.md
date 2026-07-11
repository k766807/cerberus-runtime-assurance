# Changelog

## v3.3 — Release Candidate — 2026-07-11

### Corrected

- Fixed the revision label and summary attribution inherited from v3.2.
- Corrected the conservative uncertainty direction: authority budgeting uses the upper FCOI bound because higher overlap means lower independence.
- Corrected and hardened retained bibliographic metadata, including publication dates and official source links.
- Prevented ground recovery from writing the budget, assigning authority, bypassing Anchor invariants, or waiving fresh-evidence and dwell requirements.

### Formalized

- Structural exact-match FCOI and non-estimable cases.
- Probabilistic shared-cause FCOI and uncertainty intervals.
- Pairwise/triple class aggregation.
- Certified overlap ceilings, normalized class budgets, and global minimum budget.
- Immediate demotion, hysteretic evidence-gated promotion, dwell time, and promotion rate limits.

### Added

- Primary-source verification for 37 references.
- 18-claim novelty matrix and reviewer-safe claim language.
- Shared-ontology common-cause limitation.
- Graph-external empirical witness as proposed future work.
- Reproducible fixed-seed synthetic Vigil experiment and results.
- Explicit implementation-status boundary.
- GitHub-ready release structure and citation metadata.

### Narrowed

- Conditional transfer entropy moved from core implementation claim to proposed research extension.
- Sentinel injection retained as a constrained proposal pending a channel-specific hardware safety case.
- Novelty claims stated as targeted-review findings rather than absolute priority claims.
