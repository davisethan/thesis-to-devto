---
title: 'Gaussian Processes: Weight-Space and Function-Space Views'
published: false
tags: 'machinelearning, datascience, statistics, tutorial'
series: Gaussian Processes (GP)
id: 4121236
---

> *Adapted from an appendix of my MS thesis.*

# Gaussian Process

The problem of machine learning (ML) is induction: We need to move from a finite training data {% katex inline %}\mathcal{D}{% endkatex %} to a function {% katex inline %}f{% endkatex %} that makes predictions for all possible input values. A common method is to restrict the class of functions considered, for example only considering linear functions of the input. Another common method is to give a prior probability to all possible functions, where higher probabilities are given to functions that we consider to be more likely, for example because they are smoother than other functions. The Gaussian process (GP) belongs to the latter approach [1].

A Gaussian process is a generalization of the Gaussian probability distribution. Whereas a probability distribution describes random variables which are scalars or vectors, a stochastic process governs the properties of functions. A function can be loosely thought of as a very long vector, each entry in the vector specifying the function value {% katex inline %}f(x){% endkatex %} at a particular input {% katex inline %}x{% endkatex %}. It turns out that if we only ask for the properties of the function at a finite number of points, then inference in the Gaussian process will give us the same answer as if we had considered all points [1].

![Example of a Gaussian process. Data points (red) are used to fit estimator functions (cyan). We see a distribution of functions [2].](assets/gp-preliminaries/gp.png)

## Preliminaries

There are two equivalent ways to interpret Gaussian processes for models. One can think of a Gaussian process as defining a distribution over functions, and inference taking place in function space: the function space view. Alternatively, the weight space view considers distributions over the weights of models. Let us consider standard linear regression as an example [1].

### Weight Space View

Say we have a training set {% katex inline %}\mathcal{D}{% endkatex %} of {% katex inline %}n{% endkatex %} observations, {% katex inline %}\mathcal{D} = \\{ (\boldsymbol{x}_ i,y_ i) \mid i=1,\ldots,n\\}{% endkatex %}, where {% katex inline %}\boldsymbol{x}{% endkatex %} denotes an input vector of dimension {% katex inline %}D{% endkatex %} and {% katex inline %}y{% endkatex %} denotes a scalar output or target. The column vector inputs for all {% katex inline %}n{% endkatex %} cases are aggregated in the {% katex inline %}D \times n{% endkatex %} design matrix {% katex inline %}\boldsymbol{X}{% endkatex %}, and the target are collected in the vector {% katex inline %}\boldsymbol{y}{% endkatex %}, so we can write {% katex inline %}\mathcal{D}=(\boldsymbol{X},\boldsymbol{y}){% endkatex %}. The standard linear regression model with Gaussian noise is written as follows where {% katex inline %}\boldsymbol{x}{% endkatex %} is the input vector, {% katex inline %}\boldsymbol{w}{% endkatex %} is a vector of weights (parameters) of the linear model, {% katex inline %}f{% endkatex %} is the function value, and {% katex inline %}y{% endkatex %} is the observed target value [1].


{% katex %}
f(\boldsymbol{x}) = \boldsymbol{x}^ \top\boldsymbol{w}, \quad y = f(\boldsymbol{x}) + \epsilon.
{% endkatex %}


Often a bias weight or offset is included, but this can be implemented by augmenting the input vector {% katex inline %}\boldsymbol{x}{% endkatex %} and weight vector {% katex inline %}\boldsymbol{w}{% endkatex %}, and so is not explicitly included in this notation. We have assumed that the observed values {% katex inline %}y{% endkatex %} differ from the function values {% katex inline %}f(\boldsymbol{x}){% endkatex %} by additive noise, and further assumed that this noise follows and independent and identically distributed (IID) Gaussian distribution with zero mean and variance {% katex inline %}\sigma_ n^ 2{% endkatex %} [1].


{% katex %}
\epsilon \sim \mathcal{N}(0, \sigma_ n^ 2).
{% endkatex %}


