---
title: 'Cross-Validation: Training, Validation, and Test Splits'
published: true
tags: 'machinelearning, datascience, statistics, tutorial'
series: Model Evaluation
id: 4127182
date: '2026-07-12T17:42:41Z'
---

> *Adapted from an appendix of my MS thesis.*

# Cross-Validation

## Training Phase

Performance should not be evaluated using the same data that was used for training. Therefore, the first step is to split the data into a training set and a testing set. This should be done before starting work on the data, whether it is training an ML model or even doing simple statistics for identifying interesting features. Note that we want the output variable distribution to be approximately the same in the training and testing sets. This is called stratification [1].

The split between train and test sets is arbitrary. With the same machine learning algorithm, two different data splits will lead to two different observed performances, both of which are noisy estimates of the expected generalization performance of prediction models built with this learning procedure. A common strategy to obtain better estimates consists of performing multiple splits of the whole dataset into training and testing sets, a so-called cross-validation loop [1].

For each split of cross-validation, a model is trained using the training set, and the performances are computed using the testing set. The performances over all the testing sets are then aggregated. {% katex inline %}k\text{-fold}{% endkatex %} cross-validation consists of splitting the data into {% katex inline %}k{% endkatex %} sets called folds of approximately equal size. It ensures that each sample in the dataset is used exactly once for testing. Splitting out 10-20% for the testing set is a good trade-off, which amounts to {% katex inline %}k=5{% endkatex %} or 10 [1].

![Example of 5-fold cross-validation [1].](assets/cv-training/cross-validation.png)

Often an additional validation set is useful to make choices on the model to maximize prediction performance, such as, make changes on the architecture, tune hyperparameters, or perform early stopping. As the test set performance is our best estimate of prediction performance, we could double the test set as a validation set. However, in such a situation, the performances reported on the testing set will have an optimistic bias, since a data dependent choice has been made on this test set. There are two main solutions to this issue [1].

The first one is usually applied when the model training is fast and the dataset is of small size. It is called nested cross-validation. It consists of running two loops of cross-validation, one nested into the other. The inner loop serves for hyperparameter tuning or model selection, while the outer loop is used to evaluate the performance. Nested cross-validation should be preferred for very small datasets as it gives better testing power [1].

The second solution is to separate from the whole dataset the test set, which will only be used to evaluate the performances. Then, the remainder of the dataset can be further split into training data and data used to make modeling choices, called the validation set. The training and validation sets will be used in a cross-validation manner, and to experiment with different models and tune parameters. It is absolutely crucial that the test set is isolated at the very beginning, before any experiment is done It should be left untouched and used only at the end of the study to report the performances [1].

![Example of cross-validation with training, validation, and test sets [1].](assets/cv-training/train-validation-test.png)

Data leakage denotes cases where some information from the training set has leaked into the test set. As a consequence, the estimation of the performances is likely to be optimistic. A first basic cause of data leakage is to use the whole dataset for performing various operations on the data. A very common example is to perform feature selection using the whole dataset and then to use the selected feature for model training. A similar situation is when dimensionality reduction is performed on the whole dataset [1].


## References

1. Varoquaux, Gael, Colliot, Olivier (2023) *Evaluating Machine Learning Models and Their Diagnostic Value*. Springer US.
