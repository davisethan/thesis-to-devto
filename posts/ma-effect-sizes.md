---
title: "Meta-Analysis: Effect Sizes"
published: false
tags: machinelearning, datascience, statistics, tutorial
series: "Meta-Analysis"
---

> *Adapted from an appendix of my MS thesis.*

## Effect Sizes

To perform a meta-analysis, we have to find an effect size which can be summarized across all studies. In particular, the selected effect size measure for a meta-analysis should comparable, computable, reliable, and interpretable. An effect size is defined as a metric quantifying the relationship between two entities. It captures the direction and magnitude of this relationship. For example, correlations describe how well we can predict the values of a variable through the values of another and so can be seen as a form of effect size [1].

In mathematical notation, it is common to use the Greek letter {% katex inline %}\theta{% endkatex %} as the symbol for a true effect size. More precisely, {% katex inline %}\theta_ k{% endkatex %} represents the true effect size of a study {% katex inline %}k{% endkatex %}. Importantly, the true effect size is not identical with the observed effect size that we find in the published results of the study. The observed effect size {% katex inline %}\hat{\theta}{% endkatex %} is only an estimate of the true effect size. The observed effect size of study {% katex inline %}k{% endkatex %} is therefore {% katex inline %}\hat{\theta}_ k{% endkatex %}. Note that {% katex inline %}\hat{\theta}_ k{% endkatex %} differs from {% katex inline %}\theta_ k{% endkatex %} because of the sampling error {% katex inline %}\epsilon_ k{% endkatex %} [1].


{% katex %}
\hat{\theta}_ k = \theta_ k + \epsilon_ k.
{% endkatex %}


We can assume that studies with smaller {% katex inline %}\epsilon{% endkatex %} will deliver a more precise estimate of the true effect size. When pooling the results of different studies, meta-analyses give studies with greater precision (less sampling error) a higher weight, because they are better estimators of the true effect. The question is how we can know how large the sampling error is [1].

Unsurprisingly, the true effect of a study {% katex inline %}\theta_ k{% endkatex %} is unknown, and so {% katex inline %}\epsilon_ k{% endkatex %} is also unknown. Often, however, we can approximate the expected sampling error. A common way to represent {% katex inline %}\epsilon{% endkatex %} is through the standard error (SE). The standard error is defined as the standard deviation of the sampling distribution. A sampling distribution is the distribution of a metric we get when we draw random samples with the same sample size {% katex inline %}n{% endkatex %} from our population many times [1].

### Within-Group Study

The arithmetic mean is probably the most commonly used central tendency measure, and can easily be pooled in a meta-analysis [1].


{% katex %}
\bar{x} = \frac{\sum_ {i=1}^ {n}x_ i}{n}.
{% endkatex %}


The standard error of the mean is calculated as the ratio of the sample standard deviation {% katex inline %}s{% endkatex %} and the square root of the sample size {% katex inline %}n{% endkatex %} [1].


{% katex %}
SE_ {\bar{x}} = \frac{s}{\sqrt{n}}.
{% endkatex %}


### Between-Group Study

The between-group mean difference {% katex inline %}MD_ {\text{between}}{% endkatex %} is defined as the raw, unstandardized difference of the means for two independent groups. Between-group mean differences can be calculated when a study contained at least two groups, as is usually the case in controlled trials or other types of experimental studies. In meta-analyses, mean differences can only be used when all the studies measured the outcome of interest on exactly the same scale. The mean difference is defined as the mean of group 1, {% katex inline %}\bar{x}_ 1{% endkatex %}, minus the mean of group 2, {% katex inline %}\bar{x}_ 2{% endkatex %} [1].


{% katex %}
MD_ {\text{between}} = \bar{x}_ 1 - \bar{x}_ 2.
{% endkatex %}


The standard error can be obtained using the following formula where {% katex inline %}n_ 1{% endkatex %} represents the sample size of group 1, {% katex inline %}n_ 2{% endkatex %} the sample size of group 2, and {% katex inline %}s_ {\text{pooled}}{% endkatex %} the pooled standard deviation of both groups [1].


