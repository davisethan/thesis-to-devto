---
title: 'Recording EEG: Electrodes, Montages, and Protocol'
published: true
tags: 'neuroscience, machinelearning, datascience, tutorial'
series: Electroencephalogram (EEG) Fundamentals
id: 4116531
date: '2026-07-10T23:45:37Z'
---

> *Adapted from an appendix of my MS thesis.*

## Experiment Protocol

EEG signals are recorded through the use of electrodes placed over the scalp. The EEG relies on different types of electrodes: wet/dry and active/passive electrodes. Wet electrodes need an electrolytic gel to enable conduction between the skin and electrode. Dry electrodes behave as a conductor between the skin and electrode. Active electrodes contain an electronic module that performs a pre-amplification of the signal to ensure stability of the system from changes in impedance and noise. Passive electrodes do not use a pre-amplification module [1].

Even though some differences can be found from one EEG device to another, there are standardized ways to name and localize EEG sensors (also called channels). Each channel is referred to by a letter and number. Odd channels are located on the left hemisphere and even ones on the right hemisphere. The letters correspond to the area: frontal, temporal, parietal, central, and occipital. In addition to the sensors, one can also find landmarks: nasion, inion, and pre-auricular points [1].

![Experiment protocol for EEG data acquisition [1].](assets/eeg-protocol/experiment-protocol.jpg)

Depending on the scientific question to be addressed and, therefore, the brain areas of interest, different montages can be found. One can build an EEG montage from less than 5 electrodes and up to 256 electrodes. EEG measurements rely on a difference of electrical potentials. For this purpose, two montages can be considered: the referential and bipolar montage [1].

In the referential montage each difference of electrical potentials considers an electrode placed over the scalp and a reference. The choice of the reference is crucial. The most commonly chosen locations for the reference electrodes are the mastoids (temporal bone behind the ears), though several studies prefer placing the reference at the vertex (Cz, midline of the scalp). The bipolar montage consists of performing the difference between two electrodes after the experiment. Another electrode referred to as the ground electrode is used. Among the chosen locations is the scapula (shoulder blade) [1].

There has been increased interest in developing wearable EEG, to remove wires and reduce its dimension but also to enable long lasting recordings in a less constrained environment. Three bottlenecks need to be overcome: the EEG electrodes, hard to put on and keep in place on the head; the EEG hardware, to make it less power consuming and miniaturized; and the EEG software, to propose the most intelligible and reliable information regarding the captured brain activity [1].

For data acquisition, it will consist of cleaning the locations where electrodes will be in contact with the skin, like forehead and mastoids. The electrodes and EEG cap are then placed. Several key distances can be measured to verify the cap is well placed. Then, the experimenter needs to ensure that the communication between electrodes and scalp is established. For that purpose, an assessment of the impedance is made for each electrode. The lower it is, the better it is. Once impedance are lower than a certain threshold, typically a few kOhms, then the experiment can start [1].

Once the subject is correctly in place, the experimenter can start some pre-recordings to check quality of the signal and give specific instructions to the subjects accordingly, like loosening the jaw to avoid muscular artifacts. Finally, the experimenter can give further instructions regarding the task to perform before starting the recordings. After the session ends, the data is stored in specific servers to be processed [1].


## References

1. Corsi, Marie-Constance (2023) *Electroencephalography and Magnetoencephalography*. Springer US.
