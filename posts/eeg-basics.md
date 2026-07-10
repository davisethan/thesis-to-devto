---
title: 'EEG Basics: How Brain Activity Becomes a Signal'
published: true
tags: 'neuroscience, machinelearning, datascience, tutorial'
series: Electroencephalogram (EEG) Fundamentals
id: 4116498
date: '2026-07-10T23:43:59Z'
---

> *Adapted from an appendix of my MS thesis.*

## Basic Principles

The origin of electroencephalogram (EEG) signals comes from neurons creating electrical signals that are transmitted to other cells through synapses. An action potential (AP) arrives at a synaptic cleft (step 1 in the figure) where it transmits chemical information through neurotransmitters (step 2) that generate postsynaptic potentials (PSPs) and local current (step 3). A PSP will create a current sink and will propogate to the cell body to generate a current source (step 4) [1].

As a result, the postsynaptic potential creates an electrical dipole consisting of a negative pole (the sink) and a positive pole (the source). The dipole generates primary (intracellular) currents and secondary (extracellular) currents. EEG signals result from postsynaptic potentials. More specifically, EEG signals result from the spatial and temporal summation of activity from a large population of synchronous neurons [1].

![Example of neural activity [1].](assets/eeg-basics/neurons.jpg)

EEG signals correspond to a difference between electrical potentials, mainly due to extracellular currents. It is sensitive to both radial currents (actively located at the gyrus level) and to tangential currents (generated within sulci) even though it has strong sensitivity to radial currents. EEG, though, is also strongly attenuated and deformed by crossing through the skull [1].

**Characteristics of EEG** [1]

| Property | Value |
| :-- | :-- |
| Measurement | Difference of potentials, extracellular currents |
| Spatial resolution | 2–3 cm |
| Temporal resolution | 1 ms or less |
| Amplitudes | ≈ 100 μVolts |
| Advantages | Portable, low cost |
| Drawbacks | Need of a reference, affected by bone, diffuse |

There are two main types of electrophysiological activity of interest that are exploited for EEG: the evoked and oscillatory activity. Evoked responses are weak variations of electromagnetic activity resulting from a stimulation, such as in response to a task performed by the participant. There is a specific way to identity and describe evoked responses according to their latency, amplitude, shape, and polarity [1].

The figure first shows a positive deflection occurring 300 ms after the presentation of a stimulation. These waves of evoked activity can reflect different mechanisms: the early components are mostly exogenous and are related to stimulus characteristics, and late components are endogenous and are related to the performed task and to the subject’s state. Alternatively, oscillatory activity, or induced activity, results from the summation of activity in a given brain region. These rhythms are mainly defined by their frequency, amplitude, shape, location, and duration [1].

![P300 waves visualization [1].](assets/eeg-basics/p300.jpeg)

Each frequency band is referred to by a Greek letter and corresponds to a subject’s state. Delta (0.5–3 Hz) and Theta (3–7 Hz) rhythms are detected in deep and slight sleeps respectively. Alpha (8–12 Hz in posterior areas) and Mu (7–13 Hz in central areas) rhythms are observed in quiet watch and resting state (with eyes closed for Alpha). Beta (13–30 Hz) rhythm is detected during active watch and cognitive tasks such as motor imagery. Gamma rhythm (divided into two sub-rhythms: slow in 30–70 Hz and fast beyond 70 Hz) is observed during specific cognitive processing [1].

![Frequency bands characteristics [1].](assets/eeg-basics/frequency.jpeg)


## References

1. Corsi, Marie-Constance (2023) *Electroencephalography and Magnetoencephalography*. Springer US.
