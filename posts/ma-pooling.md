---
title: "Meta-Analysis: Pooling Effect Sizes"
published: false
tags: machinelearning, datascience, statistics, tutorial
series: "Meta-Analysis"
---

> *Adapted from an appendix of my MS thesis.*

## Pooling Effect Sizes

### Fixed-Effect Model

The fixed-effect model assumes that all effect sizes stem from a single, homogeneous population. It states that all studies share the same true effect size. According to the fixed-effect model, the only reason why a study {% katex inline %}k{% endkatex %}’s observed effect size {% katex inline %}\hat{\theta}_ k{% endkatex %} deviates from {% katex inline %}\theta{% endkatex %} is because of its sampling error {% katex inline %}\epsilon_ k{% endkatex %}. This sampling error causes the observed effect to deviate from the overall, true effect. We can describe the relationship as the following [1].


{% katex %}
\hat{\theta}_ k = \theta + \epsilon_ k.
{% endkatex %}


In the formula of the fixed-effect model, the true effect size is symbolized by {% katex inline %}\theta{% endkatex %}, not {% katex inline %}\theta_ k{% endkatex %} as in the equation. Previously, we only made statements about the true effect size of one individual study {% katex inline %}k{% endkatex %}. The fixed-effect tells us that a study’s true effect size {% katex inline %}\theta_ k{% endkatex %}, and the overall, pooled effect size {% katex inline %}\theta{% endkatex %}, are identical. The formula of the fixed-effect models tells us that there is only one reason why observed effect sizes {% katex inline %}\theta_ k{% endkatex %} deviate from the true overall effect: because of the sampling error {% katex inline %}\epsilon_ k{% endkatex %}. Furthermore, all things being equal, as the sample size becomes larger, the sampling error becomes smaller [1].

If we want to calculate the pooled effect size under the fixed-effect model, we therefore simply use a weighted average of all studies. To calculate the weight {% katex inline %}w_ k{% endkatex %} for each study {% katex inline %}k{% endkatex %}, we can use the standard error, which we square to obtain the variance {% katex inline %}s_ k^ 2{% endkatex %} of each effect size. Since a lower variance indicates higher precision, the inverse of the variance is used to determine the weight of each study [1].


{% katex %}
w_ k = \frac{1}{s_ k^ 2}.
{% endkatex %}


Once we know the weights, we can calculate the weighted average, our estimate of the true pooled effect {% katex inline %}\hat{\theta}{% endkatex %}. This method is the most common approach to calculate average effects in meta-analyses. Since we use the inverse of the variance, it is often called inverse-variance weighting, or simply inverse-variance meta-analysis [1].


{% katex %}
\hat{\theta} = \frac{\sum_ {k=1}^ {K}\hat{\theta}_ kw_ k}{\sum_ {k=1}^ {K}w_ k}.
{% endkatex %}


### Random-Effects Model

The fixed-effect model assumes that all our studies are part of a homogeneous population. However, it is simply unrealistic that studies in a meta-analysis are always completely homogeneous. It is likely that we can anticipate considerable between-study heterogeneity in the true effects. The random-effects model assumes that there is not only one true effect size but a distribution of true effect sizes. The goal of the random-effects model is therefore not to estimate the one true effect size of all studies, but the mean of the distribution of true effects [1].

Similar to the fixed-effect model, the random-effects model starts by assuming that an observed effect size {% katex inline %}\hat{\theta}_ k{% endkatex %} is an estimator of the study’s true effect size {% katex inline %}\theta_ k{% endkatex %}, burdened by sampling error {% katex inline %}\epsilon_ k{% endkatex %} [1].


{% katex %}
\hat{\theta}_ k = \theta_ k + \epsilon_ k.
{% endkatex %}


