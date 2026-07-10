---
title: "Common Spatial Pattern (CSP): A Correctness Proof"
published: false
tags: machinelearning, datascience, computerscience, tutorial
series: "Feature Engineering: Electroencephalogram"
---

> *Adapted from an appendix of my MS thesis. Equations render via Dev.to's KaTeX support.*

# Common Spatial Pattern

## Correctness Proof

The common spatial pattern (CSP) allows one to maximize the variance of signals from one condition and at the same time minimize the variance of signals from another condition [1]. For example, consider two three-dimensional tensors ({% katex inline %}\text{trials} \times \text{channels} \times \text{time}{% endkatex %}) of electroencephalogram (EEG) from separate classes {% katex inline %}\boldsymbol{X}_ 1,\boldsymbol{X}_ 2\in\mathbb{R}^ {p \times q \times r}{% endkatex %}. For each trial let us assume zero mean and compute between channel across time sample covariance matrices (SCMs) {% katex inline %}\boldsymbol{\Sigma}_ i^ {(k)}=\frac{1}{r-1}\boldsymbol{X}_ i^ {(k)}\boldsymbol{X}_ i^ {(k)\top}\in\mathbb{R}^ {q \times q}{% endkatex %} for {% katex inline %}i=1,2{% endkatex %} and {% katex inline %}k=1,\ldots,p{% endkatex %}. Furthermore, let us take {% katex inline %}\bar{\boldsymbol{\Sigma}}_ i\in\mathbb{R}^ {q \times q}{% endkatex %} as the arithmetic mean SCM for each class across all trials {% katex inline %}k{% endkatex %}.

![Example of averaged sample covariance matrices (SCMs).](assets/csp/scms.png)

Our example is a standard data and preprocessing pipeline for CSP used by software libraries like PyRiemann [2]. We assume the SCMs are conditioned so that they are symmetric positive definite (SPD). By definition, for a matrix {% katex inline %}\boldsymbol{A}\in\mathbb{R}^ {n \times n}{% endkatex %} and any non-zero vector {% katex inline %}\boldsymbol{x}\in\mathbb{R}^ n{% endkatex %}, if {% katex inline %}\boldsymbol{A}=\boldsymbol{A}^ \top{% endkatex %} and {% katex inline %}\boldsymbol{x}^ \top\boldsymbol{A}\boldsymbol{x}>0{% endkatex %}, then {% katex inline %}\boldsymbol{A}{% endkatex %} is SPD. As a result, all eigenvalues are positive {% katex inline %}\lambda_ i > 0{% endkatex %} from the eigendecomposition {% katex inline %}\boldsymbol{A}=\boldsymbol{Q}\boldsymbol{D}\boldsymbol{Q}^ \top{% endkatex %} where {% katex inline %}\boldsymbol{D} = \text{diag}(\lambda_ 1,\ldots,\lambda_ n){% endkatex %} [3]. Furthermore, the sum of two SPD matrices {% katex inline %}\boldsymbol{A},\boldsymbol{B}\in\mathbb{R}^ {n \times n}{% endkatex %} is also SPD since {% katex inline %}\boldsymbol{x}^ \top(\boldsymbol{A}+\boldsymbol{B})\boldsymbol{x}=\boldsymbol{x}^ \top\boldsymbol{A}\boldsymbol{x} + \boldsymbol{x}^ \top\boldsymbol{B}\boldsymbol{x} > 0{% endkatex %}. Let us diagonalize the mean SCMs from our example.


{% katex %}
\bar{\boldsymbol{\Sigma}}_ 1+\bar{\boldsymbol{\Sigma}}_ 2 = \boldsymbol{V}\boldsymbol{\Lambda}\boldsymbol{V}^ \top.
{% endkatex %}


![The averaged SCMs summed.](assets/csp/scms-summed.png)

The whitening transformation of an SCM results in zero mean, unit variance, and zero covariance [1]. In other words, the whitening transformation maps an SCM to the identity matrix {% katex inline %}\boldsymbol{\Sigma}\mapsto\boldsymbol{I}{% endkatex %}. We define the whitening matrix as {% katex inline %}\boldsymbol{W} = \boldsymbol{V}\boldsymbol{\Lambda}^ {-1/2}\boldsymbol{V}^ \top \in \mathbb{R}^ {n \times n}{% endkatex %}. The result is no longer an ellipse when plotted but rather the unit circle.


