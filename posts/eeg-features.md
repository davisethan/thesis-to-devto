---
title: EEG Feature Engineering and Selection
published: true
tags: 'neuroscience, machinelearning, datascience, tutorial'
series: Electroencephalogram (EEG) Fundamentals
id: 4116539
date: '2026-07-10T23:55:11Z'
---

> *Adapted from an appendix of my MS thesis.*

## Feature Engineering & Selection

The event related features consist of chunks of time series concatenated from all the channels, resulting from a low pass or band pass filtering and a down sampling step. This category of features is relevant when considering evoked activity after the presentation of a stimulus (visual, auditory, or sensory). They are therefore of interest when one is expecting significant changes in several amplitudes occurring at a given moment [1].

The spectral features are used in the case of detection for an oscillatory activity, when changes in EEG rhythms amplitudes are expected. The features are associated with the power spectra estimated in a given channel and in a given frequency band for a specific time window. Power spectra can be computed through many methods like, most notably, spectrogram, Morlet wavelet scalogram, and autoregressive models [1].

Spatial filtering can be a valuable tool both for event related and spectral features. It relies on the combination of signals, recorded from different sensors, to obtain a new one, associated with an improved signal-to-noise ratio. Spatial filtering methods can be divided into three categories [1].

First, and not data driven, this category relies on physical considerations regarding the way the signals propagate through different brain tissues. The most famous illustration of this category is the Laplacian filter. In its simplest version, the small Laplacian consists of a derivation of the EEG waveform from the average signal computed with the four nearest neighbors for each electrode location [1].

Second, and data driven and unsupervised, this spatial filtering category can rely on a principal component analysis (PCA) approach. Third, and data driven and supervised, has its most famous examples in common spatial patterns (CSP) for spectral patterns and xDawn for event related features. CSP consists of a linear combination of EEG signals to maximize the difference between two classes in terms of variance. The xDawn approach aims at improving the signal-to-noise ratio through a projection of the raw EEG signals onto an estimated subspace of the evoked potentials [1].

Even though spectral and event related features are the most used in EEG literature, alternative features have been considered in past years. Firstly, features relying on covariance matrices have recently been used extensively, in particular for Riemannian geometry based classification. Despite an unclear neurophysiological interpretation, they have reached state of the art performance and won a large number of competitions. Secondly, new features, which take into account the interconnected nature of brain functioning and intensity of interactions, have emerged [1].

![Various contemporary forms of EEG data analysis [1].](assets/eeg-features/eeg-analysis.png)

Estimating brain interactions in real time is not trivial: it consists of finding a compromise between ensuring the quasi-stationary nature of the signals and the statistical reliability of the functional connectivity estimation. Recent studies have considered the use of brain network metrics as potential features. These include local and global network metrics [1].

At the local scale, the node degree counts the number of connections linking one node to another. In weighted networks, it is referred to as node strength and consists of summing the weights of the connections of the considered node. Another local scale property of interest is the betweenness centrality defined as the extent to which a node lies between other pairs of nodes. This metric enables the identification of the nodes that are crucial for information transfer between distant regions [1].

At the global scale, there is the characteristic path length and clustering coefficient. The characteristic path length indicates the global tendency of the nodes in the network to integrate and exchange information. The clustering coefficient measures the tendency of having nodes whose neighbors are mutually interconnected [1].

The feature selection is a crucial step as it prevents redundancy, ensures the reliability of the features, reduces dimensionality tuned, and helps to provide interpretable results. It can be divided into three categories: embedded, filtered, and wrapper methods [1].

In filter methods, the feature selection is performed independently and before evaluation. For example, the {% katex inline %}R^ 2{% endkatex %} score criterion can be used to assess to which extent a given feature is influenced by a task performed by the subject. In wrapper methods, the feature selection utilizes the classification. In other words, in an iterative process, the relevance of each subset of features is assessed through classification performance until a given criterion is met. The embedded method consists of integrating both the feature selection and classification in the same process, for example, with a decision tree [1].


## References

1. Corsi, Marie-Constance (2023) *Electroencephalography and Magnetoencephalography*. Springer US.
