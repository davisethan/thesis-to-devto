---
id: 4121677
title: Convolutional Neural Networks
published: true
tags: 'machinelearning, deeplearning, datascience, tutorial'
series: Deep Neural Networks (DNN)
---

> *Adapted from an appendix of my MS thesis.*

## Convolutional Neural Network

The convolutional neural network (CNN) is used to apply neural networks for images. In this case, we replace matrix multiplication with a convolution operation. The basic idea is to divide the input into overlapping 2D image patches, and to compare each patch with a set of small weight matrices, or filters, which represents part of an object [1].

This can be thought of as a form of template matching. We learn these templates from data. Since the templates are small (often just {% katex inline %}3 \times 3{% endkatex %} or {% katex inline %}5 \times 5{% endkatex %}), the number of parameters needed for learning is small. Additionally, since we use convolution to do template matching, instead of matrix multiplication, the model will be translationally invariant. This is useful for tasks such as image classification, where the goal is to classify if an object is present regardless of its location [1].

The 1D convolution between two function {% katex inline %}f,g:\mathbb{R}^ D\to\mathbb{R}{% endkatex %} is defined as follows [1].


{% katex %}
\lbrack f \circledast g \rbrack(z) = \int_ {\mathbb{R}^ D}f(u)g(z-u)\mathrm{d}u.
{% endkatex %}


Now suppose we replace the functions with finite-length vectors, which we can think of as functions defined on a finite set of points. Let {% katex inline %}f{% endkatex %} be evaluated at the points {% katex inline %}\\{-L,-L+1,\ldots,0,1,\ldots,L\\}{% endkatex %} to yield the weight vector (also called a filter or kernel) {% katex inline %}w_ {-L}=f(-L){% endkatex %} up to {% katex inline %}w_ L=f(L){% endkatex %}. Now let {% katex inline %}g{% endkatex %} be evaluated at the points {% katex inline %}\\{-N,\ldots,N\\}{% endkatex %} to yield the feature vector {% katex inline %}x_ {-N}=g(-N){% endkatex %} up to {% katex inline %}x_ N=g(N){% endkatex %}. Then the equation becomes the following. We see that we flip the weight vector {% katex inline %}\boldsymbol{w}{% endkatex %}, and then drag it over the the {% katex inline %}\boldsymbol{x}{% endkatex %} vector, summing up the local windows at each point [1].


{% katex %}
\lbrack \boldsymbol{w}\circledast\boldsymbol{x} \rbrack(i) = w_ {-L}x_ {i+L}+\cdots+w_ {-1}x_ {i+1}+w_ 0x_ i+w_ 1x_ {i-1}+\cdots+w_ Lx_ {i-L}.
{% endkatex %}


When we do not flip {% katex inline %}\boldsymbol{w}{% endkatex %} first, then we get the cross correlation [1].


{% katex %}
\lbrack \boldsymbol{w}\circledast\boldsymbol{x} \rbrack(i) = w_ {-L}x_ {i-L}+\cdots+w_ {-1}x_ {i-1}+w_ 0x_ i+w_ 1x_ {i+1}+\cdots+w_ Lx_ {i+L}.
{% endkatex %}


If the weight vector is symmetric, then cross correlation and convolution are the same. In the deep learning literature, the term “convolution” is often used to mean cross correlation. We can also evaluate the weights {% katex inline %}\boldsymbol{w}{% endkatex %} on the domain {% katex inline %}\\{0,1,\ldots,L-1\\}{% endkatex %} and the features {% katex inline %}\boldsymbol{x}{% endkatex %} on the domain {% katex inline %}\\{0,1,\ldots,N-1\\}{% endkatex %}, to eliminate negative indices [1].


{% katex %}
\lbrack \boldsymbol{w}\circledast\boldsymbol{x} \rbrack(i) = \sum_ {u=0}^ {L-1}w_ ux_ {i+u}.
{% endkatex %}


![1D discrete convolution of a signal with a kernel.](assets/dnn-cnn/conv1d-diagram.png)

In 2D, the equation becomes the following where the 2D filter {% katex inline %}\boldsymbol{W}{% endkatex %} has size {% katex inline %}H \times W{% endkatex %} [1].


{% katex %}
\lbrack \boldsymbol{W}\circledast\boldsymbol{X} \rbrack(i,j) = \sum_ {u=0}^ {H-1}\sum_ {v=0}^ {W-1}w_ {u,v}x_ {i+u,j+v}.
{% endkatex %}


![2D discrete convolution of a signal with a kernel.](assets/dnn-cnn/conv2d-diagram.png)

We can think of 2D convolution as template matching, since the output at a point {% katex inline %}(i,j){% endkatex %} will be large if the corresponding image centered on {% katex inline %}(i,j){% endkatex %} is similar to {% katex inline %}\boldsymbol{W}{% endkatex %}. More generally, we can think of convolution as a form of feature detection. The resulting output {% katex inline %}\boldsymbol{Y}=\boldsymbol{W}\circledast\boldsymbol{X}{% endkatex %} is therefore called a feature map [1].

In the figure we see that convolving a {% katex inline %}3 \times 3{% endkatex %} image with a {% katex inline %}2 \times 2{% endkatex %} filter results in a {% katex inline %}2 \times 2{% endkatex %} output. This is called valid convolution, since we only apply the filter to valid parts of the input, and we do not let it slide off the ends. If we want the output to have the same size as the input, we can use zero-padding, where we add a border of zeros to the image. This is called same convolution [1].

![The first 6 of 25 convolutions with padding [2].](assets/dnn-cnn/padding-grid.png)

Since each output pixel is generated by a weighted combination of inputs in its receptive field, neighboring outputs will be very similar in value, since their inputs are overlapping. We can reduce this redundancy and speedup computation by skipping every {% katex inline %}s{% endkatex %} number of inputs. This is called strided convolution [1].

![The first 6 in 9 convolutions with padding and strides [2].](assets/dnn-cnn/strides-grid.png)

Convolution will preserve information about the location of input features, a property known as equivariance. In some cases we want to be invariant to the location. For example, when performing image classification, we may just want to know if an object of interest is present anywhere in the image. A simple way to achieve this is called max pooling, which computes the maximum over its incoming values. An alternative is to use average pooling, which replaces the maximum with the mean. A common design pattern is to create a CNN by alternating convolutional layers with max pooling layers, followed by a final linear classification layer at the end [1].

![Max pooling [3].](assets/dnn-cnn/max-pooling.png)


## References

1. Kevin P. Murphy (2022) *Probabilistic Machine Learning: An Introduction*. MIT Press.
2. Dumoulin, Vincent, Visin, Francesco (2016) *A guide to convolution arithmetic for deep learning*. ArXiv e-prints.
3. Aphex34 (2015) *Max pooling*.