{% katex %}
\boldsymbol{W}(\bar{\boldsymbol{\Sigma}}_ 1+\bar{\boldsymbol{\Sigma}}_ 2)\boldsymbol{W}^ \top = \boldsymbol{V}\boldsymbol{\Lambda}^ {-1/2}\boldsymbol{V}^ \top(\boldsymbol{V}\boldsymbol{\Lambda}\boldsymbol{V}^ \top)\boldsymbol{V}\boldsymbol{\Lambda}^ {-1/2}\boldsymbol{V}^ \top = \boldsymbol{I}.
{% endkatex %}


We can rewrite our whitening transformation to show that the variance of the signals in our first class {% katex inline %}\bar{\boldsymbol{\Sigma}}_ 1{% endkatex %} is maximized, while the variance of the signals in our second class {% katex inline %}\bar{\boldsymbol{\Sigma}}_ 2{% endkatex %} is also minimized. We do this by distributing the whitening matrix throughout the sum of our SCMs. The result is two transformed SCMs we denote by {% katex inline %}\bar{\boldsymbol{\Sigma}}_ 1',\bar{\boldsymbol{\Sigma}}_ 2'\in\mathbb{R}^ {n \times n}{% endkatex %} whose sum is the identity matrix.


{% katex %}
\boldsymbol{W}(\bar{\boldsymbol{\Sigma}}_ 1+\bar{\boldsymbol{\Sigma}}_ 2)\boldsymbol{W}^ \top = \boldsymbol{W}\bar{\boldsymbol{\Sigma}}_ 1\boldsymbol{W}^ \top + \boldsymbol{W}\bar{\boldsymbol{\Sigma}}_ 2\boldsymbol{W}^ \top = \bar{\boldsymbol{\Sigma}}_ 1' + \bar{\boldsymbol{\Sigma}}_ 2' = \boldsymbol{I}.
{% endkatex %}


![Both the whitened sum of the SCMs and the sum of each SCM transformed by the whitening matrix equals the identity matrix.](assets/csp/scms-transformed.png)

Let us use {% katex inline %}\boldsymbol{V}_ i'\boldsymbol{\Lambda}_ i'\boldsymbol{V}_ i'^ \top{% endkatex %} where {% katex inline %}i=1,2{% endkatex %} to denote the diagonalization of our transformed SCMs. Since {% katex inline %}\bar{\boldsymbol{\Sigma}}_ 1' + \bar{\boldsymbol{\Sigma}}_ 2' = \boldsymbol{I}{% endkatex %} the sum of the diagonals {% katex inline %}d_ {ij} = \text{diag}(\boldsymbol{\Lambda}_ i')_ j{% endkatex %} is {% katex inline %}d_ {1j}+d_ {2j}=1{% endkatex %}. Furthermore, {% katex inline %}d_ {ij}>0{% endkatex %} since {% katex inline %}\bar{\boldsymbol{\Sigma}}_ i'{% endkatex %} is SPD. Therefore, the diagonals are bounded between 0 and 1. When the variance {% katex inline %}d_ {aj} \gg d_ {bj}{% endkatex %} for {% katex inline %}a \neq b{% endkatex %}, the classification problem is more or less solved for unseen EEG trials. However, when {% katex inline %}d_ {aj}{% endkatex %} is close to {% katex inline %}d_ {bj}{% endkatex %} the discrimination between classes is more ambiguous [1].


## References

1. Benjamin Blankertz (2018) *Gentle Introduction to Signal Processing and Classification for Single-Trial EEG Analysis*. CRC Press.
2. Alexandre Barachant, Quentin Barthélemy, Jean-Rémi King, Alexandre Gramfort, Sylvain Chevallier, Pedro L. C. Rodrigues, Emanuele Olivetti, Vladislav Goncharenko, Gabriel Wagner vom Berg, Ghiles Reguig, Arthur Lebeurrier, Erik Bjäreholt, Maria Sayu Yamamoto, Pierre Clisson, Marie-Constance Corsi, Igor Carrara, Apolline Mellot, Bruna Junqueira Lopes, Brent Gaisford, Ammar Mian, Anton Andreev, Gregoire Cattan, Arthur Lebeurrier (2025) *pyRiemann*. Zenodo.
3. Kevin P. Murphy (2022) *Probabilistic Machine Learning: An Introduction*. MIT Press.
