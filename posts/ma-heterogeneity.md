---
title: 'Meta-Analysis: Between-Study Heterogeneity'
published: true
tags: 'math, datascience, statistics, tutorial'
series: Meta-Analysis
id: 4128051
---

> *Adapted from an appendix of my MS thesis.*

## Between-Study Heterogeneity

The extent to which true effect sizes vary within a meta-analysis is called between-study heterogeneity. For example, the random-effects model assumes that between-study heterogeneity causes the true effect sizes of studies to differ. It therefore includes an estimate of {% katex inline %}\tau^ 2{% endkatex %}, which quantifies this variance in true effects. This allows us to calculate the pooled effect, defined as the mean of the true effect size distribution [1].

High heterogeneity can be caused by the fact that there are two or more subgroups of studies in our data that have a different true effect. In extreme cases, very high heterogeneity can mean that the studies have nothing in common, and that it makes no sense to interpret the pooled effect at all. Every good meta-analysis should not only report an overall effect but also state how trustworthy this estimate is. An essential part of this is to quantify and analyze the between-study heterogeneity [1].

### Cochran’s {% katex inline %}Q{% endkatex %}

When we want to quantify between-study heterogeneity, the difficulty is to identify how much of the variation can be attributed to the sampling error, and how much to true effect size differences. Traditionally, meta-analysts have used Cochran’s {% katex inline %}Q{% endkatex %} for this purpose. Cochran’s {% katex inline %}Q{% endkatex %} is defined as a weighted sum of squares (WSS). It uses the deviation of each study’s observed effect {% katex inline %}\hat{\theta}_ k{% endkatex %} from the summary effect {% katex inline %}\hat{\theta}{% endkatex %}, weighted by the inverse of the study’s variance {% katex inline %}w_ k{% endkatex %} [1].


{% katex %}
Q = \sum_ {k=1}^ {K}w_ k(\hat{\theta}_ k-\hat{\theta})^ 2.
{% endkatex %}


The amount to which individual effects deviate from the summary effect, the residuals, is squared. Because of the weighting by {% katex inline %}w_ k{% endkatex %}, the value of {% katex inline %}Q{% endkatex %} does not only depend on how much of {% katex inline %}\hat{\theta}_ k{% endkatex %} deviates from {% katex inline %}\hat{\theta}{% endkatex %} but also on the precision of studies. If the standard error of an effect size is low (and thus the precision is high), even small deviations from the summary effect will be given a higher weight, leading to higher values of {% katex inline %}Q{% endkatex %}. The value of {% katex inline %}Q{% endkatex %} can be used to check if there is excess variation in our data, meaning more variation than can be expected from sampling error alone. If this is the case, we can assume that the rest of the variation is due to between-study heterogeneity [1].

It is assumed that {% katex inline %}Q{% endkatex %} will approximately follow a {% katex inline %}\chi^ 2{% endkatex %} distribution with {% katex inline %}K-1{% endkatex %} degrees of freedom where {% katex inline %}K{% endkatex %} is the number of studies in our meta-analysis. That is, this assumption holds if effect size differences are only caused by sampling error. Thus the mean of a {% katex inline %}\chi^ 2{% endkatex %} distribution with {% katex inline %}K-1{% endkatex %} degrees of freedom tells us the value of {% katex inline %}Q{% endkatex %} we can expect through sampling error alone [1].

Cochran’s {% katex inline %}Q{% endkatex %} can be used to test if the variation in a meta-analysis significantly exceeds the amount we would expect under the null hypothesis of no heterogeneity. Although {% katex inline %}Q{% endkatex %} is commonly used and reported in meta-analyses, it has several flaws. A practical concern is that {% katex inline %}Q{% endkatex %} increases both when the number of studies {% katex inline %}K{% endkatex %}, and when the precision (the sample size of a study) increases. Therefore, {% katex inline %}Q{% endkatex %} and whether it is significant highly depends on the size of a meta-analysis, and thus its statistical power. From this it follows that we should not only rely on the significance of a {% katex inline %}Q\text{-test}{% endkatex %} when assessing heterogeneity [1].

### Higgins & Thompson’s {% katex inline %}I^ 2{% endkatex %} Statistic

The {% katex inline %}I^ 2{% endkatex %} statistic is directly based on Cochran’s {% katex inline %}Q{% endkatex %}. It is defined as the percentage of variability in the effect sizes that is not caused by sampling error. {% katex inline %}I^ 2{% endkatex %} draws on the assumption that {% katex inline %}Q{% endkatex %} follows a {% katex inline %}\chi^ 2{% endkatex %} distribution with {% katex inline %}K-1{% endkatex %} degrees of freedom under the null hypothesis of no heterogeneity. It quantifies, in percent, how much the observed value of {% katex inline %}Q{% endkatex %} exceeds the expected {% katex inline %}Q{% endkatex %} value when there is no heterogeneity. The value of {% katex inline %}I^ 2{% endkatex %} cannot be lower than 0%, so if {% katex inline %}Q{% endkatex %} happens to be smaller than {% katex inline %}K-1{% endkatex %}, we simply use 0 instead of a negative value [1].


{% katex %}
I^ 2 = \frac{Q-(K-1)}{Q}.
{% endkatex %}


