---
title: 'Meta-Analysis: Meta-Regression'
published: true
tags: 'math, datascience, statistics, tutorial'
series: Meta-Analysis
id: 4128050
date: '2026-07-12T22:50:12Z'
---

> *Adapted from an appendix of my MS thesis.*

## Meta-Regression

Usually, regression models are based on data comprising individual persons or specimens, for which both the independent {% katex inline %}x{% endkatex %} and dependent {% katex inline %}y{% endkatex %} values are measured. In meta-regression, this concept is applied to entire studies. The variable {% katex inline %}x{% endkatex %} represents characteristics of studies, for example, the year in which it was conducted. Based on this information, a meta-regression model tries to predict {% katex inline %}y{% endkatex %}, the study’s effect size [1].

In a conventional regression, we want to estimate the value {% katex inline %}y_ i{% endkatex %} of a person or specimen {% katex inline %}i{% endkatex %} using a predictor (or covariate) {% katex inline %}x_ i{% endkatex %} with a regression coefficient {% katex inline %}\beta{% endkatex %} [1].


{% katex %}
y_ i = \beta_ 0 + \beta_ 1 x_ i.
{% endkatex %}


In meta-regression, the variable {% katex inline %}y{% endkatex %} we want to predict is the observed effect size {% katex inline %}\hat{\theta}_ k{% endkatex %} of study {% katex inline %}k{% endkatex %} [1].


{% katex %}
\hat{\theta}_ k = \theta + \beta x_ k + \epsilon_ k + \zeta_ k.
{% endkatex %}


This formula contains two extra terms, {% katex inline %}\epsilon_ k{% endkatex %} and {% katex inline %}\zeta_ k{% endkatex %}. The same terms found in the random-effects model from the equation. The first one, {% katex inline %}\epsilon_ k{% endkatex %}, is the sampling error through which the effect size of a study deviates from its true effect. The second error, {% katex inline %}\zeta_ k{% endkatex %}, denotes that even the true effect size of the study is only sampled from an overarching distribution of effect sizes. Since the meta-regression formula includes a fixed effect (the {% katex inline %}\beta{% endkatex %} coefficient) as well as a random effect ({% katex inline %}\zeta_ k{% endkatex %}), the model used in meta-regression is often called a mixed-effects model [1].

### Meta-Regression with a Categorical Predictor

Subgroup analysis (from the companion Subgroup Analysis post) is nothing else than a meta-regression with a categorical predictor, where such categorical variables can be included through dummy-coding, such as the following [1].


{% katex %}
D_ g =
\begin{cases}
0: &\text{Subgroup A} \\\\
1: &\text{Subgroup B} \\\\
\end{cases}
{% endkatex %}


To specify a subgroup analysis in the form of a meta-regression, we simply have to replace the covariate {% katex inline %}x_ k{% endkatex %} with {% katex inline %}D_ g{% endkatex %} [1].


{% katex %}
\hat{\theta}_ k = \theta + \beta D_ g + \epsilon_ k + \zeta_ k.
{% endkatex %}


![Meta-regression with a categorical predictor (subgroup analysis).](assets/ma-meta-regression/subgroup_regression.png)

### Meta-Regression with a Continuous Predictor

When people speak of a meta-regression, they usually think of models in which a continuous variable is used as the predictor. The aim of the meta-regression model is to find values of {% katex inline %}\theta{% endkatex %} and {% katex inline %}\beta{% endkatex %} which minimize the difference between the predicted effect size and the true effect size of studies. Taking into account both the sampling error {% katex inline %}\epsilon_ k{% endkatex %} and between-study heterogeneity {% katex inline %}\zeta_ k{% endkatex %}, meta-regression tried to find a model that generalizes well, not only to the observed effect sizes but to the universe of all possible studies of interest [1].

