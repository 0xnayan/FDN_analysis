# Multi-Scale Analysis of Ripple and Decay Behaviour in Sparse Feedback Delay Networks

**Nayanmoni Borah** — Independent DSP / Audio Research

---

## Overview

This repository contains the full implementation and analysis pipeline for an independent research project investigating how delay-spacing strategies influence **macro-scale decay smoothness**, **micro-level ripple behaviour**, and **residual correlation structures** in sparse, low-order Feedback Delay Networks (FDNs).

The work began as a simple reverberation experiment in SuperCollider and evolved into a rigorous multi-scale signal analysis study after a non-intuitive result emerged early in the research: *configurations that appeared smoother globally sometimes produced stronger micro-level ripple structures.* This paradox motivated a dedicated pipeline capable of separating and independently quantifying macro and micro decay behaviour.

---

## Research Question

> How do different delay-spacing strategies influence macro-scale decay smoothness and micro-scale ripple behaviour in sparse, low-order Feedback Delay Network systems?

---

## Key Finding

> **Improving global decay smoothness does not necessarily improve local ripple smoothness — and in sparse FDNs, these two objectives may actively conflict.**

Specifically:

- The **optimized** configuration produced the smoothest global EDC slope yet exhibited among the highest derivative energy and residual variance at the micro level.
- The **irregular** configuration achieved the best decorrelation and lowest residual variance despite not having the smoothest global decay.
- **Quasi-uniform** spacing introduced long-range correlation locking — persistent coherent residual structures across thousands of samples.
- **Golden-ratio** spacing reduced direct periodicity but introduced sparse, persistent autocorrelation peaks in sparse networks.
- **Decorrelation**, **ripple smoothness**, and **decay stability** are distinct, potentially competing objectives — none of the tested configurations optimised all three simultaneously.

---

## Delay Configurations Studied

| Configuration | Description |
|---|---|
| Uniform | Equal delay spacing — maximally periodic, strong comb artefacts |
| Irregular | Linearly increasing spacing — best decorrelation, lowest residual variance |
| Optimized | Manually clustered — smoothest global EDC, paradoxically high micro ripple |
| Quasi-uniform | Uniform + controlled perturbation — long-range correlation locking |
| Golden-ratio | Irrational spacing via φ ≈ 1.618 — reduced direct periodicity, sparse coherent structures |

---

## Repository Structure

```
FDN_analysis/
│
├── README.md
├── LICENSE
│
├── rippleSmoothness.py          # Primary multi-metric ripple analysis pipeline
├── autocorrelationStudy.py      # Residual autocorrelation and periodicity metrics
├── energyDecayCompare.py        # Energy Decay Curve (EDC) comparison across configs
├── improveDelay.py              # Early-reflection and zoomed EDC analysis
│
├── supercolliderSoundSynthesis/ # SuperCollider FDN synthesis patches (.scd)
├── autocorrelation/             # Autocorrelation output plots
├── energyDecay/                 # EDC output plots
└── plotsOfRippleSmoothness/     # Ripple residual and metric output plots
```

---

## Analysis Pipeline

Each audio file goes through the following stages:

```
WAV File
    │
    ▼
Load & Normalise
    │
    ▼
Hilbert Transform → Instantaneous Amplitude Envelope
    │
    ▼
Peak Alignment (trim pre-impulse samples)
    │
    ▼
Adaptive Savitzky-Golay Smoothing
    │
    ▼
dB Conversion & Peak Normalisation
    │
    ▼
Decay Region Isolation  (−5 dB to −60 dB window)
    │
    ▼
Linear Trend Removal (OLS fit in dB domain)
    │
    ▼
Residual Extraction  ←── micro-level ripple signal
    │
    ├──▶ Variance
    ├──▶ MAD (Mean Absolute Deviation)
    ├──▶ Derivative Energy
    ├──▶ FFT High-Frequency Ripple Ratio
    └──▶ Autocorrelation Analysis
```

---

## Ripple Metrics

| Metric | What It Measures |
|---|---|
| **Variance** | Global deviation of the residual — aggregate ripple energy |
| **MAD** | Mean absolute deviation — typical ripple magnitude, robust to outliers |
| **Derivative Energy** | Average squared first-difference — local fluctuation roughness |
| **FFT Ripple Ratio** | Fraction of residual energy in the upper 30% of the spectrum — high-frequency micro-structure |

Relative change vs. the uniform baseline is reported as a percentage for each metric.

---

## Autocorrelation Metrics

| Metric | What It Measures |
|---|---|
| **Peak Periodicity** | Maximum ACF value at lag > 0 — strength of any recurrent structure |
| **Mean Correlation** | Mean absolute ACF — overall persistence of residual coherence |

