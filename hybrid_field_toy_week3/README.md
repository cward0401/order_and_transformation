# Week 3 – Hybrid Modular Field Toy with Closure Diagnostics

## Overview

This project implements a modular field model to explore how simple local rules generate structured, persistent, and recurring behavior over time.

---

## System Definition

Each cell updates according to:

s(t+1, i) = (a * N(t, i) + b) mod m

where:

N(t, i) = s(i-1) + s(i) + s(i+1)

The system is deterministic with periodic boundaries.

---

## Key Features

- Local interaction dynamics  
- Modular arithmetic update rule  
- Emergent structure and recurrence  

---

## Diagnostics

- Entropy  
- Coherence  
- Closure / recurrence  
- Closure lag spectrum  
- Dominant lag  
- Reconstruction coherence  
- Compression ratio  

---

## Observations

- Emergent recurrence (~14 timestep lag)  
- System stabilizes into a repeating regime  
- High reconstruction coherence after lock-in  
- Increasing structural regularity  

---

## Purpose

This project explores how memory-like structure and recurrence emerge from simple deterministic systems.