# CERBERUS v3.4

## The Fourth Guarantee: Independence as a Runtime Quantity

**Emily Echterhoff**  
Working release candidate - research architecture, not flight-certified software

> Intelligence is not safety. Layering is not independence. Independence is not permanent.

## Abstract

CERBERUS is a three-layer runtime-assurance architecture for autonomous systems. An adaptive **Pilot** proposes actions but never holds direct execution authority; a deterministic **Watchdog** checks proposals against physics invariants and certified envelopes; and a minimal **Anchor** preserves a mission-survivable floor. A non-authoritative **Vigil** estimates whether the layers remain failure-mode independent over mission life.

The central claim is that inter-layer independence should not be treated as a permanent design-time fact. It is a perishable runtime quantity that can decay through aging, maintenance, shared environmental stress, software convergence, compromised ground commands, or newly discovered common-cause pathways. CERBERUS therefore models independence, monitors it, adversarially challenges it, budgets authority against its pessimistic estimate, and restores authority only through fresh evidence.

Version 3.4 makes passive conditioned-residual monitoring the baseline Vigil mechanism. Sentinel injection is retained only as an optional diagnostic extension, disabled by default and excluded from safety-case credit until independently validated. It also clarifies the probabilistic FCOI denominator and reframes the synthetic result as matched-model pipeline verification rather than operational detector validation.

## 1. Architecture

### Pilot

The Pilot performs adaptive reasoning, planning, and hypothesis generation. It may inspect Watchdog constraints and pre-shape proposals, but it cannot execute commands or relax constraints.

### Watchdog

The Watchdog is a deterministic gate. It evaluates proposals against physics invariants, hard envelopes, certified rules, and required cross-channel agreement. Its value is not greater intelligence; its value is failing for different reasons than the Pilot.

### Anchor

The Anchor enforces the minimum mission-survivable action set: power-positive attitude, thermal survival, bounded orientation control, authenticated communications, and an evidence-gated route to recovery. Anchor invariants are not overridable by Pilot, Watchdog, Vigil, or ground command.

### Vigil

The Vigil is an evidence layer with no command authority. Its load-bearing baseline is passive, conditioned, baseline-referenced residual monitoring with explicit uncertainty intervals. Vigil evidence may reduce authority but cannot promote it by itself.

## 2. Failure-Cause Overlap Index

For failure class `k`, let `M[i,k]` be the family of minimal cut sets sufficient to defeat layer `i` with respect to its stated safety function.

### 2.1 Structural FCOI

For layers `i` and `j`:

```text
FCOI_S(i,j,k) = |M[i,k] ∩ M[j,k]| / |M[i,k] ∪ M[j,k]|
```

The structural form ranges from 0 to 1 when estimable. It is a property of the causal model, not a claim of ground truth. When both cut-set families are empty, the result is **not estimable**, not zero. Exact-match Jaccard can understate similarity when two cut sets share nearly all root causes but differ by one event; therefore it is a screening instrument and must be accompanied by a near-match census or weighted-incidence refinement.

### 2.2 Probabilistic FCOI

Let `F[i,k]` denote failure of layer `i` in class `k` during exposure interval `T`, and let `G[i,j,k]` denote the event that both failures propagate through at least one shared modeled root cause. Then:

```text
FCOI_P(i,j,k,T) = P(F[i,k] ∩ F[j,k] ∩ G[i,j,k] | evidence_T)
                  ------------------------------------------------
                  P(F[i,k] ∪ F[j,k] | evidence_T)
```

This is equivalently the probability of shared-root joint failure **conditioned on at least one layer failing**. The union denominator is intentional: the ratio measures the share of total pair failure exposure attributable to shared-root joint failure.

It is **not** a reliability-invariant dependence coefficient. Changes in `P(F[i,k])` or `P(F[j,k])` can move the denominator even when the shared-cause numerator is unchanged. Every operational report must therefore publish:

- `P(F[i,k])`;
- `P(F[j,k])`;
- the shared-root joint-failure numerator;
- the union denominator;
- the resulting FCOI ratio and uncertainty interval.