A rapidly decaying ACF indicates a well-decorrelated, noise-like residual. Persistent off-zero peaks indicate rhythmic or quasi-periodic structure in the ripple.

---

## Tools & Dependencies

### Audio Synthesis
- [SuperCollider](https://supercollider.github.io/) — FDN synthesis, impulse response capture

### Python Analysis
```
numpy
scipy
matplotlib
librosa
```

Install dependencies:
```bash
pip install numpy scipy matplotlib librosa
```

---

## Scripts

### `rippleSmoothness.py`
The primary analysis script. For each delay configuration, it extracts the Hilbert envelope, isolates the decay region, removes the linear trend, and computes all four ripple metrics. Produces three plots: decay comparison, residual comparison, and signal-vs-trend overlay.

```bash
python rippleSmoothness.py
```

### `autocorrelationStudy.py`
Extracts the residual ripple signal for each configuration (using the same pipeline as `rippleSmoothness.py`) and computes the normalised autocorrelation up to 5000 lags. Reports peak periodicity and mean correlation, and plots the ACF comparison.

```bash
python autocorrelationStudy.py
```

### `energyDecayCompare.py`
Computes and plots the Schroeder EDC (backwards-integrated squared IR) for each recording on a common dB axis, aligned at the impulse peak.

```bash
python energyDecayCompare.py
```

### `improveDelay.py`
Compares the full EDC alongside a zoomed early-reflection view (first 0.5 s) for the uniform, irregular, and optimized configurations. Also computes smoothness, frame-level fluctuation, and raw early variance metrics.

```bash
python improveDelay.py
```

> **Note:** Update the file paths at the top of each script to point to your local WAV recordings before running.

---

## FDN Architecture (SuperCollider)

The reverberation system is a sparse **4×4 Feedback Delay Network** implemented in SuperCollider using:

- `DelayN` UGens for the four delay lines
- A mixing matrix for cross-channel feedback
- Low-pass damping filters within the feedback loop (frequency-dependent absorption)
- Single-sample impulse excitation for clean impulse response capture
- Monophonic output (sum of delay-line outputs)

Preliminary **6×6** experiments were also conducted and indicated significantly increased sensitivity to damping, matrix interaction, and modal reinforcement — confirming that delay-spacing effects become more complex and less predictable as network order increases.

---

## Theoretical Background

A Feedback Delay Network in the z-domain is described by:

$$\mathbf{X}(z) = \mathbf{D}(z)\left[\mathbf{A}\,\mathbf{X}(z) + \mathbf{b}\,U(z)\right]$$

where $\mathbf{D}(z) = \text{diag}(z^{-m_1},\ldots,z^{-m_N})$ is the delay matrix, $\mathbf{A}$ is the feedback matrix, and $m_i$ are the delay lengths in samples. The output is $Y(z) = \mathbf{c}^T \mathbf{X}(z) + d\,U(z)$.

The residual ripple signal is defined as:

$$r[n] = \mathrm{dB}[n] - \mathrm{trend}[n] - \overline{\bigl(\mathrm{dB} - \mathrm{trend}\bigr)}$$

The FFT high-frequency ripple ratio is:

$$R_{HF} = \frac{\sum_{k > 0.7K} |R[k]|^2}{\sum_{k=0}^{K} |R[k]|^2}$$

---

## Limitations

- Analysis is restricted to **sparse low-order FDNs** (primarily 4×4); results may not generalise directly to dense or high-order networks.
- No formal perceptual listening study was conducted — analysis is entirely objective.
- A linear trend model is used for trend removal; slight curvature in real decays may leave systematic residuals.
- The FFT split frequency (70% of baseband) and dB analysis window (−5 to −60 dB) are empirically chosen constants.

---

## Future Work

- Higher-order FDN analysis (8×8, 16×16)
- Orthogonal and randomised feedback matrix comparison
- Formal ABX perceptual listening evaluation
- Frequency-band-resolved (octave / third-octave) ripple analysis
- Adaptive delay-spacing systems driven by real-time ACF feedback
- Mathematical characterisation of ripple risk from pairwise delay-length differences

---

## Citation

If you use or build upon this work, please cite as:

```
Borah, N. (2025). Multi-Scale Analysis of Ripple and Decay Behaviour in Sparse 
Feedback Delay Networks. Independent DSP Research Project. 
GitHub: https://github.com/0xnayan/FDN_analysis
```

---

## License

This project is released under the [MIT License](LICENSE) for research and educational purposes.

---

## Author

**Nayanmoni Borah**

Independent researcher in DSP, creative audio systems, signal analysis, and computational media.
