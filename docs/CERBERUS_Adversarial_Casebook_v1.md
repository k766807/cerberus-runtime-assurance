# CERBERUS Adversarial Casebook v1

**Status:** red-team research artifact  
**Purpose:** force CERBERUS to state how it fails, what evidence should appear, how authority should contract, and where survivability ends.

## Case format

Each case is traced through:

```text
root cause → propagation path → minimal cut set → FCOI effect → Vigil evidence
→ authority trajectory → survivability → test injection → acceptance criterion → residual risk
```

## Scenario index

| ID | Scenario | Principal assurance question | Expected minimum response |
|---|---|---|---|
| AC-01 | Shared estimator corruption | Can Pilot and Watchdog share a false state while appearing independent? | Detect cross-layer residual dependence or admit ontology blind spot; demote |
| AC-02 | Degrading shared power rail | Does one physical rail couple supposedly diverse sensors? | Raise probabilistic FCOI; enter A0-POWER if margin collapses |
| AC-03 | Benign common stimulus | Can Vigil avoid treating a shared sky or eclipse cycle as a defect? | Condition on measured environment; no sustained alarm |
| AC-04 | Unmodeled benign stimulus | What happens when passive evidence cannot distinguish benign from harmful coupling? | Conservative budget reduction; queue diagnosis |
| AC-05 | Vigil persistent unknown | Can a broken meter park the vehicle forever? | A0-COMMS, explicit meter-health flag, bounded recovery path |
| AC-06 | Fabricated good news | Can Vigil failure understate overlap? | Independent self-check; survival-boundary declaration; no promotion |
| AC-07 | Unsafe sentinel injection | Can the test instrument disturb the controlled system? | Hardware amplitude cap, automatic removal, passive-only fallback |
| AC-08 | Sentinel leakage | Does a watermark appear in a channel declared independent? | Treat as direct evidence against independence; immediate budget reduction |
| AC-09 | Pilot hallucinated correlation | Can shadow red-teaming create denial of availability? | Ratchet may tighten only; ground review required; track availability cost |
| AC-10 | Pilot misses real correlation | Can the red team fail silently? | Vigil and graph-external witness remain independent discovery paths |
| AC-11 | Compromised ground recovery | Can ground dissolve the assurance mechanism? | Two-party authenticated expiring window; no direct promotion or budget write |
| AC-12 | Stale ground picture | Can a valid but obsolete command reopen the wrong path? | Anti-replay, freshness checks, in-flight evidence still required |
| AC-13 | Shared software maintenance | Does an update introduce a common library across layers? | Correlation map update; structural FCOI rise; authority re-certification |
| AC-14 | Clock or timestamp corruption | Can asynchronous evidence fabricate or hide dependence? | Timebase health flag; fail-conservative evidence status; A0-COMMS if unresolved |
| AC-15 | Telemetry dropout | Can missing samples flatter the estimator? | Unknown is not zero; widen interval; reduce budget |
| AC-16 | Hidden Anchor aperture | Do all layers depend on one physical sensor aperture or harness? | Survival-boundary update; redesign or explicitly accept uncovered class |
| AC-17 | Actuator common-mode loss | Can all reasoning remain correct while the physical effector set disappears? | A0-CONTAIN; preserve power, thermal, contact if physically possible |
| AC-18 | Shared false ontology | Can every assurance mechanism miss a cause absent from the causal model? | Graph-external witness proposal; explicit epistemic boundary; no total-safety claim |

## Worked cases

### AC-01 — Shared estimator corruption

**Root cause:** Pilot and Watchdog consume state estimates derived from a shared navigation library or shared corrupted sensor fusion product.

**Propagation:** common estimator → Pilot proposal and Watchdog invariant evaluation → both accept an unsafe trajectory.

**Minimal cut set:** `{shared estimator corruption, no independent raw-physics check}`.

**FCOI effect:** high overlap for navigation-loss and unsafe-guidance classes. Structural FCOI should expose the shared estimator node; probabilistic FCOI increases as estimator confidence degrades.

**Vigil evidence:** proposal residuals and Watchdog acceptance decisions drift together after conditioning on measured environment. A graph-external monitor using raw geometric consistency may disagree.

**Authority:** A3 → A1 or A0 depending on consequence severity and upper-bound overlap.

**Acceptance criterion:** an injected estimator bias must not be accepted simultaneously by Pilot and Watchdog without either a deterministic raw-physics trip or an independence alarm.

**Residual risk:** an estimator defect that also corrupts every supposedly independent physical check remains outside the protected boundary.

### AC-03 — Benign common stimulus

**Root cause:** two channels observe the same eclipse cycle or solar-flux change.

**Propagation:** environment → both channels, without a new shared internal pathway.

**FCOI effect:** none if the environment is explicitly modeled and does not create a shared failure mechanism.

**Vigil evidence:** high raw correlation, low conditioned residual correlation, no sustained baseline drift.

