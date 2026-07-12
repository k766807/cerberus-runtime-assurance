# CERBERUS v3.5 arXiv source

This directory contains the submission-ready source for:

**CERBERUS: Runtime Independence Budgeting for Layered Assurance in Autonomous Systems**

## Build

```bash
latexmk -pdf -interaction=nonstopmode CERBERUS_v3.5_arXiv.tex
```

The manuscript uses only local text assets: the LaTeX source, section files, exact verified bibliography files, and a downsampled CSV plotted with PGFPlots.

## Evidence boundary

The paper is a research preprint, not flight-certified software, a completed safety case, or a claim of operational readiness. The fixed-seed experiment is explicitly framed as matched-model pipeline verification.

## arXiv routing

The intended primary category is **`eess.SY` — Systems and Control**. Use the same category in the repository README and the arXiv submission form. A robotics cross-list may be considered later only if the final submission emphasis supports it.

## Repositories

- Architecture and paper: https://github.com/emilyecht/cerberus-runtime-assurance
- Reproducible experiment: https://github.com/emilyecht/cerberus-vigil-experiment