This gives rise to the likelihood, the probability density of the observations given the parameters, which is factored as follows by the independence assumption [1].


{% katex %}
\begin{split}
p(\boldsymbol{y}|\boldsymbol{X},\boldsymbol{w}) &= \prod_ {i=1}^ {n}p(y_ i|\boldsymbol{x}_ i,\boldsymbol{w}) \\\\
&= \prod_ {i=1}^ {n} \frac{1}{\sqrt{2\pi}\sigma_ n} \exp\left(-\frac{(y_ i-\boldsymbol{x}_ i^ \top\boldsymbol{w})^ 2}{2\sigma_ n^ 2}\right) \\\\
&= \frac{1}{(2\pi\sigma_ n^ 2)^ {n/2}} \exp\left(-\frac{1}{2\sigma_ n^ 2}\left|\boldsymbol{y}-\boldsymbol{X}^ \top\boldsymbol{w}\right|^ 2\right) \\\\
&= \mathcal{N}(\boldsymbol{X}^ \top\boldsymbol{w},\sigma_ n^ 2\boldsymbol{I}).
\end{split}
{% endkatex %}


For Bayesian formalism we specify a prior over the parameters using a zero mean Gaussian with covariance matrix {% katex inline %}\boldsymbol{\Sigma}_ p{% endkatex %} on the weights [1].


{% katex %}
\boldsymbol{w} \sim \mathcal{N}(\boldsymbol{0},\boldsymbol{\Sigma}_ p).
{% endkatex %}


Inference in the Bayesian linear model is based on the posterior distribution over the weights computed by Bayes’ rule [1].


{% katex %}
\text{posterior} = \frac{\text{likelihood}\times\text{prior}}{\text{marginal likelihood}}, \quad p(\boldsymbol{w}|\boldsymbol{y},\boldsymbol{X}) = \frac{p(\boldsymbol{y}|\boldsymbol{X},\boldsymbol{w})p(\boldsymbol{w})}{p(\boldsymbol{y}|\boldsymbol{X})}.
{% endkatex %}


The normalizing constant known as the marginal likelihood or evidence is independent of the weights and given by the following [1].


{% katex %}
p(\boldsymbol{y}|\boldsymbol{X}) = \int p(\boldsymbol{y}|\boldsymbol{X},\boldsymbol{w})p(\boldsymbol{p})\mathrm{d}\boldsymbol{w}.
{% endkatex %}


The posterior combines the likelihood and the prior capturing everything we know about the parameters, and writing only the terms from the likelihood and prior which depend on the weights we obtain the following where {% katex inline %}\boldsymbol{\bar{w}}=\sigma_ n^ {-2}(\sigma_ n^ {-2}\boldsymbol{X}\boldsymbol{X}^ \top+\boldsymbol{\Sigma}_ p^ {-1})^ {-1}\boldsymbol{X}\boldsymbol{y}{% endkatex %} [1].


{% katex %}
\begin{split}
p(\boldsymbol{w}|\boldsymbol{X},\boldsymbol{y}) &\propto \exp\left(-\frac{1}{2\sigma_ n^ 2}(\boldsymbol{y}-\boldsymbol{X}^ \top\boldsymbol{w})^ \top(\boldsymbol{y}-\boldsymbol{X}^ \top\boldsymbol{w})\right) \exp\left(-\frac{1}{2}\boldsymbol{w}^ \top\boldsymbol{\Sigma}_ p^ {-1}\boldsymbol{w}\right) \\\\
&\propto \exp\left(-\frac{1}{2}(\boldsymbol{w}-\boldsymbol{\bar{w}})^ \top(\frac{1}{\sigma_ n^ 2}\boldsymbol{X}\boldsymbol{X}^ \top+\boldsymbol{\Sigma}_ p^ {-1})(\boldsymbol{w}-\boldsymbol{\bar{w}})\right).
\end{split}
{% endkatex %}


