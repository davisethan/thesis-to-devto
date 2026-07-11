---
title: "Hamiltonian Monte Carlo (HMC)"
published: false
tags: machinelearning, datascience, statistics, tutorial
series: "Markov Chain Monte Carlo (MCMC)"
id: 4117135
---

> *Adapted from an appendix of my MS thesis.*

## Hamiltonian Monte Carlo

Hamiltonian Monte Carlo (HMC) is a type of MCMC method that makes use of gradients to generate new proposed states. HMC attempts to avoid the random walk behavior typical of Metropolis-Hastings by using the gradient to propose new positions far from the current one with high acceptance probability. This allows HMC to better scale to higher dimensions and in principle more complex geometries [1].

In physical systems, the Hamiltonian is a description of the total energy. The total energy can be decomposed into two terms, the kinetic and the potential energy. We can write the Hamiltonian of such a system as the following where {% katex inline %}K(\boldsymbol{p},\boldsymbol{q}){% endkatex %} is the kinetic energy and {% katex inline %}V(\boldsymbol{q}){% endkatex %} is the potential energy [1].


{% katex %}
H(\boldsymbol{q},\boldsymbol{p}) = K(\boldsymbol{p},\boldsymbol{q}) + V(\boldsymbol{q}).
{% endkatex %}


The probability of being at a particular position with a particular momentum is given as follows [1]. The exponential is a non-negative quantity and can therefore be viewed as an unnormalized probability distribution. The introduction of the minus sign in the exponential is simply a convention, meaning that higher values of energy correspond to lower values of probability [2].


{% katex %}
p(\boldsymbol{q},\boldsymbol{p}) = \exp\left(-H(\boldsymbol{q},\boldsymbol{p})\right).
{% endkatex %}


To simulate such systems the Hamiltonian equations must be solve [1].


{% katex %}
\begin{aligned}
\frac{\mathrm{d}\boldsymbol{q}}{\mathrm{d}t} &= \frac{\partial H}{\partial \boldsymbol{p}} = \frac{\partial K}{\partial \boldsymbol{p}} + \frac{\partial V}{\partial \boldsymbol{p}} \\\\
\frac{\mathrm{d}\boldsymbol{p}}{\mathrm{d}t} &= -\frac{\partial H}{\partial \boldsymbol{q}} = -\frac{\partial K}{\partial \boldsymbol{q}} - \frac{\partial V}{\partial \boldsymbol{q}}.\end{aligned}
{% endkatex %}


The potential energy {% katex inline %}V(\boldsymbol{q}){% endkatex %} is given by the probability we wish to sample from {% katex inline %}p(\boldsymbol{q}){% endkatex %}. For the momentum {% katex inline %}K(\boldsymbol{p},\boldsymbol{q}){% endkatex %} we can invoke an auxiliary variable, and by choosing {% katex inline %}p(\boldsymbol{p}|\boldsymbol{q}){% endkatex %} we can write {% katex inline %}p(\boldsymbol{q},\boldsymbol{p}) = p(\boldsymbol{p}|\boldsymbol{q})p(\boldsymbol{q}){% endkatex %}. This ensures we can recover the target distribution by marginalizing out the momentum. By introducing the auxiliary variable we can rewrite the equation [1].


{% katex %}
H(\boldsymbol{q},\boldsymbol{p}) = -\log p(\boldsymbol{p}|\boldsymbol{q}) - \log p(\boldsymbol{q}).
{% endkatex %}


We are free to choose the kinetic energy, and if we choose it to be Gaussian and drop the normalization constant, then we have the following where {% katex inline %}\boldsymbol{M}{% endkatex %} is the precision matrix [1].


{% katex %}
K(\boldsymbol{p},\boldsymbol{q}) = \frac{1}{2}\boldsymbol{p}^ \top\boldsymbol{M}^ {-1}\boldsymbol{p} + \log \left|\boldsymbol{M}\right|.
{% endkatex %}


