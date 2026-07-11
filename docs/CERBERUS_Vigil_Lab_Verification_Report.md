# CERBERUS Vigil Lab Verification Report

**Artifact:** `vigil-lab/index.html`  
**Status:** explanatory browser prototype  
**Not:** flight software, a completed safety case, or validation of operational FCOI

## 1. Purpose

The Vigil Lab makes the v3.3 control doctrine inspectable. It visualizes a conservative overlap proxy, the normalized independence budget, A3–A0 authority, Vigil health, immediate demotion, dwell-gated restoration, sentinel behavior, Pilot shadow red-teaming, and bounded ground recovery.

## 2. Implemented behaviors

- selectable synthetic failure scenarios;
- independent overlap proxies for sensor, software, and power classes;
- pessimistic upper-bound calculation;
- worst-class budget aggregation;
- immediate authority demotion, including skipped levels;
- sequential promotion with dwell time;
- fail-conservative Vigil fault behavior;
- sentinel campaign control;
- one-directional Pilot red-team update;
- authenticated-ground-recovery concept represented as an expiring diagnostic path;
- event trace and downloadable telemetry CSV.

## 3. Verification matrix

| ID | Property | Test action | Acceptance criterion | Prototype support |
|---|---|---|---|---|
| V-01 | Immediate demotion | Drive budget below one or more thresholds | Authority reaches the demanded lower level in the same update | Implemented |
| V-02 | No direct ground promotion | Fault Vigil, then request recovery | Recovery opens diagnostics; authority is not assigned | Implemented |
| V-03 | Sentinel boundedness | Run sentinel | Sentinel does not directly issue vehicle commands or promote authority | Implemented conceptually |
| V-04 | Monotonic red-team ratchet | Run Pilot red-team | Claimed overlap may rise; no constraint or authority is relaxed | Implemented |
| V-05 | Fail-conservative Vigil | Fault Vigil | Budget collapses and authority reaches A0 | Implemented |
| V-06 | Common-stimulus conditioning | Run benign common stimulus | Raw correlation may rise while conditioned residual remains near baseline | Implemented proxy |
| V-07 | Sequential promotion | Recover and hold healthy margin | Promotion occurs one level per completed dwell; no upward skip | Implemented |
| V-08 | Traceability | Run simulation and download CSV | Time, budget, authority, overlap proxy, and residual are recorded | Implemented |

## 4. Scenario expectations

### Radiation aging

A gradual sensor-coupling proxy rises after an initial healthy phase. The expected trajectory is A3 → A2 → A1 → A0 as the pessimistic bound consumes margin.

### Shared power rail

Power-class overlap rises more rapidly than nominal aging. The architecture should contract authority before the proxy reaches its certified ceiling.

### Common-library patch

Software-class overlap rises after the simulated patch point. The scenario represents the loss of diversity caused by maintenance convergence.

### Benign common stimulus

Raw correlation oscillates while conditioned residual dependence remains near baseline. The vehicle should remain at A3 unless uncertainty alone consumes margin.

### Spoofed navigation input

Sensor overlap rises and a sentinel campaign may expose prohibited cross-channel propagation.

## 5. Reproducibility

The browser prototype is deterministic only at the level of its update equations and user actions; it is not the fixed-seed Monte Carlo experiment. The reproducible numerical result is maintained separately under `experiment/`.

## 6. Known limitations

- the plotted FCOI is a normalized explanatory proxy, not a calibrated probabilistic FCOI;
- thresholds are illustrative rather than mission-derived;
- the browser model does not implement minimal cut sets;
- no cryptographic command stack is present;
- sentinel safety is represented as policy, not hardware-in-the-loop evidence;
- promotion dwell is simplified;
- no spacecraft dynamics or flight software are modeled;
- the Vigil does not use transfer entropy;
- no graph-external empirical witness is implemented.

## 7. Correct interpretation

The lab demonstrates how CERBERUS decisions are intended to depend on evidence. It does not demonstrate that the evidence model is complete, that a detector will work on flight telemetry, or that any authority threshold is safe for a real vehicle.
