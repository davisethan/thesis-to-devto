---
title: "Markov Chain Monte Carlo: Theoretical Foundations"
published: false
tags: machinelearning, datascience, statistics, tutorial
series: "Markov Chain Monte Carlo (MCMC)"
---

> *Adapted from an appendix of my MS thesis.*

# Markov Chain Monte Carlo

Almost as soon as computers were invented, they were used for simulation. Markov chain Monte Carlo (MCMC) was invested as Los Alamos, Metropolis et al (1953) simulated a liquid in equilibrium with its gas phase. Their tour de force was the realization that they did not need to simulate the exact dynamics, they only needed to simulate some Markov chain with the same equilibrium distribution. The Metropolis algorithm was widely used by chemists and physicists, but was not widely known among statisticians until after 1990. Hastings (1970) generalized the Metropolis algorithm, and simulations following his scheme are said to use the Metropolis-Hastings (MH) algorithm [1].

A special case of the MH algorithm was introduced by Geman et al (1984) discussing optimization to find the posterior mode rather than simulation. Algorithms following their scheme are said to use the Gibbs sampler. It took some time for the spatial statistics community to understand that the Gibbs sampler simulated the posterior distribution, thus enabling full Bayesian inference of all kinds. Gelfand et al (1990) made the wider Bayesian community aware of the Gibbs sampler, and then it was rapidly realized that most Bayesian inference could be done using MCMC, whereas very little could be done without MCMC. Green (1995) generalized the MH algorithm as much as it could be generalized [1].

## Theoretical Foundations

A sequence {% katex inline %}X_ 1, X_ 2, \ldots{% endkatex %} of random elements of some set is a Markov chain if the conditional distribution of {% katex inline %}X_ {n+1}{% endkatex %} given {% katex inline %}X_ 1,\ldots,X_ n{% endkatex %} depends on {% katex inline %}X_ n{% endkatex %} only. The set in which the {% katex inline %}X_ i{% endkatex %} take values is called the state space of the Markov chain. A Markov chain has stationary transition probabilities if the conditional distribution of {% katex inline %}X_ {n+1}{% endkatex %} given {% katex inline %}X_ n{% endkatex %} does not depend on {% katex inline %}n{% endkatex %}. This is the main kind of Markov chain of interest in MCMC. The joint distribution of a Markov chain is determined by the following [1].

  - The marginal distribution of {% katex inline %}X_ 1{% endkatex %} called the initial distribution, and

  - The conditional distribution of {% katex inline %}X_ {n+1}{% endkatex %} given {% katex inline %}X_ n{% endkatex %} called the transition probability distribution.

If the state space is finite or countable, written {% katex inline %}\{x_ 1,\ldots,x_ n\}{% endkatex %}, then the initial distribution can be associated with a vector {% katex inline %}\lambda=(\lambda_ 1,\ldots,\lambda_ n){% endkatex %} defined by {% katex inline %}\mathrm{P}(X_ 1=x_ i)=\lambda_ i{% endkatex %} for {% katex inline %}i=1,\ldots,n{% endkatex %}, and the transition probabilities can be associated with a matrix {% katex inline %}P{% endkatex %} having elements {% katex inline %}p_ {ij}{% endkatex %} defined by {% katex inline %}\mathrm{P}(X_ {n+1}=x_ j \mid X_ n=x_ i){% endkatex %} where {% katex inline %}i=1,\ldots,n{% endkatex %} and {% katex inline %}j=1,\ldots,n{% endkatex %}. When the state space is uncountable, we must think of the initial distribution and transition probability distribution as unconditional and conditional probability distributions [1].

A stochastic process is stationary if for every positive integer {% katex inline %}k{% endkatex %} the distribution of the {% katex inline %}k{% endkatex %}-tuple {% katex inline %}(X_ {n+1},  \ldots,  X_ {n+k}){% endkatex %} does not depend on {% katex inline %}n{% endkatex %}. An initial distribution is said to be stationary, invariant, or equilibrium for some transition probability distribution if the Markov chain specified by this initial distribution and transition probability distribution is stationary. Stationarity implies stationary transition probabilities, but not vice versa. The Metropolis-Hastings-Green (MHG) algorithm constructs a transition probability distribution that preserves a specified equilibrium distribution [1].

A transition probability distribution is reversible with respect to an initial distribution if for its Markov chain {% katex inline %}X_ 1,X_ 2,\ldots{% endkatex %}, the distribution of pairs {% katex inline %}(X_ i,X_ {i+1}){% endkatex %} is exchangeable. Reversibility implies stationarity, but not vice versa. A reversible Markov chain has the same laws running forward and backward. That is, for any {% katex inline %}i{% endkatex %} and {% katex inline %}k{% endkatex %}, the distributions {% katex inline %}(X_ {i+1},\ldots,X_ {i+k}){% endkatex %} and {% katex inline %}(X_ {i+k},\ldots,X_ {i+1}){% endkatex %} are the same. All known methods for constructing transition probabilities that preserve a specified equilibrium are special cases of the MHG algorithm, and all elementary updates from the MHG algorithm are reversible [1].