The form of the posterior distribution is also Gaussian with mean {% katex inline %}\boldsymbol{\bar{w}}{% endkatex %} and covariance matrix {% katex inline %}\boldsymbol{A}^ {-1}{% endkatex %} where {% katex inline %}\boldsymbol{A}=\sigma_ n^ {-2}\boldsymbol{X}\boldsymbol{X}^ \top+\boldsymbol{\Sigma}_ p^ {-1}{% endkatex %} [1].


{% katex %}
p(\boldsymbol{w}|\boldsymbol{X},\boldsymbol{y}) \sim \mathcal{N}\left(\frac{1}{\sigma_ n^ 2}\boldsymbol{A}^ {-1}\boldsymbol{X}\boldsymbol{y},\boldsymbol{A}^ {-1}\right).
{% endkatex %}


To make predictions for a test case we average over all possible parameter values weighted by their posterior probability. This is in contrast to non-Bayesian schemes where a single parameter is typically chosen by some optimization criterion. Thus the predictive distribution for {% katex inline %}f_ \ast=f(\boldsymbol{x}_ \ast){% endkatex %} at {% katex inline %}\boldsymbol{x}_ \ast{% endkatex %} is given by averaging the output of all output linear models with respect to the Gaussian posterior. The predictive distribution is again Gaussian [1].


{% katex %}
\begin{split}
p(f_ \ast|\boldsymbol{x}_ \ast,\boldsymbol{X},\boldsymbol{y}) &= \int p(f_ \ast|\boldsymbol{x}_ \ast,\boldsymbol{w})p(\boldsymbol{w}|\boldsymbol{X},\boldsymbol{y})\mathrm{d}\boldsymbol{w} \\\\
&= \int \boldsymbol{x}_ \ast^ \top\boldsymbol{w}p(\boldsymbol{w}|\boldsymbol{X},\boldsymbol{y})\mathrm{d}\boldsymbol{w} \\\\
&= \mathcal{N}\left(\frac{1}{\sigma_ n^ 2}\boldsymbol{x}_ \ast^ \top\boldsymbol{A}^ {-1}\boldsymbol{X}\boldsymbol{y},\boldsymbol{x}_ \ast^ \top\boldsymbol{A}^ {-1}\boldsymbol{x}_ \ast\right).
\end{split}
{% endkatex %}


The Bayesian linear model suffers from limited expressiveness. A simple idea to overcome this problem is to first project the inputs into some high dimensional space using a set of basis functions and then apply the linear model in this space instead of directly on the inputs themselves. For example, a scalar input {% katex inline %}x{% endkatex %} could be projected into the space of powers of {% katex inline %}x{% endkatex %}: {% katex inline %}\phi(x)=(1,x,x^ 2,x^ 3,\ldots)^ \top{% endkatex %} to implement polynomial regression. This idea is also used in classification where a dataset which is not linearly separable in the original data space may become linearly separable in a high dimensional feature space [1].

We assume a given basis function {% katex inline %}\phi(\boldsymbol{x}){% endkatex %} which maps a {% katex inline %}D{% endkatex %} dimensional input vector {% katex inline %}\boldsymbol{x}{% endkatex %} into an {% katex inline %}N{% endkatex %} dimensional feature space. Further let the matrix {% katex inline %}\Phi(\boldsymbol{X}){% endkatex %} be the aggregation of columns {% katex inline %}\phi(\boldsymbol{x}){% endkatex %} for all cases in the training set. Now the model is as follows where the vector of parameters now has length {% katex inline %}N{% endkatex %} [1].


{% katex %}
f(\boldsymbol{x}) = \phi(\boldsymbol{x})^ \top\boldsymbol{w}.
{% endkatex %}


The predictive distribution becomes the following with {% katex inline %}\Phi=\Phi(\boldsymbol{X}){% endkatex %} and {% katex inline %}\boldsymbol{A}=\sigma_ n^ {-2}\Phi\Phi^ \top+\boldsymbol{\Sigma}_ p^ {-1}{% endkatex %} [1].