**Authority:** remain A3.

**Acceptance criterion:** nominal environmental sweeps must remain below the calibrated sustained-alarm threshold at the stated false-alarm rate.

**Residual risk:** an unmeasured benign stimulus can still be misclassified and cost availability.

### AC-05 — Vigil persistent unknown

**Root cause:** Vigil processor fault, inconsistent estimator state, missing environment inputs, or authenticated alarm-channel failure.

**Propagation:** meter health lost → independence estimate invalid.

**FCOI effect:** not assigned a favorable number. The budget collapses to its floor because independence is unknown.

**Authority:** immediate demotion to the appropriate conservative level, typically A0-COMMS.

**Availability response:** maintain power, thermal survival, authenticated beacon, and a scheduled contact posture. An expiring diagnostic window may be opened by ground, but promotion still requires fresh evidence and dwell.

**Acceptance criterion:** repeated unknown-state injection must not create silent permanent lockdown, unsafe autonomous restoration, or direct ground promotion.

### AC-07 — Unsafe sentinel injection

**Root cause:** sentinel amplitude, timing, or duration perturbs a safety-critical loop.

**Propagation:** test excitation → state-estimate error or actuator response → operational disturbance.

**Required controls:** hardware amplitude limit, maximum duration, maneuver and safing exclusion, watchdog removal, and precomputed deadband margin.

**Authority:** sentinel is aborted; channel is reclassified passive-only; any unexplained propagation reduces the independence budget.

**Acceptance criterion:** zero injection-attributable operational effects across closed-loop simulation and hardware-in-the-loop tests. A channel without a safe detectable amplitude is never injected.

### AC-09 — Pilot hallucinated correlation

**Root cause:** shadow-mode reasoner invents a plausible but false common-cause pathway.

**Propagation:** red-team finding → conservative map update request.

**Control:** monotonicity ratchet permits only constraint tightening. The Pilot cannot relax the map, promote itself, or write the operational FCOI directly.

**Authority:** may narrow pending validation; never expands.

**Acceptance criterion:** adversarial Pilot output must produce zero instances of constraint relaxation. Availability cost is measured explicitly.

### AC-11 — Compromised ground recovery

**Root cause:** stolen credentials, malicious insider, compromised mission-control host, or mistaken operator.

**Propagation:** apparently valid recovery directive attempts to bypass A0.

**Controls:** end-to-end authentication, anti-replay, two-party authorization, narrow command semantics, expiration, and immutable Anchor invariants.

**Authority:** ground may open diagnostics and re-arm the promotion law. It cannot set `B(t)`, select A1–A3, bypass dwell, or override hardware limits.

**Acceptance criterion:** compromise of one credential or one workstation must not directly increase vehicle authority.

### AC-14 — Clock corruption

**Root cause:** common timebase drift, timestamp rollover, delayed telemetry, or malicious time manipulation.

**Propagation:** misaligned channels → false dependence or hidden dependence → incorrect Vigil estimate.

**FCOI effect:** timebase becomes an explicit shared root cause. Estimate intervals widen while alignment is uncertain.

**Authority:** demote if the timing uncertainty crosses the certified evidence limit; enter A0-COMMS if no trustworthy reconstruction is possible.

**Acceptance criterion:** injected clock faults must be detected before the estimator can treat stale or misaligned samples as favorable independence evidence.

### AC-16 — Hidden Anchor aperture

**Root cause:** Pilot, Watchdog, and Anchor all rely on one physical aperture, harness, power converter, or environmental assumption.

**Propagation:** common physical loss defeats every layer despite software diversity.

**FCOI effect:** triple-overlap failure class approaches 1 once the shared dependency is modeled.

**Authority:** demotion cannot restore missing physical truth. The architecture must either redesign for dissimilar sensing or admit the failure class in the survival boundary.

**Acceptance criterion:** architecture review must enumerate physical apertures and harnesses, not only software dependencies.

### AC-18 — Shared false ontology

**Root cause:** the causal model lacks the concept required to represent an actual coupling mechanism.

**Propagation:** the same omission affects cut-set analysis, Vigil conditioning, red-team search space, and the stated survival map.

**Why this matters:** implementation diversity does not protect against a shared ontology.

**Response:** add a graph-external empirical witness built with different representations and assumptions. It may only reduce confidence; it cannot certify independence.

**Acceptance criterion:** the safety case must state that all FCOI values are conditional on the modeled ontology and must not present the index as ground truth.

## Verification use

Each scenario should become a machine-readable test record with:

- scenario identifier and version;
- causal-graph delta;
- injected signal or fault;
- expected Vigil evidence;
- expected authority transitions;
- timing bounds;
- safety and availability acceptance criteria;
- observed result;
- residual-risk disposition.

A scenario passes only when the observed trace satisfies the predeclared criterion. A persuasive narrative after the fact is not a test result.