A bit of compute code that makes a pseudorandom change to its state is an update mechanism. An update mechanism is elementary if it is not made up of parts that are themselves update mechanisms preserving the specified distribution. Suppose the specified distribution (the desired stationary distribution of the MCMC sampler) has unnormalied density {% katex inline %}h{% endkatex %}. The Metropolis-Hastings update does the following [1]:

  - When the current state is {% katex inline %}x{% endkatex %}, propose a move to {% katex inline %}y{% endkatex %}, having conditional probability density given {% katex inline %}x{% endkatex %} denoted {% katex inline %}q(x, y){% endkatex %}.

  - Calculate the Hastings ratio 
{% katex %}
r(x,y) = \frac{h(y)q(y,x)}{h(x)q(x,y)}.
{% endkatex %}


  - Accept the proposed move {% katex inline %}y{% endkatex %} with probability 
{% katex %}
a(x,y) = \min(1,r(x,y)),
{% endkatex %}
 that is, the state after the update is {% katex inline %}y{% endkatex %} with probability {% katex inline %}a(x,y){% endkatex %}, and the state after the update is {% katex inline %}x{% endkatex %} with probability {% katex inline %}1-a(x,y){% endkatex %}.

For example, consider the probability density function {% katex inline %}h(x){% endkatex %} is given by {% katex inline %}h(x) = \frac{g(x)}{\int_ {-\infty}^ {\infty}g(u)du}{% endkatex %} where we cannot or do not desire to solve the integral in the denominator analytically. Therefore, the distribution is only known up to some unknown constant: {% katex inline %}h(x) \propto g(x){% endkatex %}. Notice that the ratio {% katex inline %}\frac{h(y)}{h(x)}{% endkatex %} from {% katex inline %}r(x,y){% endkatex %} does not depend on the normalizing constant. The latter term {% katex inline %}\frac{q(y,x)}{q(x,y)}{% endkatex %} corrects for biases from the proposal distribution. The special case of the Metropolis-Hastings algorithm where the proposal distribution is symmetric meaning {% katex inline %}q(y,x)=q(x,y){% endkatex %} is referred to as the Metropolis algorithm [1].

The Metropolis-Hastings update is reversible with respect to {% katex inline %}h{% endkatex %}, meaning that the transition probability that describes the update is an exact sampler of the specified distribution. If {% katex inline %}X_ n{% endkatex %} is the current state and {% katex inline %}Y_ n{% endkatex %} is the proposal, we have {% katex inline %}X_ n=X_ {n+1}{% endkatex %} whenever the proposal is rejected. The distribution of {% katex inline %}(X_ n,X_ {n+1}){% endkatex %} given rejection is exchangeable, and we must show that {% katex inline %}(X_ n,Y_ n){% endkatex %} is exchangeable given acceptance. That is, we must show that for any function {% katex inline %}f{% endkatex %} that has expectation, we can interchange the arguments of {% katex inline %}f{% endkatex %} [1].


{% katex %}
\mathbb{E}[f(X_ n,Y_ n)a(X_ n,Y_ n)] = \iint f(x,y)h(x)a(x,y)q(x,y)\mathrm{d}x\mathrm{d}y = \mathbb{E}[f(Y_ n,X_ n)a(X_ n,Y_ n)].
{% endkatex %}


This follows if we can interchange {% katex inline %}x{% endkatex %} and {% katex inline %}y{% endkatex %} in {% katex inline %}h(x)a(x,y)q(x,y){% endkatex %}. Only the set of {% katex inline %}x{% endkatex %} and {% katex inline %}y{% endkatex %} such that {% katex inline %}h(x)>0{% endkatex %}, {% katex inline %}q(x,y)>0{% endkatex %}, and {% katex inline %}a(x,y)>0{% endkatex %} contribute to the integral or sum in the discrete case. These inequalities further imply that {% katex inline %}h(y)>0{% endkatex %} and {% katex inline %}q(y,x)>0{% endkatex %}. Thus {% katex inline %}r(y,x)=\frac{1}{r(x,y)}{% endkatex %} for all {% katex inline %}x{% endkatex %} and {% katex inline %}y{% endkatex %}. Suppose that {% katex inline %}r(x,y) \leq 1{% endkatex %}, so {% katex inline %}r(x,y)=a(x,y){% endkatex %} and {% katex inline %}a(y,x)=1{% endkatex %}. Then we have the following [1].


{% katex %}
\begin{aligned}
h(x)a(x,y)q(x,y) &= h(x)r(x,y)q(x,y) \\\\
&= h(y)q(y,x) \\\\
&= h(y)a(y,x)q(y,x).\end{aligned}
{% endkatex %}


Conversely, suppose that {% katex inline %}r(x,y)>1{% endkatex %}, so {% katex inline %}a(x,y)=1{% endkatex %} and {% katex inline %}a(y,x)=r(y,x){% endkatex %}, and we have the following [1].


{% katex %}
\begin{aligned}
h(x)a(x,y)q(x,y) &= h(x)q(x,y) \\\\
&= h(y)r(y,x)q(y,x) \\\\
&= h(y)a(y,x)q(y,x).\end{aligned}
{% endkatex %}



## References

1. (2011) *Handbook of {Markov} Chain {Monte} {Carlo}*. Chapman and Hall/{CRC}.
