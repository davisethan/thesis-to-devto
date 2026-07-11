---
title: "Support Vector Machines: Soft Margins, Duality, and Kernels"
published: false
tags: machinelearning, datascience, statistics, tutorial
series: "Support Vector Machines (SVM)"
---

> *Adapted from an appendix of my MS thesis.*

## Further Reading

The traditional derivation of the margin is known as the hard margin SVM. The reason for the expression “hard” is because the formulation does not all for any violations of the margin condition. In the case where data is not linearly separable, we may wish to allow some examples to fall within the margin region, or even to be on the wrong side of the hyperplane. The model that allows for some classification errors is called the soft margin SVM [1].

The key geometric idea of the soft margin SVM is the to introduce a slack variable {% katex inline %}\xi_ n{% endkatex %} corresponding to each example-label pair {% katex inline %}(\boldsymbol{x}_ n,y_ n){% endkatex %}. We subtract the value of {% katex inline %}\xi_ n{% endkatex %} from the margin, constraining {% katex inline %}\xi_ n{% endkatex %} to be non-negative. To encourage correct classification of samples, {% katex inline %}\xi_ n{% endkatex %} is added to the optimization objective [1].

A different approach to deriving the SVM follows the principle of empirical risk minimization. This requires minimization of a chosen loss function for our binary classification task. The ideal loss function between binary labels is the count the number of mismatches between the prediction and the label. This is denoted by {% katex inline %}\mathbf{1}(f(\boldsymbol{x}_ n) \neq y_ n){% endkatex %} and is called the zero-one loss. Unfortunately, the zero-one loss results in a combinatorial optimization problem for finding the best parameters {% katex inline %}\boldsymbol{w},b{% endkatex %}, and in general these are more challenging to solve than continuous optimization problems. An equivalent reformulation of our objective allows us to use hinge loss [1].

Yet another equivalent optimization problem of the SVM is the dual view which is independent of the number of features. Instead, the number of parameters increases with the number of examples in the training set. This is useful for problems where we have more features than the number of examples in the training dataset [1].

The formulation of the dual SVM can be written such that the inner product in its objective occurs only between examples {% katex inline %}\boldsymbol{x}_ i{% endkatex %} and {% katex inline %}\boldsymbol{x}_ j{% endkatex %}. In other words, there are no inner products between the examples and the parameters. Therefore, if we consider a set of features {% katex inline %}\phi(\boldsymbol{x}_ i){% endkatex %} to represent {% katex inline %}\boldsymbol{x}_ i{% endkatex %}, the only change in the dual SVM will be to replace the inner product. This modularity, where the choice of the SVM classification method and the choice of the feature representation {% katex inline %}\phi(\boldsymbol{x}){% endkatex %} can be considered separately, provides flexibility for us to explore the two problems independently [1].

Since {% katex inline %}\phi(\boldsymbol{x}_ i){% endkatex %} could be a non-linear function, we can use the SVM (which assumes a linear classifier) to construct classifiers that are nonlinear in the examples {% katex inline %}\boldsymbol{x}_ n{% endkatex %}. This provides a second avenue, in addition to the soft margin, for users to deal with a dataset that is not linearly separable. Instead of explicitly defining a non-linear feature map {% katex inline %}\phi(\cdot){% endkatex %} and computing the results inner product between examples {% katex inline %}\boldsymbol{x}_ i{% endkatex %} and {% katex inline %}\boldsymbol{x}_ j{% endkatex %}, we can define a similarity function {% katex inline %}k(\boldsymbol{x}_ i,\boldsymbol{x}_ j){% endkatex %} between {% katex inline %}\boldsymbol{x}_ i{% endkatex %} and {% katex inline %}\boldsymbol{x}_ j{% endkatex %} [1].

![Example of different support vector classification (SVC) kernels applied to the classic Iris flower dataset [2].](assets/svm-kernels/sepals.png)

For a certain class of similarity functions, called kernels, the similarity function implicitly defines a non-linear feature map {% katex inline %}\phi(\cdot){% endkatex %}. Kernels are by definition functions {% katex inline %}k:\mathcal{X}\times\mathcal{X}\to\mathbb{R}{% endkatex %} for which there exists a Hilbert space {% katex inline %}\mathcal{H}{% endkatex %} and a feature map {% katex inline %}\phi:\mathcal{X}\to\mathcal{H}{% endkatex %} such that {% katex inline %}k(\boldsymbol{x}_ i,\boldsymbol{x}_ j)=\langle\phi(\boldsymbol{x}_ i),\phi(\boldsymbol{x}_ j)\rangle_ \mathcal{H}{% endkatex %}. There is a unique reproducing kernel Hilbert space (RKHS) associated with every kernel {% katex inline %}k{% endkatex %}. The generalization from an inner product to a kernel function is known as the kernel trick [1].


## References

1. Deisenroth, Marc Peter, Faisal, Aldo, Ong, Cheng Soon (2020) *Mathematics for Machine Learning*. Cambridge University Press.
2. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., Duchesnay, E. (2011) *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research.