{% katex %}
f_ \ast|\boldsymbol{x}_ \ast,\boldsymbol{X},\boldsymbol{y} \sim \mathcal{N}\left(\frac{1}{\sigma_ n^ 2}\phi(\boldsymbol{x}_ \ast)^ \top\boldsymbol{A}^ {-1}\Phi\boldsymbol{y},\phi(\boldsymbol{x}_ \ast)^ \top\boldsymbol{A}^ {-1}\phi(\boldsymbol{x}_ \ast)\right).
{% endkatex %}


The equation can be rewritten in the following way where {% katex inline %}\phi(\boldsymbol{x}_ \ast)=\phi_ \ast{% endkatex %} and {% katex inline %}\boldsymbol{K}=\Phi^ \top\boldsymbol{\Sigma}_ p\Phi{% endkatex %} [1].


{% katex %}
\begin{split}
f_ \ast|\boldsymbol{x}_ \ast,\boldsymbol{X},\boldsymbol{y} \sim \mathcal{N}(&\phi_ \ast^ \top\boldsymbol{\Sigma}_ p\Phi(\boldsymbol{K}+\sigma_ n^ 2\boldsymbol{I})^ {-1}\boldsymbol{y},\\\\
&\phi_ \ast^ \top\boldsymbol{\Sigma}_ p\phi_ \ast-\phi_ \ast^ \top\boldsymbol{\Sigma}_ p\Phi(\boldsymbol{K}+\sigma_ n^ 2\boldsymbol{I})^ {-1}\Phi^ \top\boldsymbol{\Sigma}_ p\phi_ \ast).
\end{split}
{% endkatex %}