### 2.3 Conservative runtime value

For budgeting, CERBERUS uses the upper defensible bound:

```text
FCOI_bar(i,j,k,t) = upper_bound(FCOI_P(i,j,k,t))
```

Higher overlap means less independence, so using the lower bound would flatter the system.

### 2.4 Marginal-health promotion guard

A lower FCOI caused by worsening independent single-layer failure rates is not improving assurance. Authority promotion requires both:

1. improving or stable overlap evidence; and
2. non-worsening certified upper bounds on each layer's marginal failure probability.

Demotion may occur from either overlap deterioration or marginal-health deterioration. Promotion requires both dimensions to pass.

## 3. Independence budget

For each failure class `k`, design review establishes an acceptable overlap ceiling `theta[k]`.

```text
O[k,t] = max over all layer pairs and the three-layer estimate of FCOI_bar
m[k,t] = theta[k] - O[k,t]
b[k,t] = clip((theta[k] - O[k,t]) / (theta[k] - O[k,0]), 0, 1)
B[t]   = min over k of b[k,t]
```

`B=1` represents full certified design margin and `B=0` means at least one failure class has reached its certified overlap ceiling.

Authority is discretized:

- **A3** - full negotiated Pilot proposal envelope.
- **A2** - restricted proposal magnitudes and stronger consensus requirements.
- **A1** - Watchdog-directed operation; Pilot advisory only.
- **A0** - Anchor authority and minimum survivable action set.

Demotion is immediate and may skip levels. Promotion is sequential, rate-limited, requires a higher hysteresis threshold than demotion, requires continuous margin evidence for dwell time `tau`, and must pass the marginal-health promotion guard. Ground may veto promotion but is not required for demotion.

## 4. Common stimulus versus common cause

Channels exposed to the same sky, thermal cycle, or radiation environment will correlate. The Vigil therefore conditions on measured common environmental inputs and monitors drift from commissioning baselines rather than absolute correlation.

The current prototype uses linear environmental conditioning, rolling residual correlation, a one-sided Fisher upper confidence bound, and a persistence rule. Conditional transfer entropy remains a proposed research extension because it is data-hungry, estimator-sensitive, and vulnerable under non-stationary or degrading telemetry.

A passive alarm cannot always distinguish an unmodeled benign stimulus from harmful coupling. CERBERUS treats that ambiguity conservatively: reduce the independence budget, preserve the full evidence trace, and request diagnosis. Ambiguity cannot create permission.

## 5. Optional sentinel interrogation

Passive conditioned-residual monitoring is the baseline and load-bearing Vigil mechanism. It can reduce the independence budget without actively perturbing the vehicle and remains sufficient to declare evidence unknown or adverse.

A sentinel is an optional, bounded, statistically characterized perturbation intended to test whether a signal propagates into a channel declared independent. No channel is injectable by default; the default is **passive-only**.

A channel may be reclassified as injectable only after an independent, channel-specific hardware-in-the-loop safety case establishes:

- hardware amplitude and duration caps;
- mutual exclusion with maneuvers and safing;
- automatic removal and timeout behavior;
- state-estimation and actuation-deadband protection;
- detection-power and false-alarm evidence;
- zero unacceptable injection-attributable effects in accepted testing.

Sentinel injection receives no baseline safety-case credit, cannot increase the independence budget, cannot promote authority, and is not required for conservative demotion. Its failure or unavailability must never block the passive Vigil from declaring evidence insufficient.

## 6. Pilot red team and monotonicity ratchet

During idle mission phases, the Pilot may attack the correlation map in sandboxed shadow mode. It may propose missing shared pathways and test them against simulation or replayed telemetry.

The ratchet is one-directional: a discovered pathway may reduce claimed independence, tighten budgets, or narrow authority. Pilot output can never expand the safety claim or relax a constraint. The dog may find holes in the fence; it may never declare the fence sound.

## 7. Safety is not availability