The fact that we use {% katex inline %}\theta_ k{% endkatex %} instead of {% katex inline %}\theta{% endkatex %} is an important difference. The random-effects model only assumes that {% katex inline %}\theta_ k{% endkatex %} is the true effect size of one single study {% katex inline %}k{% endkatex %}. It stipulates that there is a second source of error, denoted by {% katex inline %}\zeta_ k{% endkatex %}. This second source of error is introduced by the fact that even the true effect size {% katex inline %}\theta_ k{% endkatex %} of study {% katex inline %}k{% endkatex %} is only part of an over-arching distribution of true effect sizes with mean {% katex inline %}\mu{% endkatex %} [1].


{% katex %}
\theta_ k = \mu + \zeta_ k.
{% endkatex %}


The random-effects model tells us that there is a hierarchy of two processes. The observed effect sizes of a study deviate from their true value because of the sampling error. But even the true effect sizes are only a draw from a universe of true effects, whose mean {% katex inline %}\mu{% endkatex %} we want to estimate as the pooled effect of our meta-analysis. We can express the random-effects mode in one line. This formula makes it clear that our observed effect size deviates from the pooled effect {% katex inline %}\mu{% endkatex %} because of two error terms, {% katex inline %}\zeta_ k{% endkatex %} and {% katex inline %}\epsilon_ k{% endkatex %} [1].


{% katex %}
\hat{\theta}_ k = \mu + \zeta_ k + \epsilon_ k.
{% endkatex %}


A crucial assumption of the random-effects model is that the size of {% katex inline %}\zeta_ k{% endkatex %} is independent of {% katex inline %}k{% endkatex %}. That is, the size of {% katex inline %}\zeta_ k{% endkatex %} is a product of chance, and chance alone. This is known as the exchangeability assumption of the random-effects model. All true effect sizes are assumed to be exchangeable in so far as we have nothing that could tell us how big {% katex inline %}\zeta_ k{% endkatex %} will be in some study {% katex inline %}k{% endkatex %} before seeing the data [1].

![Illustration of parameters from the random-effects model.](assets/ma-pooling/random_effects.png)

The challenge associated with the random-effects model is that we have to take the error {% katex inline %}\zeta_ k{% endkatex %} into account. To do this, we have to estimate the variance of the distribution of true effect sizes. This variance is known as {% katex inline %}\tau^ 2{% endkatex %}. Once we know the value of {% katex inline %}\tau^ 2{% endkatex %}, we can include the between-study heterogeneity when determining the inverse-variance weight of each effect size. In the random-effects model, we therefore calculate an adjusted random-effects weight {% katex inline %}w_ k^ \ast{% endkatex %} for each observation [1].


{% katex %}
w_ k^ \ast = \frac{1}{s_ k^ 2+\tau^ 2}.
{% endkatex %}


Using the adjusted random-effects weights, we then calculate the pooled effect size using the inverse variance method, just as we do using the fixed-effect model [1].


{% katex %}
\hat{\theta} = \frac{\sum_ {k=1}^ {K}\hat{\theta}_ kw_ k^ \ast}{\sum_ {k=1}^ {K}w_ K^ \ast}.
{% endkatex %}


There are several methods to estimate {% katex inline %}\tau^ 2{% endkatex %}, and it is an ongoing research question which of these estimators performs best for different kinds of data. Overall, estimators of {% katex inline %}\tau^ 2{% endkatex %} fall into two categories. Some, like the DerSimonian-Laird and Sidik-Jonkman estimator, are based on closed-form expressions. The restricted maximum likelihood, Paule-Mandel estimator, and empirical Bayes estimator find the optimal value of {% katex inline %}\tau^ 2{% endkatex %} through an iterative algorithm [1].

The Knapp-Hartung adjustments try to control for the uncertainty in our estimate of the between-study heterogeneity. While significance tests of the pooled effect usually assume a normal distribution known as Wald tests, the Knapp-Hartung method is based a {% katex inline %}t{% endkatex %}-distribution. Applying a Knapp-Hartung adjustment is usually sensible. Several studies have shown that these adjustments can reduce the chance of false positives, especially when the number of studies is small [1].


## References

1. Harrer, Mathias, Cuijpers, Pim, Furukawa Toshi A, Ebert, David D (2021) *Doing Meta-Analysis With R: A Hands-On Guide*. Chapman & Hall/CRC Press.