To make predictions using the equation we need to invert the {% katex inline %}\boldsymbol{A}{% endkatex %} matrix of size {% katex inline %}N \times N{% endkatex %} which may not be convenient if the dimension of the feature space {% katex inline %}N{% endkatex %} is large. In the equation we need to invert matrices of size {% katex inline %}n \times n{% endkatex %} which is more convenient when {% katex inline %}n < N{% endkatex %}. The feature space in the equation only appears in the form of {% katex inline %}\Phi^ \top\boldsymbol{\Sigma}_ p\Phi{% endkatex %}, {% katex inline %}\phi_ \ast^ \top\boldsymbol{\Sigma}_ p\Phi{% endkatex %}, or {% katex inline %}\phi_ \ast^ \top\boldsymbol{\Sigma}_ p\phi_ \ast{% endkatex %}. Thus the entries of these matrices are invariably of the form {% katex inline %}\phi(\boldsymbol{x})^ \top\boldsymbol{\Sigma}_ p\phi(\boldsymbol{x}'){% endkatex %} where {% katex inline %}\boldsymbol{x}{% endkatex %} and {% katex inline %}\boldsymbol{x}'{% endkatex %} are in either the training of the test sets [1].

Let us define {% katex inline %}k(\boldsymbol{x},\boldsymbol{x}') = \phi(\boldsymbol{x})^ \top\boldsymbol{\Sigma}_ p\phi(\boldsymbol{x}'){% endkatex %}. We call {% katex inline %}k(\boldsymbol{x},\boldsymbol{x}'){% endkatex %} a covariance function or kernel. Notice that {% katex inline %}\phi(\boldsymbol{x})^ \top\boldsymbol{\Sigma}_ p\phi(\boldsymbol{x}'){% endkatex %} is an inner product with respect to {% katex inline %}\boldsymbol{\Sigma}_ p{% endkatex %}. As {% katex inline %}\boldsymbol{\Sigma}_ p{% endkatex %} is positive definite we can define {% katex inline %}\boldsymbol{\Sigma}_ p^ {1/2}{% endkatex %}. Then defining {% katex inline %}\psi(\boldsymbol{x})=\boldsymbol{\Sigma}_ p^ {1/2}\phi(\boldsymbol{x}){% endkatex %} we obtain a simple dot product representation {% katex inline %}k(\boldsymbol{x},\boldsymbol{x}')=\psi(\boldsymbol{x})\psi(\boldsymbol{x}'){% endkatex %} [1].

If an algorithm is defined solely in terms of inner products in input space then it can be lifted into feature space by replacing occurrences of those inner products by {% katex inline %}k(\boldsymbol{x},\boldsymbol{x}'){% endkatex %}. This is called the kernel trick. This technique is particularly valuable in situations where it is more convenient to compute the kernel than the feature vectors themselves. This often leads to considering the kernel as the object of primary interest, and its corresponding feature space as having secondary practical importance [1].

### Function Space View

An alternative and equivalent way of reaching identical results to the weight space view is possible by considering inference directly in function space, and we can use a Gaussian process to describe a distribution over functions [1].

**Definition.** A Gaussian process is a collection of random variables, any finite number of which have a joint Gaussian distribution [1].

A Gaussian process is completely specified by its mean function and covariance function, which we define as {% katex inline %}m(\boldsymbol{x}){% endkatex %} and {% katex inline %}k(\boldsymbol{x},\boldsymbol{x}'){% endkatex %} respectively for a real process {% katex inline %}f(\boldsymbol{x}){% endkatex %} [1].


{% katex %}
\begin{split}
m(\boldsymbol{x}) &= \mathbb{E}[f(\boldsymbol{x})] \\\\
k(\boldsymbol{x},\boldsymbol{x}') &= \mathbb{E}[(f(\boldsymbol{x})-m(\boldsymbol{x}))(f(\boldsymbol{x}')-m(\boldsymbol{x}'))].
\end{split}
{% endkatex %}


We write a Gaussian process as follows [1].


{% katex %}
f(\boldsymbol{x}) \sim \mathcal{GP}(m(\boldsymbol{x}),k(\boldsymbol{x},\boldsymbol{x}')).
{% endkatex %}


A simple example of a Gaussian process can be obtained from our Bayesian linear regression model {% katex inline %}f(\boldsymbol{x})=\phi(\boldsymbol{x})^ \top\boldsymbol{w}{% endkatex %} with prior {% katex inline %}\boldsymbol{w}\sim\mathcal{N}(\boldsymbol{0},\boldsymbol{\Sigma}_ p){% endkatex %} [1].


{% katex %}
\begin{split}
\mathbb{E}[f(\boldsymbol{x})] &= \phi(\boldsymbol{x})^ \top\mathbb{E}[\boldsymbol{w}] = 0 \\\\
\mathbb{E}[f(\boldsymbol{x})f(\boldsymbol{x}')] &= \phi(\boldsymbol{x})^ \top\mathbb{E}[\boldsymbol{w}\boldsymbol{w}^ \top]\phi(\boldsymbol{x}') = \phi(\boldsymbol{x})^ \top\boldsymbol{\Sigma}_ p\phi(\boldsymbol{x}').
\end{split}
{% endkatex %}


Thus {% katex inline %}f(\boldsymbol{x}){% endkatex %} and {% katex inline %}f(\boldsymbol{x}'){% endkatex %} are jointly Gaussian with zero mean and covariance given by {% katex inline %}\phi(\boldsymbol{x})^ \top\boldsymbol{\Sigma}_ p\phi(\boldsymbol{x}'){% endkatex %}. Our running example of a covariance function will be the squared exponential (SE) covariance function. For this particular covariance function, we see that the covariance is almost unity between variables whose corresponding inputs are close, and decreases as their distance in the input space increases [1].


{% katex %}
\operatorname{cov}(f(\boldsymbol{x}_ p),f(\boldsymbol{x}_ 1)) = k(\boldsymbol{x}_ p,\boldsymbol{x}_ q) = \exp\left(-\frac{1}{2}\left|\boldsymbol{x}_ p-\boldsymbol{x}_ q\right|^ 2\right).
{% endkatex %}


The specification of the covariance function implies a distribution over functions. We can draw samples from the distribution of functions evaluated at any number of points. We choose a number of input points {% katex inline %}\boldsymbol{X}_ \ast{% endkatex %} and write the corresponding covariance matrix elementwise using the equation. Then we generate a random Gaussian vector with this covariance matrix and further can plot the generated values as a function of the inputs [1].


{% katex %}
\boldsymbol{f}_ \ast \sim \mathcal{N}(\boldsymbol{0}, K(\boldsymbol{X}_ \ast,\boldsymbol{X}_ \ast)).
{% endkatex %}


### Prediction with Noise Free Observations

We are not primarily interested in drawing random functions from the prior, but want to incorporate the knowledge that the training data provides about the function. Let us consider the simple special case where the observations are noise free. That is, we know {% katex inline %}\\{(\boldsymbol{x}_ i,f_ i)|i=1,\ldots,n\\}{% endkatex %}. The joint distribution of the training outputs {% katex inline %}\boldsymbol{f}{% endkatex %} and the test outputs {% katex inline %}\boldsymbol{f}_ \ast{% endkatex %} according to the prior are as follows [1].


{% katex %}
\begin{bmatrix}
\boldsymbol{f} \\\\
\boldsymbol{f}_ \ast
\end{bmatrix}
\sim\mathcal{N}\left(\boldsymbol{0},
\begin{bmatrix}
K(\boldsymbol{X},\boldsymbol{X}) & K(\boldsymbol{X},\boldsymbol{X}_ \ast) \\\\
K(\boldsymbol{X}_ \ast,\boldsymbol{X}) & K(\boldsymbol{X}_ \ast,\boldsymbol{X}_ \ast)
\end{bmatrix}
\right).
{% endkatex %}


If there are {% katex inline %}n{% endkatex %} training points and {% katex inline %}n_ \ast{% endkatex %} test points then {% katex inline %}K(\boldsymbol{X},\boldsymbol{X}_ \ast){% endkatex %} denotes the {% katex inline %}n \times n_ \ast{% endkatex %} matrix of covariances evaluated at all pairs of training and test points, and similarly for the other entries {% katex inline %}K(\boldsymbol{X},\boldsymbol{X}){% endkatex %}, {% katex inline %}K(\boldsymbol{X}_ \ast,\boldsymbol{X}_ \ast){% endkatex %}, and {% katex inline %}K(\boldsymbol{X}_ \ast,\boldsymbol{X}){% endkatex %}. To get the posterior distribution over functions we need to restrict this joint prior distribution to contain only those functions which agree with the observed data points [1].

Graphically we may think of generating functions from the prior, and rejecting the ones that disagree with the observations, although this strategy is computationally inefficient. Though in probabilistic terms this operation is simple, corresponding to conditioning the joint Gaussian prior distribution on the observations. In the following, function values {% katex inline %}\boldsymbol{f}_ \ast{% endkatex %} corresponding to test inputs {% katex inline %}\boldsymbol{X}_ \ast{% endkatex %} can be sampled from the joint posterior distribution by evaluating the mean and covariance matrix [1].


{% katex %}
\begin{split}
\boldsymbol{f}_ \ast|\boldsymbol{X}_ \ast,\boldsymbol{X},\boldsymbol{f}
\sim\mathcal{N}(&K(\boldsymbol{X}_ \ast,\boldsymbol{X})K(\boldsymbol{X},\boldsymbol{X})^ {-1}\boldsymbol{f},\\\\
&K(\boldsymbol{X}_ \ast,\boldsymbol{X}_ \ast)-K(\boldsymbol{X}_ \ast,\boldsymbol{X})K(\boldsymbol{X},\boldsymbol{X})^ {-1}K(\boldsymbol{X},\boldsymbol{X}_ \ast)).
\end{split}
{% endkatex %}



## References

1. Rasmussen, Carl Edward, Williams, Christopher K. I. (2005) *Gaussian Processes for Machine Learning*. The MIT Press.
2. Chris Fonnesbeck, Ana Rita Santos, Sandra Meneses (2022) *Gaussian Processes using numpy kernel*. Zenodo.