If we choose {% katex inline %}\boldsymbol{M}{% endkatex %} to be the identity matrix we have {% katex inline %}K(\boldsymbol{p},\boldsymbol{q})=\frac{1}{2}\boldsymbol{p}^ \top\boldsymbol{p}{% endkatex %}, making {% katex inline %}\frac{\partial K}{\partial \boldsymbol{p}}=\boldsymbol{p}{% endkatex %} and {% katex inline %}\frac{\partial K}{\partial \boldsymbol{q}}=0{% endkatex %}, and then we can simplify the Hamiltonian equations [1].


{% katex %}
\begin{aligned}
\frac{\mathrm{d}\boldsymbol{q}}{\mathrm{d}t} &= \boldsymbol{p} \\\\
\frac{\mathrm{d}\boldsymbol{p}}{\mathrm{d}t} &= -\frac{\partial V}{\partial\boldsymbol{q}}.\end{aligned}
{% endkatex %}


Therefore, the HMC algorithm can be summarized as follows [1].

1.  Sample {% katex inline %}\boldsymbol{p}\sim\mathcal{N}(0,\boldsymbol{I}){% endkatex %}

2.  Simulate {% katex inline %}\boldsymbol{q}_ t{% endkatex %} and {% katex inline %}\boldsymbol{p}_ t{% endkatex %} for some amount of time {% katex inline %}T{% endkatex %}

3.  {% katex inline %}\boldsymbol{q}_ T{% endkatex %} is the new proposed state

4.  Use the Metropolis acceptance criterion to accept or reject {% katex inline %}\boldsymbol{q}_ T{% endkatex %}.

In an idealized model, energy is perfectly conserved. However, we use the Metropolis acceptance criterion to correct for errors introduced by the numerical simulation of the Hamiltonian equations. To compute the Hamiltonian equations we have to compute a trajectory. That is, all the intermediate points between one state and the next. In practice this involves computing a series of small integration steps. The most popular method is the leapfrog integrator. Leapfrog integration updates positions {% katex inline %}\boldsymbol{q}_ t{% endkatex %} and momentums {% katex inline %}\boldsymbol{p}_ t{% endkatex %} at interleaved time points, staggered in such that they leapfrog over each other [1].

An efficient HMC run requires proper tuning of its hyperparameters [1]:

  - The time discretization (step size of the leapfrog)

  - The integration time (number of leapfrog steps)

  - The precision matrix {% katex inline %}\boldsymbol{M}{% endkatex %} that parametrizes the kinetic energy.

For example, if the step size is too large then the leapfrog integrator will be inaccurate and too many proposals will be rejected. However, if it is too small we waste computation resources. If the number of steps is too small, the simulated trajectory at each iteration will be too short and sampling will fall back to random walk. But if too large the trajectory might run in circles and we again waste computation resources. If the estimated covariance (inverse of the precision matrix) is too different from the posterior covariance, the proposal momentum will be suboptimal and movement in the position space will be too large or too small in some dimension [1].

![Example of the circular leapfrog. Three different trajectories around the same 2D normal distribution. For practical sampling we want to move as far as possible from the starting point while avoiding U-turns in the trajectory. Hence, the name of one of the most popular dynamic HMC methods No U-Turn Sampling (NUTS) [1].](assets/mcmc-hmc/circular-leapfrog.png)

![Example of the funnel leapfrog. Three different trajectories around the same Neal’s funnel, a common geometry arising in (centered) hierarchical models. These trajectories fail to properly simulate following the correct distribution resulting in divergences. When the exact trajectories lie on regions of high curvature, the numerical trajectories generated can rapidly get off towards the boundaries of the distribution we are trying to explore [1].](assets/mcmc-hmc/funnel-leapfrog.png)


## References

1. Martin, Osvaldo A., Kumar, Ravin, Lao, Junpeng (2021) *Bayesian Modeling and Computation in Python*. Chapman and Hall/CRC.
2. Bishop, Christopher M., Bishop, Hugh (2023) *Deep Learning: Foundations and Concepts*. Springer Cham.
