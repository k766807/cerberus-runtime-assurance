# CERBERUS Vigil Synthetic Independence-Decay Experiment

This reproducible experiment supports one narrow claim in CERBERUS v3.3: a monitor that conditions out a measured common environment can detect an emerging latent shared pathway before a predefined behavioral-symptom time, and a conservative upper bound on residual dependence can drive authority demotion.

## Run

```bash
python run_experiment.py
```

Python dependencies: `numpy`, `matplotlib`.

The script uses fixed seeds and writes all outputs to `results/`. The repository workflow `.github/workflows/reproduce-vigil.yml` runs the experiment in a clean Python environment and compares the headline metrics with the committed summary.

## Model

Two synthetic channels observe the same measured environment. During commissioning, the environment-to-channel response is estimated. After sample 700, a hidden latent process is gradually injected into both channels; the gain reaches its maximum at sample 1300. The monitor computes rolling residual correlation after removing the measured environment, then converts the magnitude to a one-sided 95% Fisher upper confidence bound.

The alarm threshold is not hand-picked from the representative trace. It is calibrated as the 95th percentile of the maximum upper bound observed across 100 independent nominal runs. Evaluation then uses separate ensembles of 200 nominal and 200 coupling runs. An alarm requires ten consecutive samples above threshold.

## Results

With the included configuration and seeds:

- Nominal run false-alarm rate: **0/200**
- Coupling-run detection rate: **200/200**
- Median detection sample: **1061.5**
- Median lead before the chosen behavioral-symptom time: **238.5 samples**
- 10th–90th percentile lead: **160.9–319.6 samples**
- Representative authority path: **A3 at commissioning, A2 at sample 799, A1 at 1139, A0 at 1197**

## Scope boundary

This is an explanatory synthetic experiment. It does not validate transfer entropy, sentinel injection safety, spacecraft FDIR performance, FCOI probability calibration, or flight-certified authority logic. Those remain proposed or open work in the v3.3 status table.
