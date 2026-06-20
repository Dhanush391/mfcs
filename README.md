# CommLink-BPSK with Automatic Gain Control (AGC) and Synchronization

## Project Overview

This project implements a complete Binary Phase Shift Keying (BPSK) digital communication system and analyzes its performance under noisy channel conditions. The system includes Automatic Gain Control (AGC), timing synchronization analysis, BER evaluation, and Shannon Capacity benchmarking.

The project was developed as part of the **Mathematics for Communication Systems (MFCS)** course to demonstrate the practical application of signal processing, probability, filtering, and information theory concepts.

---

## Objectives

* Implement a complete BPSK communication link.
* Analyze Bit Error Rate (BER) performance over an AWGN channel.
* Compare theoretical and simulated BER results.
* Implement Automatic Gain Control (AGC).
* Study the impact of timing synchronization errors.
* Evaluate system performance using Shannon Capacity analysis.
* Calculate the Shannon Capacity Gap between practical and theoretical limits.

---

## System Architecture

Source → BPSK Modulator → Pulse Shaping Filter → AWGN Channel → AGC → Timing Synchronization → Matched Filter → Sampler & Decision → Data Sink

---

## Features

* BPSK Modulation and Demodulation
* AWGN Channel Simulation
* Matched Filter Receiver
* FIR Pulse Shaping Filter
* Automatic Gain Control (AGC)
* Timing Synchronization Study
* BER Analysis
* Shannon Capacity Analysis
* Monte Carlo Simulation

---

## Mathematical Layers

### Layer 1: Signal Representation

* BPSK signal generation
* Energy and power calculations

### Layer 2: Fourier Transform

* FFT analysis
* Power Spectral Density (PSD)
* Parseval's Theorem Verification

### Layer 3: LTI Systems and Matched Filter

* Channel modeling
* Correlator receiver
* Matched filter implementation

### Layer 4: Z-Transform and FIR Filtering

* FIR filter design
* Magnitude and phase response analysis

### Layer 5: Probability and BER

* Theoretical BER derivation
* Monte Carlo BER simulation

### Layer 6: Shannon Capacity

* Capacity calculation
* Spectral efficiency analysis
* Capacity gap evaluation

---

## Results

* Simulated BER closely matches theoretical BER.
* AGC maintains stable signal amplitude.
* Timing synchronization significantly affects BER performance.
* Practical BPSK operating point ≈ 9.6 dB.
* Shannon limit ≈ −1.6 dB.
* Observed capacity gap ≈ 11.2 dB.

---

## Technologies Used

* Python 3.x
* NumPy
* SciPy
* Matplotlib

---

## Applications

* Digital Communication Systems
* Wireless Communication
* Satellite Communication
* Software Defined Radio (SDR)
* Communication System Education and Research

---

## Conclusion

The project successfully demonstrates the design and analysis of a BPSK communication system. Theoretical and simulated BER results show strong agreement, while AGC and synchronization studies highlight practical receiver challenges. Shannon Capacity analysis provides insight into the gap between practical communication systems and theoretical limits.

---

## Author

M. Sai Dhanush

B.Tech – Electronics and Communication Engineering (ECE)
