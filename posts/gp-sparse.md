---
title: Sparse Gaussian Process Approximations
published: true
tags: 'machinelearning, datascience, statistics, tutorial'
series: Gaussian Processes (GP)
id: 4121239
date: '2026-07-11T18:03:18Z'
---

> *Adapted from an appendix of my MS thesis.*

## Sparse Approximation

The best way to perform GP inference and training is to compute a Cholesky decomposition of the {% katex inline %}N \times N{% endkatex %} Gram matrix. Unfortunately, this take {% katex inline %}\mathcal{O}(N^ 3){% endkatex %} time. Instead, we can use an approximation method based on inducing points, also called pseudoinputs, which are like a learned summary of the training data that we can condition on, rather than conditioning on all of it [1].

Let {% katex inline %}\boldsymbol{X}{% endkatex %} be the observed inputs, and {% katex inline %}\boldsymbol{f}_ X=f(\boldsymbol{X}){% endkatex %} be the unknown vector of function values for which we have observations {% katex inline %}\boldsymbol{y}{% endkatex %}. Let {% katex inline %}\boldsymbol{f}_ \ast{% endkatex %} be the unknown function values at one or more test points {% katex inline %}\boldsymbol{X}_ \ast{% endkatex %}. Finally, let us assume we have {% katex inline %}M{% endkatex %} additional inputs {% katex inline %}\boldsymbol{Z}{% endkatex %} with unknown function values {% katex inline %}\boldsymbol{f}_ Z{% endkatex %} also denoted by {% katex inline %}\boldsymbol{u}{% endkatex %}. The exact joint prior has the following form [1].


{% katex %}
p(\boldsymbol{f}_ X,\boldsymbol{f}_ \ast)
= \int p(\boldsymbol{f}_ \ast,\boldsymbol{f}_ X,\boldsymbol{f}_ Z)\mathrm{d}\boldsymbol{f}_ Z
= \int p(\boldsymbol{f}_ \ast,\boldsymbol{f}_ X|\boldsymbol{f}_ Z)p(\boldsymbol{f}_ Z)\mathrm{d}\boldsymbol{f}_ Z
= \mathcal{N}\left(\boldsymbol{0},
\begin{pmatrix}
\boldsymbol{K}_ {X,X} & \boldsymbol{K}_ {X,\ast} \\\\
\boldsymbol{K}_ {\ast,X} & \boldsymbol{K}_ {\ast,\ast} \\\\
\end{pmatrix}
\right).
{% endkatex %}


We can choose {% katex inline %}\boldsymbol{f}_ Z{% endkatex %} in such a way that it acts as a sufficient statistic for the data, so that we can predict {% katex inline %}\boldsymbol{f}_ \ast{% endkatex %} just using {% katex inline %}\boldsymbol{f}_ Z{% endkatex %} instead of {% katex inline %}\boldsymbol{f}_ X{% endkatex %}, and thus we approximate the prior as follows [1].


{% katex %}
p(\boldsymbol{f}_ \ast,\boldsymbol{f}_ X,\boldsymbol{f}_ Z)
= p(\boldsymbol{f}_ \ast|\boldsymbol{f}_ X,\boldsymbol{f}_ Z)p(\boldsymbol{f}_ X|\boldsymbol{f}_ Z)p(\boldsymbol{f}_ Z)
\approx p(\boldsymbol{f}_ \ast|\boldsymbol{f}_ Z)p(\boldsymbol{f}_ X|\boldsymbol{f}_ Z)p(\boldsymbol{f}_ Z).
{% endkatex %}


From this we derive the following train and test conditionals [1].


{% katex %}
\begin{aligned}
p(\boldsymbol{f}_ X|\boldsymbol{f}_ Z) &= \mathcal{N}(\boldsymbol{f}_ X|\boldsymbol{K}_ {X,Z}\boldsymbol{K}_ {Z,Z}^ {-1}\boldsymbol{f}_ Z,\boldsymbol{K}_ {X,X}-\boldsymbol{Q}_ {X,X}) \\\\
p(\boldsymbol{f}_ \ast|\boldsymbol{f}_ Z) &= \mathcal{N}(\boldsymbol{f}_ \ast|\boldsymbol{K}_ {\ast,Z}\boldsymbol{K}_ {Z,Z}^ {-1}\boldsymbol{f}_ Z,\boldsymbol{K}_ {\ast,\ast}-\boldsymbol{Q}_ {\ast,\ast}).\end{aligned}
{% endkatex %}