An important detail about meta-regression models is that they can be seen as an extension of the random-effects model. The random-effects model is nothing but a meta-regression without a slope term. Since it contains no slope, the random-effects model simply predicts the same value for all studies. That is, the estimate of the pooled effect size {% katex inline %}\mu{% endkatex %}, which is equivalent to the intercept [1].

![Example of a random-effects model versus a meta-regression.](assets/ma-meta-regression/regression_left.png)

![Example of a random-effects model versus a meta-regression.](assets/ma-meta-regression/regression_right.png)

In the first step, the calculation of a meta-regression therefore closely resembles the one of a random-effects meta-analysis, in that the between-study heterogeneity {% katex inline %}\tau^ 2{% endkatex %} is estimated. In the next step, the fixed weights {% katex inline %}\theta{% endkatex %} and {% katex inline %}\beta{% endkatex %} are estimated. In meta-regression, weighted least squares (WLS) is used to find the regression line that fits the data best. WLS makes sure that studies with a smaller standard error are given a higher weight [1].

If the meta-regression model fits the data well, the true effect sizes should deviate less from the regression line compared to the pooled effect {% katex inline %}\hat{\mu}{% endkatex %}. If this is the case, the predictor {% katex inline %}x{% endkatex %} explains some of the heterogeneity variance in our meta-analysis. The fit of the meta-regression model can therefore be assessed by checking how much of the heterogeneity variance it explains [1].

The predictors included in the mixed-effects model should minimize the amount of residual heterogeneity variance denoted by {% katex inline %}\hat{\tau}_ \text{MEM}^ 2{% endkatex %}. The {% katex inline %}R_ \ast^ 2{% endkatex %} index is used to quantify the percentage of variation explained by the meta-regression model. The asterisk is added to differentiate from the {% katex inline %}R^ 2{% endkatex %} index used in conventional regressions, since meta-regression deals with true effect sizes instead of observed data points [1].

{% katex inline %}R_ \ast^ 2{% endkatex %} uses the amount of residual heterogeneity variance that even the meta-regression slope cannot explain. It is put in relation to the total heterogeneity that we initially found in our random-effects model {% katex inline %}\hat{\tau}_ \text{REM}^ 2{% endkatex %}. Subtracting this fraction from 1 leaves us with the percentage of between-study heterogeneity explained by the predictor, and is expressed in the equation. We can also says that it is how much the mixed-effects model has reduced the heterogeneity variance compared to the initial random-effects pooling model, in percent [1].


{% katex %}
R_ \ast^ 2
= 1 - \frac{\hat{\tau}_ \text{MEM}^ 2}{\hat{\tau}_ \text{REM}^ 2}
= \frac{\hat{\tau}_ \text{REM}^ 2-\hat{\tau}_ \text{MEM}^ 2}{\hat{\tau}_ \text{REM}^ 2}.
{% endkatex %}


Usually, we are not only in the amount of heterogeneity explained by the regression model but also if the regression weight of our predictor {% katex inline %}x{% endkatex %} is significant. Both in conventional and meta-regression, the significance of a regression weight is commonly assessed through a Wald test. This involves calculating the test statistic {% katex inline %}z{% endkatex %}, by dividing the estimate of {% katex inline %}\beta{% endkatex %} through its standard error [1].


{% katex %}
z = \frac{\beta}{SE_ {\hat{\beta}}}.
{% endkatex %}


Under the null hypothesis that {% katex inline %}\beta=0{% endkatex %}, this {% katex inline %}z\text{-statistic}{% endkatex %} follows a standard normal distribution. This allows us to calculate a corresponding {% katex inline %}p\text{-value}{% endkatex %}. Like in normal meta-analysis models, we can also use the Knapp-Hartung adjustment, which results in a test statistic based on the {% katex inline %}t\text{-distribution}{% endkatex %} [1].


## References

1. Harrer, Mathias, Cuijpers, Pim, Furukawa Toshi A, Ebert, David D (2021) *Doing Meta-Analysis With R: A Hands-On Guide*. Chapman & Hall/CRC Press.
