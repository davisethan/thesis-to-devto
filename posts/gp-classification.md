---
title: Gaussian Process Classification
published: false
tags: 'machinelearning, datascience, statistics, tutorial'
series: Gaussian Processes (GP)
id: 4121260
---

> *Adapted from an appendix of my MS thesis.*

## Classification

We have considered regression problems where the targets are real valued. Classification problems aim to assign an input {% katex inline %}\boldsymbol{x}{% endkatex %} to one of {% katex inline %}C{% endkatex %} classes {% katex inline %}\mathcal{C}_ 1,\ldots,\mathcal{C}_ C{% endkatex %}. These problems can either be binary ({% katex inline %}C=2{% endkatex %}) or multiclass ({% katex inline %}C>2{% endkatex %}). Let us focus on probabilistic classification where test predictions take the form of class probabilities. Since generalization to test cases inherently involves some level of uncertainty, it is natural to attempt to make predictions in a way that reflects these uncertainties [1].

Both classification and regression can be viewed as function approximation problems. Unfortunately, the solution of classification problems using Gaussian processes is more demanding than for regression problems. This is because regression problems can assume that the likelihood function is Gaussian. A Gaussian process prior combined with a Gaussian likelihood gives rise to a posterior Gaussian process over functions and everything remains analytically tractable. For classification models where the targets are discrete class labels, the Gaussian likelihood is inappropriate, and we must use methods of approximate inference since exact inference is not feasible [1].

We have seen how Gaussian process regression (GPR) can be obtained by generalizing linear regression. Logistic regression describes an analog of linear regression in the classification case. It is generalized to yield Gaussian process classification (GPC) using again the ideas behind the generalization of linear regression for GPR [1].

For binary discriminative classification the output of a regression model can turn into a class probability using a response function (the inverse of a link function). This squashes its arguments which can lie in the domain {% katex inline %}(-\infty,\infty){% endkatex %} into the domain {% katex inline %}[0,1]{% endkatex %} guaranteeing a valid probabilistic interpretation. An example is the linear logistic regression model (see the companion logistic regression post for more information) which combines the linear model with the logistic response function [1].


{% katex %}
p(\mathcal{C}_ 1|\boldsymbol{x})=\lambda(\boldsymbol{x}^ \top\boldsymbol{w}) \quad \text{where} \quad \lambda(z)=\frac{1}{1+\exp(-z)}.
{% endkatex %}


Let us consider linear models for binary classification which form the foundation of Gaussian process classification models. We use the labels {% katex inline %}y=1{% endkatex %} and {% katex inline %}y=-1{% endkatex %} to distinguish the two classes. The likelihood is given by {% katex inline %}p(y=1|\boldsymbol{x},\boldsymbol{w}) = \sigma(\boldsymbol{x}^ \top\boldsymbol{w}){% endkatex %} where {% katex inline %}\boldsymbol{w}{% endkatex %} is the weights vector and {% katex inline %}\sigma(z){% endkatex %} can be any sigmoid function. When using the logistic {% katex inline %}\sigma(z)=\lambda(z){% endkatex %} from the equation the model is simply called logistic regression. A the probability of the two classes must sum to 1, we have {% katex inline %}p(y=-1|\boldsymbol{x},\boldsymbol{w})=1-p(y=1|\boldsymbol{x},\boldsymbol{w}){% endkatex %}. Thus for a data points {% katex inline %}(\boldsymbol{x}_ i,y_ i){% endkatex %} the likelihood is given by {% katex inline %}\sigma(\boldsymbol{x}_ i^ \top\boldsymbol{w}){% endkatex %} if {% katex inline %}y_ i=1{% endkatex %}, and {% katex inline %}1-\sigma(\boldsymbol{x}_ i^ \top\boldsymbol{w}){% endkatex %} if {% katex inline %}y_ i=-1{% endkatex %} [1].

For binary classification the basic idea behind Gaussian process prediction is that we place a GP prior over the latent function {% katex inline %}f(\boldsymbol{x}){% endkatex %} and then squash this through the logistic function to obtain a prior on {% katex inline %}\pi(\boldsymbol{x})=p(y=1|\boldsymbol{x})=\sigma(f(\boldsymbol{x})){% endkatex %}. Note that {% katex inline %}\pi{% endkatex %} is a deterministic function of {% katex inline %}f{% endkatex %}, and since {% katex inline %}f{% endkatex %} is stochastic, so if {% katex inline %}\pi{% endkatex %}. The latent function {% katex inline %}f{% endkatex %} is a nuisance function that we do not observe values of itself, and instead only observe the inputs {% katex inline %}\boldsymbol{X}{% endkatex %} and the class labels {% katex inline %}\boldsymbol{y}{% endkatex %}. We are not particularly interested in the values of {% katex inline %}f{% endkatex %}, but rather in {% katex inline %}\pi{% endkatex %}, in particular for test cases {% katex inline %}\pi(\boldsymbol{x}_ \ast){% endkatex %}. The purpose of {% katex inline %}f{% endkatex %} is solely to allow a convenient formulation of the model, and the computational goal is to integrate out {% katex inline %}f{% endkatex %} [1].

Inference is naturally divided into two steps: First we compute the distribution of the latent variable corresponding to a test case in the following where {% katex inline %}p(\boldsymbol{f}|\boldsymbol{X},\boldsymbol{y})=p(\boldsymbol{y}|\boldsymbol{f})p(\boldsymbol{f}|\boldsymbol{X})/p(\boldsymbol{y}|\boldsymbol{X}){% endkatex %} is the posterior over the latent variables [1].


{% katex %}
p(f_ \ast|\boldsymbol{X},\boldsymbol{y},\boldsymbol{x}_ \ast) = \int p(f_ \ast|\boldsymbol{X},\boldsymbol{x}_ \ast,\boldsymbol{f})p(\boldsymbol{f}|\boldsymbol{X},\boldsymbol{y})\mathrm{d}\boldsymbol{f}.
{% endkatex %}


Second we use this distribution over the latent {% katex inline %}f_ \ast{% endkatex %} to produce a probabilistic prediction [1].


{% katex %}
\bar{\pi}_ \ast = p(y_ \ast=1|\boldsymbol{X},\boldsymbol{y},\boldsymbol{x}_ \ast) = \int \sigma(f_ \ast)p(f_ \ast|\boldsymbol{X},\boldsymbol{y},\boldsymbol{x}_ \ast)\mathrm{d}f_ \ast.
{% endkatex %}


In the regression case with Gaussian likelihood, computation of predictions was straightforward as the relevant integrals were Gaussian and could be computed analytically. In classification the non-Gaussian likelihood in the equation makes the integral analytically intractable. Similarly, the equation can be analytically intractable for certain sigmoid functions. Thus we need to use approximations such as Markov chain Monte Carlo (MCMC) [1].


## References

1. Rasmussen, Carl Edward, Williams, Christopher K. I. (2005) *Gaussian Processes for Machine Learning*. The MIT Press.