The above equations can be seen as exact inference on noise-free observations {% katex inline %}\boldsymbol{f}_ Z{% endkatex %}. To gain computational speedups, we can make further approximations to the terms {% katex inline %}\tilde{\boldsymbol{Q}}_ {X,X}=\boldsymbol{K}_ {X,X}-\boldsymbol{Q}_ {X,X}{% endkatex %} and {% katex inline %}\tilde{\boldsymbol{Q}}_ {\ast,\ast}=\boldsymbol{K}_ {\ast,\ast}-\boldsymbol{Q}_ {\ast,\ast}{% endkatex %}. We can then derive the approximate prior {% katex inline %}q(\boldsymbol{f}_ X,\boldsymbol{f}_ \ast)=\int q(\boldsymbol{f}_ X|\boldsymbol{f}_ Z)q(\boldsymbol{f}_ \ast|\boldsymbol{f}_ Z)p(\boldsymbol{f}_ Z)\mathrm{d}\boldsymbol{f}_ Z{% endkatex %}, which we then condition on the observations in the usual way. All of these approximations result in a training cost of {% katex inline %}\mathcal{O}(M^ 3+NM^ 2){% endkatex %}, and then take {% katex inline %}\mathcal{O}(M){% endkatex %} time for the predictive mean for each test case, and {% katex inline %}\mathcal{O}(M^ 2){% endkatex %} time for the predictive variance. Compare this to {% katex inline %}\mathcal{O}(N^ 3){% endkatex %} training time and {% katex inline %}\mathcal{O}(N){% endkatex %} and {% katex inline %}\mathcal{O}(N^ 2){% endkatex %} testing time for exact inference [1].

The deterministic inducing conditional (DIC) approximation, or the subset of regressors (SOR) approximation, results from assuming {% katex inline %}\tilde{\boldsymbol{Q}}_ {X,X}=\boldsymbol{0}{% endkatex %} and {% katex inline %}\tilde{\boldsymbol{Q}}_ {\ast,\ast}=\boldsymbol{0}{% endkatex %}, so the conditionals are deterministic. This can result in an underestimate of the predictive variance. One way to overcome the overconfidence of DIC is to only assume {% katex inline %}\tilde{\boldsymbol{Q}}_ {X,X}=\boldsymbol{0}{% endkatex %} but let {% katex inline %}\tilde{\boldsymbol{Q}}_ {\ast,\ast}=\boldsymbol{K}_ {\ast,\ast}-\boldsymbol{Q}_ {\ast,\ast}{% endkatex %} be exact. This is called the deterministic training conditional (DTC). Lastly, the fully independent training conditional (FITC) approximation assumes {% katex inline %}q(\boldsymbol{f}_ X|\boldsymbol{f}_ Z){% endkatex %} is fully factorized. This throws away less uncertainty than the SOR and DTC methods, since it does not make any deterministic assumptions about the relationship between {% katex inline %}\boldsymbol{f}_ X{% endkatex %} and {% katex inline %}\boldsymbol{f}_ Z{% endkatex %} [1].


{% katex %}
\begin{aligned}
q_ {\mathrm{SOR}}(\boldsymbol{f}_ X,\boldsymbol{f}_ \ast) &= \mathcal{N}\left(\boldsymbol{0},
\begin{pmatrix}
\boldsymbol{Q}_ {X,X} & \boldsymbol{Q}_ {X,\ast} \\\\
\boldsymbol{Q}_ {\ast,X} & \boldsymbol{Q}_ {\ast,\ast} \\\\
\end{pmatrix}
\right) \\\\
q_ {\mathrm{DTC}}(\boldsymbol{f}_ X,\boldsymbol{f}_ \ast) &=
\mathcal{N}\left(\boldsymbol{0},
\begin{pmatrix}
\boldsymbol{Q}_ {X,X} & \boldsymbol{Q}_ {X,\ast} \\\\
\boldsymbol{Q}_ {\ast,X} & \boldsymbol{K}_ {\ast,\ast} \\\\
\end{pmatrix}
\right) \\\\
q_ {\mathrm{FITC}}(\boldsymbol{f}_ X,\boldsymbol{f}_ \ast) &=
\mathcal{N}\left(\boldsymbol{0},
\begin{pmatrix}
\boldsymbol{Q}_ {X,X}-\operatorname{diag}(\boldsymbol{Q}_ {X,X}-\boldsymbol{K}_ {X,X}) & \boldsymbol{Q}_ {X,\ast} \\\\
\boldsymbol{Q}_ {\ast,X} & \boldsymbol{K}_ {\ast,\ast} \\\\
\end{pmatrix}
\right).\end{aligned}
{% endkatex %}


![Sparse GP comparison.](assets/gp-sparse/full-gp.png)

![Sparse GP comparison.](assets/gp-sparse/sparse-dtc.png)

The simplest approach to selecting the inducing points from the training set is to throw away some of the data. In this case, we could pick random examples. However, intuitively it makes more sense to try to pick a subset that in some sense covers the original data, so it contains approximately the same information without redundancy. Clustering algorithms such as {% katex inline %}k{% endkatex %}-means are a popular heuristic approach. We can also use coreset methods which can provably find such an information preserving subset. Furthermore, we can approach learning the inducing points by treating them like kernel hyperparameters, and choosing them so as to maximize the log marginal likelihood [1].


## References

1. Kevin P. Murphy (2023) *Probabilistic Machine Learning: Advanced Topics*. MIT Press.
