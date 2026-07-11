---
title: Bayesian Neural Networks
published: false
tags: 'machinelearning, deeplearning, datascience, tutorial'
series: Deep Neural Networks (DNN)
id: 4121664
---

> *Adapted from an appendix of my MS thesis.*

## Bayesian Neural Network

Deep neural networks (DNNs) are usually trained using a regularized maximum likelihood objective to find a single setting of parameters. However, large flexible models like neural networks can represent many functions, corresponding to different parameter settings, which fit the training data well, yet generalize in different ways. This phenomenon is known as underspecification [1].

Considering all of these different models together can lead to improved accuracy and uncertainty representation. This can be done by computing the posterior predictive distribution using Bayesian model averaging. The main challenges in applying Bayesian inference to DNNs are specifying suitable priors, and efficiently computing the posterior, which is challenging due to the large number of parameters and the large datasets [1].


{% katex %}
p(y|\boldsymbol{x},\mathcal{D}) = \int p(y|\boldsymbol{x},\boldsymbol{\theta})p(\boldsymbol{\theta}|\mathcal{D})\mathrm{d}\boldsymbol{\theta} \quad \text{where} \quad p(\boldsymbol{\theta}|\mathcal{D}) \propto p(\boldsymbol{\theta})p(\mathcal{D}|\boldsymbol{\theta}).
{% endkatex %}


Consider the generalized MLP with {% katex inline %}L-1{% endkatex %} hidden layers and a linear output as described in the companion MLP post [1].


{% katex %}
f(\boldsymbol{x};\boldsymbol{\theta}) = \boldsymbol{W}_ L(\cdots\varphi(\boldsymbol{W}_ 1\boldsymbol{x}+\boldsymbol{b}_ 1))+\boldsymbol{b}_ L.
{% endkatex %}


The most common choice of priors is to use a factored Gaussian prior [1].


{% katex %}
\boldsymbol{W}_ \ell \sim \mathcal{N}(\boldsymbol{0},\alpha_ \ell^ 2\boldsymbol{I}), \quad \boldsymbol{b}_ \ell \sim \mathcal{N}(\boldsymbol{0},\beta_ \ell^ 2\boldsymbol{I}).
{% endkatex %}


Initializing this model’s parameters at a particular random value is like sampling a point from this prior over functions. In the limit of infinitely wide neural networks, a neural network defines a Gaussian process (see the companion Gaussian process series) with a fixed kernel. Indeed, an MLP with one hidden layer, whose width goes to infinity, and which has a Gaussian prior on all the parameters, converges to a Gaussian process with a well-defined kernel. These kernels can be used in modeling non-stationary covariance structure [1].

Monte Carlo dropout (MCD) is a very simple and widely used method for approximating the Bayesian predictive distribution. Usually stochastic dropout layers are added as a form of regularization during training, and are turned off at test time. However, the idea of MCD is to also perform random sampling during testing [1].

More precisely, we drop out each hidden unit according to a {% katex inline %}\operatorname{Bernoulli}(p){% endkatex %} distribution, and repeat this procedure {% katex inline %}K{% endkatex %} times to create {% katex inline %}K{% endkatex %} distinct models. We then create an equally weighted average of the predictive distribution for each of these models as shown below. One drawback of MCD is that it is slow at test time. However, this can be overcome by distilling the model’s predictions into a deterministic student network [1].


{% katex %}
p(y|\boldsymbol{x},\mathcal{D}) \approx \frac{1}{K}\sum_ {k=1}^ {K}p(y|\boldsymbol{x},\boldsymbol{\theta}^ k).
{% endkatex %}


Another very simply approximation to the posterior is to only be Bayesian about the weights in the final layer. This is called the “Bayesian last layer” approximation. In more detail, let {% katex inline %}\boldsymbol{z}=f(\boldsymbol{x};\boldsymbol{\theta}){% endkatex %} be the predicted outputs of the model before any optional final nonlinearity. We assume this has the form {% katex inline %}\boldsymbol{z}=\boldsymbol{w}_ L^ \top\phi(\boldsymbol{x};\boldsymbol{\theta}){% endkatex %}, where {% katex inline %}\phi(\boldsymbol{x}){% endkatex %} are the features extracted by the first {% katex inline %}L-1{% endkatex %} layers. Then, we can use standard techniques, such as Markov chain Monte Carlo (described in the companion MCMC series), to compute {% katex inline %}p(\boldsymbol{w}_ L|\mathcal{D})=\mathcal{N}(\boldsymbol{\mu}_ L,\boldsymbol{\Sigma}_ L){% endkatex %}, given {% katex inline %}\phi(\cdot){% endkatex %} [1].

MCMC methods like Hamiltonian Monte Carlo (HMC) are generally considered to be the gold standard for posterior approximation, since they do not make strong assumptions about the form of the posterior. However, a significant limitation of standard MCMC procedures, including HMC, is that they require access to the full training set at each step. Stochastic gradient MCMC methods, such as Stochastic gradient Langevin dynamics (SGLD), operate instead using mini-batches of data, offering a scalable alternative [1].

Many conventional approximate inference methods, such as variational inference, focus on approximating the posterior {% katex inline %}p(\boldsymbol{\theta}|\mathcal{D}){% endkatex %} in a local neighborhood around one of the posterior modes. While this is often not a major limitation in classical machine learning, modern deep neural networks have highly multi-modal posteriors, with parameters in different modes giving rise to very different functions [1].

On the other hand, the functions in a neighborhood of a single mode may make fairly similar predictions. So using a local approximation to compute the posterior predictive will underestimate uncertainty and generalize more poorly. A simple alternative method is to train multiple models, and then to approximate the posterior using an equally weighted mixture of delta functions as follows where {% katex inline %}M{% endkatex %} is the number of models. This approach is called deep ensembles [1].


{% katex %}
p(\boldsymbol{\theta}|\mathcal{D}) \approx \frac{1}{M}\sum_ {m=1}^ {M} \delta(\boldsymbol{\theta}-\hat{\boldsymbol{\theta}}_ m).
{% endkatex %}


Once we have an approximation {% katex inline %}q(\boldsymbol{\theta}|\mathcal{D}){% endkatex %} of the parameter posterior {% katex inline %}p(\boldsymbol{\theta}|\mathcal{D}){% endkatex %}, we can use it to approximate the posterior predictive distribution [1].


{% katex %}
p(y|\boldsymbol{x},\mathcal{D})=\int p(y|\boldsymbol{x},\boldsymbol{\theta})p(\boldsymbol{\theta}|\mathcal{D})\mathrm{d}\boldsymbol{\theta}.
{% endkatex %}


We often approximate this integral using Monte Carlo where {% katex inline %}\boldsymbol{\theta}^ s \sim q(\boldsymbol{\theta}|\mathcal{D}){% endkatex %} [1].


{% katex %}
p(y|\boldsymbol{x},\mathcal{D}) \approx \frac{1}{S}\sum_ {s=1}^ {S}p(y|\boldsymbol{x},\boldsymbol{\theta}^ s).
{% endkatex %}



## References

1. Kevin P. Murphy (2023) *Probabilistic Machine Learning: Advanced Topics*. MIT Press.