Loss or inconsistency of the Vigil collapses the relevant independence budget contribution conservatively, but an A0 state must remain recoverable rather than mission-dead.

A0 maintains:

- power-positive attitude;
- thermal survival limits;
- authenticated command contact;
- a diagnostic beacon carrying Vigil state and the margin trace;
- bounded fault isolation;
- an expiring diagnostic-recovery window.

Ground recovery is not an override. An authenticated two-party directive may command diagnostics, re-baselining, and re-arming of the promotion law. Ground cannot write the budget, assign an authority level, bypass dwell evidence, or override Anchor hardware invariants. The authorization expires if fresh in-flight evidence is not produced.

## 8. Shared-ontology limitation

All model-based mechanisms inherit the causal ontology. A coupling mechanism absent from the graph can evade FCOI computation, conditioning, red-team search boundaries, and the stated survival map at once.

CERBERUS therefore proposes a future graph-external empirical witness: a separately implemented, model-light monitor using different representations and assumptions. It may only reduce confidence; it cannot certify independence or promote authority. This does not solve ontology incompleteness, but prevents the causal graph from being the sole judge of its own adequacy.

## 9. Matched-model pipeline verification experiment

The fixed-seed experiment is a pipeline-verification test. After conditioning two synthetic channels on a measured common environment, a deliberately injected latent shared pathway should increase residual dependence, a one-sided upper bound should move conservatively, and the illustrative authority state should contract monotonically.

> **Perfect separation is expected when the detector's model matches the data generator. The experiment tests pipeline correctness, reproducibility, and conservative-bound behavior under known ground truth - not detection difficulty.**

Supplied results:

- nominal sustained-alarm runs: **0/200**;
- coupling detections: **200/200**;
- median detection sample: **1061.5**;
- median lead before symptom: **238.5 samples**;
- 10th-90th percentile lead: **160.9-319.6 samples**.

The generator creates the same residual-coupling structure that the detector is designed to identify. The result therefore verifies the wiring of conditioning, threshold calibration, persistence logic, conservative-bound computation, fixed-seed reproducibility, and illustrative authority transitions. It is not an estimate of real-world false alarms, missed detections, lead time, flight performance, robustness to model mismatch, full probabilistic FCOI, transfer entropy, sentinel safety, or operational authority control.

The maintained implementation lives in [`cerberus-vigil-experiment`](https://github.com/k766807/cerberus-vigil-experiment).

## 10. Implementation boundary

### Implemented research artifacts

- browser Vigil Lab demonstrator;
- matched-model synthetic pipeline-verification experiment;
- Adversarial Casebook;
- Anchor Reference Specification;
- illustrative A3-A0 authority-state transitions.

### Specified but not implemented

- exact minimal-cut-set structural FCOI engine;
- operational probabilistic FCOI estimator;
- integrated Pilot shadow-mode red team;
- authenticated expiring ground-recovery command stack.

### Proposed or optional

- conditional transfer entropy extension;
- optional channel-specific sentinel interrogation;
- graph-external empirical witness;
- conservative three-layer reliability proof;
- flight and hardware-in-the-loop validation.

## 11. Novelty position

CERBERUS does not claim to invent Simplex runtime assurance, common-cause reliability modeling, dynamic watermarking, change-point detection, hysteresis, dwell-time switching, or fault-dependent autonomy restriction.

The candidate contribution is the composition of those foundations into a loop where measured inter-layer failure-mode independence is the controlled runtime resource. Novelty remains a hypothesis subject to continued primary-source and external expert review.

## Conclusion

CERBERUS treats the property on which layered assurance depends - failure-mode independence - as measurable, perishable, attackable, and budgetable. Authority is rented against pessimistic evidence for that independence; it is never owned.

Version 3.4 also makes the evidence hierarchy explicit: passive monitoring is baseline, active sentinel interrogation is optional, matched-model synthetic performance is plumbing evidence rather than validation, and improving overlap ratios cannot compensate for worsening marginal layer reliability.
