# Multi-Scale Analysis of Ripple and Decay Behavior in Sparse Feedback Delay Networks

An independent DSP research project investigating how delay-spacing strategies influence macro decay smoothness, micro-level ripple behavior, and residual correlation structures in sparse Feedback Delay Networks (FDNs).

---

## Overview

This project explores the relationship between delay spacing and reverberant decay behavior in low-order Feedback Delay Networks (FDNs) using:

* SuperCollider for FDN synthesis
* Python for objective signal analysis
* Residual ripple extraction
* FFT-based ripple metrics
* Autocorrelation analysis
* Comparative delay-network studies

The work evolved from a simple reverberation experiment into a multi-scale investigation of how different delay structures affect:

* Global decay smoothness
* Local ripple fluctuation
* Residual periodicity
* Persistent microstructure
* Decorrelation behavior

---

# Research Motivation

Artificial reverberation systems often suffer from:

* Metallic ringing
* Periodic resonance buildup
* Ripple artifacts in decay envelopes
* Persistent feedback structures

Many delay-spacing strategies aim to reduce these artifacts through:

* Irregular spacing
* Optimized delay configurations
* Quasi-uniform perturbations
* Irrational spacing methods

However, the relationship between:

* perceptual smoothness,
* ripple behavior,
* and residual correlation

is not always straightforward.

This project investigates these relationships through objective analysis rather than relying solely on listening evaluation.

---

# Core Research Question

> How do different delay-spacing strategies influence macro-scale decay smoothness and micro-scale ripple behavior in sparse low-order FDN systems?

---

# Key Findings

The study revealed several non-intuitive behaviors:

* Delay configurations that appeared smoother globally often produced stronger micro-level ripple structures.
* Ripple smoothness and decorrelation are not equivalent objectives.
* Irregular delay spacing produced the strongest decorrelation behavior.
* Quasi-uniform and golden-ratio spacing introduced persistent long-range residual structures in sparse networks.
* Macro decay smoothness does not guarantee micro-level ripple smoothness.

---

# Implemented Delay Configurations

| Configuration | Description                                         |
| ------------- | --------------------------------------------------- |
| Uniform       | Equal delay spacing                                 |
| Irregular     | Linearly increasing delay spacing                   |
| Optimized     | Manually optimized clustered spacing                |
| Quasi-uniform | Controlled perturbation around uniform spacing      |
| Golden-ratio  | Irrational spacing using golden-ratio relationships |

---

# System Architecture

## Feedback Delay Network

The reverberation system was implemented in SuperCollider using:

* Sparse low-order FDN structures
* Feedback matrices
* Delay-line feedback loops
* Low-pass damping
* Variable delay spacing strategies

---

# Analysis Pipeline

The analysis framework was implemented in Python.

## Pipeline Steps

```text
Audio Signal
    ↓
Envelope Extraction
    ↓
Smoothing
    ↓
Decay Region Isolation
    ↓
Trend Fitting
    ↓
Residual Extraction
    ↓
Ripple / Correlation Analysis
```

---

# Ripple Analysis

Residual ripple behavior was studied by removing the global decay trend from the decay envelope.

## Residual Definition

```math
Residual = Signal - Trend
```

This allowed micro-level ripple structures to be analyzed independently from the large-scale decay envelope.

---

# Ripple Metrics

The following objective metrics were implemented:

| Metric                        | Purpose                       |
| ----------------------------- | ----------------------------- |
| Variance                      | Global residual deviation     |
| MAD (Mean Absolute Deviation) | Average ripple magnitude      |
| Derivative Energy             | Local fluctuation roughness   |
| FFT Ripple Energy             | High-frequency ripple content |

---

# Autocorrelation Study

Autocorrelation analysis was used to investigate:

* residual periodicity
* persistent structures
* decorrelation behavior
* long-range self-similarity

This study revealed that some spacing strategies reduced direct periodicity while simultaneously increasing persistent coherent structures.

---

# Experimental Observations

## Uniform Delays

* Periodic but stable
* Strong coherent ringing
* Moderate residual structure

---

## Irregular Delays

* Strongest decorrelation
* Reduced periodicity
* Better residual diffusion

---

## Optimized Delays

* Smoother macro decay envelope
* Increased micro-level ripple structure
* Persistent residual correlation

---

## Quasi-uniform Delays

* Long-range correlation locking
* Coherent reinforcement structures
* Unstable residual behavior

---

## Golden-ratio Delays

* Reduced direct periodicity
* Sparse coherent interference structures
* Persistent autocorrelation patterns in sparse networks

---

# Important Insight

One of the most significant findings of this project was:

> Improving global decay smoothness does not necessarily improve local ripple smoothness.

This highlights the multi-scale nature of reverberant decay behavior in sparse delay networks.

---

# Tools & Technologies

## Audio / DSP

* SuperCollider
* Feedback Delay Networks (FDNs)
* Delay-line reverberation

## Analysis

* Python
* NumPy
* SciPy
* Matplotlib

## Techniques

* Envelope extraction
* FFT analysis
* Residual analysis
* Autocorrelation analysis
* Trend fitting
* Ripple isolation

---

# Repository Structure

```text
.
├── supercollider/
│   ├── fdn_uniform.scd
│   ├── fdn_irregular.scd
│   ├── fdn_optimized.scd
│   └── fdn_experiments.scd
│
├── analysis/
│   ├── rippleSmoothness.py
│   ├── autocorrelationStudy.py
│   └── plots/
│
├── audio/
│   ├── delay_uniform.wav
│   ├── delay_irregular.wav
│   ├── delay_optimized.wav
│   └── experimental/
│
└── report/
    └── final_report.pdf
```

---

# Example Plots

The project includes:

* Decay curve comparison
* Residual ripple analysis
* Signal vs trend visualization
* Autocorrelation comparison

These plots were used to compare macro-scale and micro-scale decay behavior across multiple delay configurations.

---

# Limitations

This study primarily focuses on:

* sparse low-order FDN systems,
* particularly 4×4 structures.

The results may not directly generalize to:

* dense reverberation networks,
* high-order FDNs,
* or perceptually optimized commercial reverberators.

Preliminary 6×6 experiments indicated significantly increased sensitivity to:

* damping,
* matrix interaction,
* modal reinforcement,
* and feedback stability.

---

# Future Work

Possible future directions include:

* Higher-order FDN analysis
* Orthogonal matrix optimization
* Perceptual listening studies
* Frequency-dependent ripple analysis
* Echo-density evolution studies
* Adaptive delay-spacing systems
* Real-time visualization tools

---

# Conclusion

This project demonstrates that delay-spacing strategies affect reverberant systems across multiple structural scales.

While some configurations improved global decay smoothness, they simultaneously introduced stronger micro-level ripple structures and persistent residual correlation.

The results suggest that:

* decorrelation,
* ripple smoothness,
* and decay stability

are interconnected but distinct properties in sparse Feedback Delay Networks.

---

# Author

**Nayanmoni Borah**

Independent DSP / Audio Research Project

Focused on:

* DSP
* Creative Audio Systems
* Signal Analysis
* Experimental Sound Design
* Computational Media

---

# License

This project is released for research and educational purposes.