It is common to use the {% katex inline %}I^ 2{% endkatex %} statistic to report the between-study heterogeneity in meta-analyses, and the popularity of this statistic may be associated with the fact that there is a rule of thumb on how we can interpret it [1].

  - {% katex inline %}I^ 2=25\\%{% endkatex %}: low heterogeneity

  - {% katex inline %}I^ 2=50\\%{% endkatex %}: moderate heterogeneity

  - {% katex inline %}I^ 2=75\\%{% endkatex %}: substantial heterogeneity.

### The {% katex inline %}H^ 2{% endkatex %} Statistic

The {% katex inline %}H^ 2{% endkatex %} statistic is also derived from Cochran’s {% katex inline %}Q{% endkatex %}, and similar to {% katex inline %}I^ 2{% endkatex %}. It describes the ratio of the observed variation, measured by {% katex inline %}Q{% endkatex %}, and the expected variance due to sampling error. The computation of {% katex inline %}H^ 2{% endkatex %} is a little more elegant than the one of {% katex inline %}I^ 2{% endkatex %} because we do not have to artificially correct its value when {% katex inline %}Q{% endkatex %} is smaller than {% katex inline %}K-1{% endkatex %}. Values greater than one indicate the presence of between-study heterogeneity. Compared to {% katex inline %}I^ 2{% endkatex %}, it is far less common to find this statistic reported in published meta-analyses [1].


{% katex %}
H^ 2 = \frac{Q}{K-1}.
{% endkatex %}


### Heterogeneity Variance {% katex inline %}\tau^ 2{% endkatex %} & Standard Deviation {% katex inline %}\tau{% endkatex %}

As previously discussed, {% katex inline %}\tau^ 2{% endkatex %} quantifies the variance of the true effect sizes underlying our data. When we take the square root, we obtain {% katex inline %}\tau{% endkatex %}, which is the standard deviation of the true effect sizes. A great asset of {% katex inline %}\tau{% endkatex %} is that it is expressed on the same scale as the effect size metric. The value of {% katex inline %}\tau{% endkatex %} tells us something about the range of the true effect sizes. For example, we can calculate the 95% confidence interval of the true effect sizes by multiplying {% katex inline %}\tau{% endkatex %} with 1.96, and then adding and subtracting this value from the pooled effect size [1].

### Assessing Heterogeneity

Cochran’s {% katex inline %}Q{% endkatex %} and whether it is significant highly depends on the size of a meta-analysis, and thus its statistical power. We should therefore no only rely on {% katex inline %}Q{% endkatex %} when assessing between-study heterogeneity. {% katex inline %}I^ 2{% endkatex %}, on the other hand, is not sensitive to changes in the number of studies in the analysis. It is also relatively easy to interpret. It is recommended to include {% katex inline %}I^ 2{% endkatex %} with confidence intervals as a heterogeneity measure in a meta-analysis report [1].

However, despite its common use in the literature, {% katex inline %}I^ 2{% endkatex %} is not a perfect measure for heterogeneity either. It still heavily depends on the precision of the included studies. {% katex inline %}I^ 2{% endkatex %} is simply the percentage of variability not caused by sampling error {% katex inline %}\epsilon{% endkatex %}. If our studies becomes increasingly large, the sampling error tends to zero, while at the same time, {% katex inline %}I^ 2{% endkatex %} tends to 100% simply because the studies have a greater sample size. Since {% katex inline %}H^ 2{% endkatex %} behaves similarly to {% katex inline %}I^ 2{% endkatex %}, the same caveats also apply to this statistic [1].

The value of {% katex inline %}\tau^ 2{% endkatex %}, on the other hand, is sensitive to the number of studies, and their precision. Yet, it is often difficult to interpret how relevant the amount of variance {% katex inline %}\tau^ 2{% endkatex %} is from a practical standpoint. Prediction intervals (PIs) are a good way to overcome this limitation, giving us a range into which we can expect the effects of future studies to fall based on present evidence. In addition to reporting {% katex inline %}I^ 2{% endkatex %} with confidence intervals, one should also report prediction intervals in meta-analyses [1].

To calculate the 95% prediction intervals around the overall effect {% katex inline %}\hat{\mu}{% endkatex %}, we use both the estimated between-study heterogeneity variance {% katex inline %}\hat{\tau}^ 2{% endkatex %}, as well as the standard error of the pooled effect {% katex inline %}SE_ {\hat{\mu}}{% endkatex %}, to compute the standard deviation of the prediction interval {% katex inline %}SD_ \text{PI}{% endkatex %}, using a {% katex inline %}t\text{-distribution}{% endkatex %} with {% katex inline %}K-1{% endkatex %} degrees of freedom [1].


{% katex %}
\hat{\mu} \pm t_ {K-1,0.975}\sqrt{SE_ {\hat{\mu}}^ 2+\hat{\tau}^ 2} = \hat{\mu} \pm t_ {K-1,0.975}SD_ \text{PI}.
{% endkatex %}



## References

1. Harrer, Mathias, Cuijpers, Pim, Furukawa Toshi A, Ebert, David D (2021) *Doing Meta-Analysis With R: A Hands-On Guide*. Chapman & Hall/CRC Press.
