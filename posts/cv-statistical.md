---
title: "Statistical Analysis"
published: false
tags: machinelearning, datascience, statistics, tutorial
series: "Model Evaluation"
---

> *Adapted from an appendix of my MS thesis.*

## Statistical Analysis

### Internal Validity

Train and test splits, cross-validation, and the like seek to estimate the expected generalization performance of a learning procedure. Keeping test data rigorously independent from algorithm development minimizes the bias of this estimation. However, there are multiple sources of arbitrary variations in these estimates. A systematic study of machine learning benchmarks shows that their most important sources of variance are as follows [1].

  - Choice of test split: A given test set is an arbitrary sample of the actual population that we are trying to generalize to. As a result, the corresponding measure of performance is an imperfect estimate of the actual expected performance. Using multiple splits, and thus multiple test sets, improves the estimation, though it makes computing confidence intervals hard [1].

  - Hyperparameter optimization: The choice of hyperparameters is imperfect, for example, because of limited resources to tune there hyperparameters. Another attempt to tune hyperparameters would lead to a slightly different choice. Thus, benchmarks do not give an absolute characterization of a learning procedure but are muddied by imperfect hyperparameters [1].

  - Random seeds: Random choices in a learning procedure, such as initial weights, random dropout for neural networks, or bootstraps in bagging, lead to uncontrolled fluctuations in benchmarking results that do not characterize the ability of the algorithm to generalize to new data [1].

With all these sources of arbitrary variance, the question is whether given benchmarks of a learning procedure performance, or improvement, is likely to generalize reliably to new data or rather to be due to benchmarking fluctuations. To answer this question, we must account for estimation error in the expected generalization performance from the different sources of uncontrolled variance in the benchmarks. A simple statistical testing procedure can be described as follows [1].

Training and testing a prediction pipeline multiple times is needed to estimate the variability of the performance measure. The simplest solution is to do this several times while varying the arbitrary factors, such as split between the train and test sets or random initialization. The resulting set of performance measures is similar to bootstrap samples and can be used to draw conclusions on the distribution of performances in a test set. Confidence intervals can be computed using percentiles of this distribution. Two learning procedures can be compared by counting the number of times that one outperforms the other. Outperforming 75% of the times is typically considered as a reliable improvement [1].

Note these procedures do not perform classic null hypothesis significance testing, which is difficult here. In particular, the standard error across the various runs should not be used instead of the standard deviation. The standard error is the standard deviation divided by the number of runs. The number of runs can be made arbitrarily large given enough compute power, thus making the standard error arbitrarily small. But in no way does the uncertainty due to the limited test data vanish [1].

Furthermore, in repeated splits or cross-validation, the runs are not independent. Specifically, it is invalid to use a standard hypothesis test, such as a {% katex inline %}t{% endkatex %}-test, across the different folds of a cross-validation. Another reason not to rely on null hypothesis testing is that their statistical significance only asserts that the expected performance, or improvement, is non-zero over a test population of infinite size. From a practical perspective, we care about meaningful improvements on tests sets of finite size, which is related to the notion of acceptance tests, as opposed to significance, in the Neyman-Pearson framework of statistical testing [1].

### External Validity

![External validation example that performs out-of-distribution (OOD) tests with generalization sets from another dataset [1].](assets/cv-statistical/study-generalization.png)

The procedures described above characterize the expected error of a learning procedure applied on a given population. A related but different question is that of characterizing the error of a given predictive model on a study population. This is related to the notion of external validity, and is important for two reasons. First, it characterizes the specific predictive model that will be used in practice. Second, characterizing the model on the target population may be important, as it may differ markedly from the study population [1].

Indeed, the techniques in the previous description rely on splitting the initial dataset into training and testing (or validation) sets. Hence, these different sets are by construction drawn from the same population and have similar characteristics. They only demonstrate the ability of the model to generalize to new but similar data. For example, to better assess model utility, guidelines on evaluating clinical prediction models insist on external validation using data collected later in time, or in a different geographical area [1].

Testing whether a prediction model can generalize to dissimilar data is important as it is all too frequent that the study sample, on which the model was developed, does not represent the target population. Participants from on study may not be representative of the target population. This can be due to inclusion/exclusion criteria or due to uncontrolled biases. To assess generalization ability, a common practice is to use one or several additional datasets for testing, these datasets being acquired using different protocols and at different sites [1].

External validation of a predictive model relies on an independent test set and not cross-validation. Statistical testing thus amounts to deriving confidence intervals or null hypothesis significance testing for the metric of interest on this test set. A general and good option, applicable to all situations, is to approximate the sampling distribution of the metric of interest by bootstrapping the test set. When comparing two classifiers, a McNemar’s test can be useful to test whether the observed difference in errors can be explained solely by sampling noise [1].


## References

1. Varoquaux, Gael, Colliot, Olivier (2023) *Evaluating Machine Learning Models and Their Diagnostic Value*. Springer US.