{% katex %}
SE_ {MD_ \text{between}} = s_ {\text{pooled}}\sqrt{\frac{1}{n_ 1}+\frac{1}{n_ 2}}.
{% endkatex %}


Using the standard deviation of group 1, {% katex inline %}s_ 1{% endkatex %}, and group 2, {% katex inline %}s_ 2{% endkatex %}, the value of {% katex inline %}s_ \text{pooled}{% endkatex %} can be calculated as follows [1].


{% katex %}
s_ {\text{pooled}}=\sqrt{\frac{(n_ 1-1)s_ 1^ 2+(n_ 2-1)s_ 2^ 2}{(n_ 1-1)+(n_ 2-1)}}.
{% endkatex %}


### Standardized Between-Group Study

The standardized between-group mean difference {% katex inline %}SMD_ \text{between}{% endkatex %} is defined as the difference in means between two independent groups, standardized by the pooled standard deviation {% katex inline %}s_ \text{pooled}{% endkatex %}. {% katex inline %}SMD_ \text{between}{% endkatex %} can be compared between studies, even if those studies did not measure the outcome of interest using the same instruments. In the literature, the standardized mean difference is also often called Cohen’s {% katex inline %}d{% endkatex %}. In contrast to unstandardized mean differences, {% katex inline %}SMD_ \text{between}{% endkatex %} expresses the difference between two groups in units of standard deviations. This can be achieved by dividing the raw mean difference of two groups, {% katex inline %}\bar{x}_ 1{% endkatex %} and {% katex inline %}\bar{x}_ 2{% endkatex %}, through the pooled standard deviation {% katex inline %}s_ \text{pooled}{% endkatex %} of both groups [1].


{% katex %}
SMD_ \text{between}=\frac{\bar{x}_ 1-\bar{x}_ 2}{s_ \text{pooled}}.
{% endkatex %}


Standardized mean differences are often interpreted using the conventions of Cohen, however, these are rules of thumb at best. It is usually much better to interpret standardized mean differences based on their implications. For example, for many serious diseases even a very small statistical effect can still have a large impact on the population level [1].

  - {% katex inline %}SMD \approx 0.20{% endkatex %}: small effect.

  - {% katex inline %}SMD \approx 0.50{% endkatex %}: moderate effect.

  - {% katex inline %}SMD \approx 0.80{% endkatex %}: large effect.

The standardized error of {% katex inline %}SMD_ \text{between}{% endkatex %} can be calculated using this formula where {% katex inline %}n_ 1{% endkatex %} and {% katex inline %}n_ 2{% endkatex %} are the sample sizes of group 1 and group 2 [1].


{% katex %}
SE_ {SMD_ \text{between}} = \sqrt{\frac{n_ 1+n_ 2}{n_ 1n_ 2}+\frac{SMD_ \text{between}^ 2}{2(n_ 1+n_ 2)}}.
{% endkatex %}


### Effect Size Correction

The standardized mean difference has been found to have an upward bias when the sample of a study is small, especially when {% katex inline %}n\leq20{% endkatex %}. This small sample bias means that SMDs systematically overestimate the true effect size when the total sample size of a study is small, which is unfortunately often the case in practice. It is therefore sensible to correct the standardized mean differences of all included studies for small-sample bias, which produces an effect size called Hedges’ {% katex inline %}g{% endkatex %}. In this formula, {% katex inline %}n{% endkatex %} represents the total sample size of the study [1].


{% katex %}
g = SMD \times \left(1-\frac{3}{4n-9}\right).
{% endkatex %}


![Example of Hedges’ {% katex inline %}g{% endkatex %} and Cohen’s {% katex inline %}d{% endkatex %} over sample size.](assets/ma-effect-sizes/hedges_g.png)


## References

1. Harrer, Mathias, Cuijpers, Pim, Furukawa Toshi A, Ebert, David D (2021) *Doing Meta-Analysis With R: A Hands-On Guide*. Chapman & Hall/CRC Press.
