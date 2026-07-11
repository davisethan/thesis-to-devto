---
title: 'Gaussian Processes: Covariance Functions (Kernels)'
published: true
tags: 'machinelearning, datascience, statistics, tutorial'
series: Gaussian Processes (GP)
id: 4121238
date: '2026-07-11T17:36:37Z'
---

> *Adapted from an appendix of my MS thesis.*

## Covariance Functions

A covariance function encodes our assumptions about the function which we wish to learn. In supervised learning, the notion of similarity between data points is also crucial. It is a basic assumption that points {% katex inline %}\boldsymbol{x}_ p{% endkatex %} and {% katex inline %}\boldsymbol{x}_ q{% endkatex %} that are close are likely to have a similar target value {% katex inline %}y{% endkatex %}. Under the Gaussian process view it is the covariance function that defines nearness or similarity [1].

A stationary covariance function is a function of {% katex inline %}\boldsymbol{x}-\boldsymbol{x}'{% endkatex %}. Thus it is invariant to translations in the input space. If further the covariance function is a function only of {% katex inline %}|\boldsymbol{x}-\boldsymbol{x}'|{% endkatex %} then it is called isotropic, and is thus invariant to all rigid motions. The squared exponential covariance function is isotropic. These functions are also known as radial basis functions (RBFs). Its formulation is as follows where {% katex inline %}\ell{% endkatex %} is the characteristic length scale [1].


{% katex %}
k(\boldsymbol{x},\boldsymbol{x}') = \exp\left(-\frac{|\boldsymbol{x}-\boldsymbol{x}'|^ 2}{2\ell^ 2}\right).
{% endkatex %}


Furthermore, if a covariance function depends only on {% katex inline %}\boldsymbol{x}{% endkatex %} and {% katex inline %}\boldsymbol{x}'{% endkatex %} through {% katex inline %}\boldsymbol{x}\cdot\boldsymbol{x}'{% endkatex %} it is called a dot product covariance function. The linear covariance function is a special case of the dot product covariance function. The linear covariance function is written as follows where {% katex inline %}\boldsymbol{c}{% endkatex %} is constant [1].


{% katex %}
k(\boldsymbol{x},\boldsymbol{x}') = (\boldsymbol{x}-\boldsymbol{c})(\boldsymbol{x'}-\boldsymbol{c}).
{% endkatex %}


![Example functions drawn from a GP prior with a given covariance function. (Left) The squared exponential covariance function. (Right) The linear covariance function [2].](assets/gp-covariance/exp-quad.png)

![Example functions drawn from a GP prior with a given covariance function. (Left) The squared exponential covariance function. (Right) The linear covariance function [2].](assets/gp-covariance/linear.png)

![Samples from additional covariance functions. (Top Left) The Matérn {% katex inline %}\frac{5}{2}{% endkatex %} kernel. (Top Right) The Matérn {% katex inline %}\frac{3}{2}{% endkatex %} kernel. (Bottom Left) The exponential kernel. (Bottom Right) The polynomial kernel [2].](assets/gp-covariance/matern-5-2.png)

![Samples from additional covariance functions. (Top Left) The Matérn {% katex inline %}\frac{5}{2}{% endkatex %} kernel. (Top Right) The Matérn {% katex inline %}\frac{3}{2}{% endkatex %} kernel. (Bottom Left) The exponential kernel. (Bottom Right) The polynomial kernel [2].](assets/gp-covariance/matern-3-2.png)

  

![Samples from additional covariance functions. (Top Left) The Matérn {% katex inline %}\frac{5}{2}{% endkatex %} kernel. (Top Right) The Matérn {% katex inline %}\frac{3}{2}{% endkatex %} kernel. (Bottom Left) The exponential kernel. (Bottom Right) The polynomial kernel [2].](assets/gp-covariance/exponential.png)

![Samples from additional covariance functions. (Top Left) The Matérn {% katex inline %}\frac{5}{2}{% endkatex %} kernel. (Top Right) The Matérn {% katex inline %}\frac{3}{2}{% endkatex %} kernel. (Bottom Left) The exponential kernel. (Bottom Right) The polynomial kernel [2].](assets/gp-covariance/polynomial.png)

A general name for a function {% katex inline %}k{% endkatex %} of two arguments mapping a pair of inputs {% katex inline %}\boldsymbol{x}\in\mathcal{X},\boldsymbol{x}'\in\mathcal{X}{% endkatex %} into {% katex inline %}\mathbb{R}{% endkatex %} is a kernel. A real kernel is said to be symmetric if {% katex inline %}k(\boldsymbol{x},\boldsymbol{x}')=k(\boldsymbol{x}',\boldsymbol{x}){% endkatex %}. Covariance functions must be symmetric by definition [1].


## References

1. Rasmussen, Carl Edward, Williams, Christopher K. I. (2005) *Gaussian Processes for Machine Learning*. The MIT Press.
2. Bill Engels, Oriol Abril Pla, Juan Orduz (2023) *Mean and Covariance Functions*. Zenodo.
