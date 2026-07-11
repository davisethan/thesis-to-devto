---
title: Non-centered Parameterization for MCMC
published: true
tags: 'machinelearning, datascience, statistics, tutorial'
series: Markov Chain Monte Carlo (MCMC)
id: 4117134
---

> *Adapted from an appendix of my MS thesis.*

## Non-centered Parameterization

For relatively simple models, samplers mostly just work, providing us with an accurate estimate of the posterior. However, certain posterior geometries are challenging for samplers. A common example is Neal’s funnel. The shape at the top of the funnel is quite wide before narrowing into a small neck. Samplers function by taking steps from one set of parameter values to another, and a key setting is how large of a step to take when exploring the posterior surface. In complex geometries, such as with Neal’s funnel, a step size that works well in one area fails in another [1].

![An example of Neal’s Funnel created from correlated samples. At the top of the funnel, where {% katex inline %}y{% endkatex %} is between 6 to 8, a step size of say 1 unit is likely to stay in a dense region of the posterior. However, when sampling at the bottom of the posterior, around {% katex inline %}y{% endkatex %} between -6 to -8, a step size of 1 unit in almost any direction will likely step into a low-density region. For HMC samplers, the occurrence of divergences can diagnose these sampling issues [1].](assets/mcmc-noncentered/neals-funnel.png)

In hierarchical models the posterior geometry is largely defined by the correlation of hyperpriors to other parameters, which can result in funnel geometry that are difficult to sample. These inconvenient posteriors can create inefficient MCMC caused by steep curvature in the negative log-likelihood and lead to divergent transitions. Transforming the prior to be smoother helps. There is a relatively simple tweak to models, referred to as a non-centered parameterization, that helps alleviate the issue [1].

### Example: Devil’s Funnel prior


{% katex %}
\begin{aligned}
v &\sim \mathrm{Normal}(0,\sigma_ v) \\\\
x &\sim \mathrm{Normal}(0, \exp(v)).\end{aligned}
{% endkatex %}


As {% katex inline %}\sigma_ v{% endkatex %} increases, a trough forms in the prior probability surface known as centered parameterization that is difficult for Hamiltonian dynamics to sample [2, 3].

![Centered parameterization [2, 3].](assets/mcmc-noncentered/centered-sigma-05.png)

![Centered parameterization [2, 3].](assets/mcmc-noncentered/centered-sigma-1.png)

![Centered parameterization [2, 3].](assets/mcmc-noncentered/centered-sigma-3.png)

To handle this, we could configure a smaller steps size to manage the steepness better, but then sampling would take longer to explore the posterior. Alternatively, we can re-parameterize (transform) to make the surface smoother known non-centered parameterization. For this purpose, we add an auxiliary variable {% katex inline %}z{% endkatex %} that has a smooth probability surface. We then sample that auxiliary variable, and transform it to obtain the target variable distribution. For the case of the devil’s funnel prior we do the following [2, 3].


{% katex %}
\begin{aligned}
v &\sim \mathrm{Normal}(0, \sigma_ v) \\\\
z &\sim \mathrm{Normal}(0, 1) \\\\
x &= z\exp(v).\end{aligned}
{% endkatex %}


![Non-centered parameterization [2, 3].](assets/mcmc-noncentered/non-centered-sigma-05.png)

![Non-centered parameterization [2, 3].](assets/mcmc-noncentered/non-centered-sigma-1.png)

![Non-centered parameterization [2, 3].](assets/mcmc-noncentered/non-centered-sigma-3.png)

We can also transform sampling using Cholesky factors. The Cholesky factor {% katex inline %}\boldsymbol{L}{% endkatex %} provides an efficient means for encoding a correlation matrix {% katex inline %}\boldsymbol{\Omega}{% endkatex %} since it requires fewer floating point numbers than the full correlation matrix. It is defined by {% katex inline %}\boldsymbol{\Omega}=\boldsymbol{L}\boldsymbol{L}^ \top{% endkatex %} where {% katex inline %}\boldsymbol{L}{% endkatex %} is a lower-triangular matrix. We can sample data with correlation {% katex inline %}\boldsymbol{\Omega}{% endkatex %}, and standard deviation {% katex inline %}\sigma_ i{% endkatex %}, using the Cholesky factorization {% katex inline %}\boldsymbol{L}{% endkatex %} of {% katex inline %}\boldsymbol{\Omega}{% endkatex %} as follows where {% katex inline %}\boldsymbol{Z}{% endkatex %} is a matrix of {% katex inline %}z{% endkatex %}-scores sampled from a standard normal distribution [2, 3].


{% katex %}
\begin{aligned}
\boldsymbol{X_ \Omega} \sim \operatorname{diag}(\sigma_ i)\boldsymbol{L}\boldsymbol{Z}.\end{aligned}
{% endkatex %}



## References

1. Martin, Osvaldo A., Kumar, Ravin, Lao, Junpeng (2021) *Bayesian Modeling and Computation in Python*. Chapman and Hall/CRC.
2. McElreath, Richard (2020) *Statistical Rethinking: A Bayesian Course with Examples in R and STAN*. Chapman and Hall/CRC.
3. Dustin Stansbury, Richard McElreath (2024) *Correlated Features*. Zenodo.
