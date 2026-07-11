---
title: "Linear Discriminant Analysis (LDA): Decision Boundaries"
published: false
tags: machinelearning, datascience, statistics, tutorial
---

> *Adapted from an appendix of my MS thesis.*

# Linear Discriminant Analysis

## Decision Boundary Derivation

Decision theory for classification tells us that we need to know the class posteriors {% katex inline %}P(G|X){% endkatex %} for optimal classification. Suppose {% katex inline %}f_ k(x){% endkatex %} is the conditional density of {% katex inline %}X{% endkatex %} for class {% katex inline %}G=k{% endkatex %}, and let {% katex inline %}\pi_ k{% endkatex %} be the prior probability of class {% katex inline %}k{% endkatex %}, with {% katex inline %}\sum_ {\ell=1}^ {K}\pi_ \ell=1{% endkatex %}. Bayes theorem gives us the following [1].


{% katex %}
P(G=k|X=x) = \frac{f_ k(x)\pi_ k}{\sum_ {\ell=1}^ {K}f_ \ell(x)\pi_ \ell}.
{% endkatex %}


Many machine learning techniques are based on models for the class densities. For example, linear and quadratic discriminant analysis use Gaussian densities. More flexible Gaussian mixture models (GMMs) allow for nonlinear decision boundaries. General nonparametric density estimates for each class density allow the most flexibility. Naive Bayes models are a variant of the previous case, and assume that the inputs are conditionally independent in each class [1].

Suppose that each class density is modeled as a multivariate Gaussian [1].


{% katex %}
f_ k(x) = (2\pi)^ {-p/2}\lvert\boldsymbol{\Sigma}_ k\rvert^ {-1/2}\exp\left(-\frac{1}{2}(x-\mu_ k)^ \top\boldsymbol{\Sigma}_ k^ {-1}(x-\mu_ k)\right).
{% endkatex %}


Linear discriminant analysis (LDA) is the special case when we assume that the classes have a common covariance matrix {% katex inline %}\boldsymbol{\Sigma}_ k=\boldsymbol{\Sigma} \forall k{% endkatex %}. When we compare the log-ratio of two classes {% katex inline %}k{% endkatex %} and {% katex inline %}\ell{% endkatex %} we get an equation linear in {% katex inline %}x{% endkatex %}. The equal covariance matrices cause the normalization factors to cancel, as well as the quadratic part in the exponents. This linear log-odds function implies that the decision boundary between classes {% katex inline %}k{% endkatex %} and {% katex inline %}\ell{% endkatex %} is linear in {% katex inline %}x{% endkatex %} [1].


{% katex %}
\begin{split}
\log\frac{P(G=k|X=x)}{P(G=\ell|X=x)} = &\log\frac{f_ k(x)}{f_ \ell(x)}+\log\frac{\pi_ k}{\pi_ \ell} \\\\
= &\log\frac{\pi_ k}{\pi_ \ell} - \frac{1}{2}(\mu_ k+\mu_ \ell)^ \top\boldsymbol{\Sigma}^ {-1}(\mu_ k-\mu_ \ell) \\\\
&+ x^ \top\boldsymbol{\Sigma}^ {-1}(\mu_ k-\mu_ \ell).
\end{split}
{% endkatex %}


The linear discriminant functions are an equivalent description of the decision rule, with {% katex inline %}G(x)=\operatorname{argmax}_ k\delta_ k(x){% endkatex %} [1].


{% katex %}
\delta_ k(x) = x^ \top\boldsymbol{\Sigma}^ {-1}\mu_ k - \frac{1}{2}\mu_ k^ \top\boldsymbol{\Sigma}^ {-1}\mu_ k + \log\pi_ k.
{% endkatex %}


In practice we do not know the parameters of the Gaussian distributions, and need to estimate them using training data [1].

  - {% katex inline %}\hat{\pi}_ k=N_ k/N{% endkatex %}, where {% katex inline %}N_ k{% endkatex %} is the number of observations from class {% katex inline %}k{% endkatex %},

  - {% katex inline %}\hat{\mu}_ k=\sum_ {g_ i=k}x_ i/N_ k{% endkatex %},

  - {% katex inline %}\hat{\boldsymbol{\Sigma}}=\sum_ {k=1}^ {K}\sum_ {g_ i=k}(x_ i-\hat{\mu}_ k)(x_ i-\hat{\mu}_ k)^ \top/(N-K){% endkatex %}.

In the general discriminant problem, if the {% katex inline %}\boldsymbol{\Sigma}_ k{% endkatex %} are not assumed to be equal, then the convenient cancellations in the equation do not take place. In particular the pieces quadratic in {% katex inline %}x{% endkatex %} remain. We then get quadratic discriminant analysis (QDA). The decision boundary between each pair of classes {% katex inline %}k{% endkatex %} and {% katex inline %}\ell{% endkatex %} is described by a quadratic equation {% katex inline %}\{x:\delta_ k(x)=\delta_ \ell(x)\}{% endkatex %} [1].


{% katex %}
\delta_ k(x)= -\frac{1}{2}\log\lvert\boldsymbol{\Sigma}_ k\rvert - \frac{1}{2}(x-\mu_ k)^ \top\boldsymbol{\Sigma}_ k^ {-1}(x-\mu_ k) + \log\pi_ k.
{% endkatex %}


Both LDA and QDA perform well on an amazingly large and diverse set of classification tasks. The question is why LDA and QDA have such a good track record. The reason is likely not that the data are approximately Gaussian, and in addition for LDA that the covariances are approximately equal. More likely the reason is that the data can only support simple decision boundaries such as linear or quadratic, and the estimates provided by the Gaussian models are stable. This is a bias variance tradeoff where we put up with the bias of a linear decision boundary because it can be estimated with much lower variance than more exotic alternatives [1].

![Example of LDA and QDA decision boundaries from a toy dataset.](assets/lda/lda.png)

![Example of LDA and QDA decision boundaries from a toy dataset.](assets/lda/qda.png)


## References

1. Trevor Hastie, Robert Tibshirani, Jerome Friedman (2009) *The Elements of Statistical Learning*. Springer New York.
