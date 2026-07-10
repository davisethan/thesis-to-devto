---
title: "The Tangent Space of the SPD Manifold for EEG Classification"
published: false
tags: machinelearning, datascience, computerscience, tutorial
series: "Feature Engineering: Electroencephalogram"
---

> *Adapted from an appendix of my MS thesis. Equations render via Dev.to's KaTeX support.*

# Tangent Space

Current state-of-the-art (SOTA) machine learning (ML) for electroencephalogram (EEG) uses across channel covariance matrices and Riemannian geometric statistics on the symmetric positive definite (SPD) manifold for classification [1, 2]. These methods either discriminate directly on the SPD manifold or in the vector space that is tangent to the manifold. In this section we analyze the latter method of discrimination that performs classification in the tangent space (TS) of the SPD manifold.

## Definitions

A manifold is a collection of points that locally, but not globally, resembles Euclidean space. A Riemannian metric is defined by a smoothly varying collection of scalar products {% katex inline %}\langle \cdot,\cdot \rangle_ x{% endkatex %} in each tangent space {% katex inline %}T_ x\mathcal{M}{% endkatex %} at points {% katex inline %}x{% endkatex %} on a manifold {% katex inline %}\mathcal{M}{% endkatex %}. For example, the inner product gives a norm {% katex inline %}\|\cdot\|_ x\colon T_ x\mathcal{M}\to\mathbb{R}{% endkatex %} by {% katex inline %}\|v\|^ 2_ x=\langle v,v \rangle_ x{% endkatex %}. The shortest distance between two points on a manifold is a geodesic {% katex inline %}\gamma(t){% endkatex %}, and it is computed by integrating the norm along its curve [3].

![Example of a tangent space, manifold, and geodesic. (Left) The tangent space {% katex inline %}T_ x\mathcal{M}{% endkatex %} that is a vector space at some point {% katex inline %}x{% endkatex %} on a manifold {% katex inline %}\mathcal{M}{% endkatex %}. (Right) The curved manifold {% katex inline %}\mathcal{M}{% endkatex %} with geodesic {% katex inline %}\gamma(t){% endkatex %} from the point {% katex inline %}x{% endkatex %} to some other point {% katex inline %}y{% endkatex %} on the manifold.](assets/ts/geodesic.png)

We can map vectors in the tangent space to the manifold using geodesics. The vector {% katex inline %}v \in T_ x\mathcal{M}{% endkatex %} can be mapped to the point of the manifold that is reached after a unit time {% katex inline %}t=1{% endkatex %} by the geodesic {% katex inline %}\gamma(t){% endkatex %} starting at {% katex inline %}x{% endkatex %} with initial velocity {% katex inline %}\gamma'(0) = v{% endkatex %}. This mapping {% katex inline %}\text{Exp}_ x \colon T_ x\mathcal{M}\to\mathcal{M}{% endkatex %} is called the exponential map where {% katex inline %}\text{Exp}_ x(v)=\gamma(1){% endkatex %}. The inverse of the exponential map is the logarithmic map {% katex inline %}\text{Log}_ x(y){% endkatex %} and is the smallest vector {% katex inline %}v{% endkatex %} as measured by the Riemannian metric so that {% katex inline %}\text{Exp}_ x(v)=y{% endkatex %} [3].

In general, finding geodesics involves solving second-order ordinary differential equations (ODEs) [3]. However, SPD matrices have additional Lie group structure that can be used to simplify algorithms and speed up computations of Riemannian metrics and geodesics [4]. A group is a set {% katex inline %}G{% endkatex %} with an associative binary operation satisfying {% katex inline %}(xy)z=x(yz){% endkatex %} for all {% katex inline %}x,y,z \in G{% endkatex %}, contains an identity element {% katex inline %}e \in G{% endkatex %} so that {% katex inline %}ex=xe=x{% endkatex %} for all {% katex inline %}x \in G{% endkatex %}, and contains an inverse element {% katex inline %}x^ {-1} \in G{% endkatex %} for each {% katex inline %}x \in G{% endkatex %} where {% katex inline %}x^ {-1}x=xx^ {-1}=e{% endkatex %}. A Lie group is a smooth manifold and also a group [3].

For each {% katex inline %}x,y{% endkatex %} in a Lie group {% katex inline %}G{% endkatex %}, left-translations by {% katex inline %}y{% endkatex %} are denoted {% katex inline %}L_ y\colon x \mapsto yx{% endkatex %}. The differential {% katex inline %}(L_ y)_ \ast{% endkatex %} of left-translation maps the tangent space {% katex inline %}T_ xG{% endkatex %} to the tangent space {% katex inline %}T_ {yx}G{% endkatex %}. In particular, {% katex inline %}(L_ y)_ \ast{% endkatex %} maps any vector {% katex inline %}u \in T_ eG{% endkatex %} to the vector {% katex inline %}(L_ y)_ \ast u \in T_ yG{% endkatex %}. The vector field {% katex inline %}\tilde{u}(y) = (L_ y)_ \ast u{% endkatex %} is called left-invariant since it is invariant under left-translations {% katex inline %}\tilde{u} \circ L_ y = (L_ y)_ \ast \tilde{u}{% endkatex %} for all {% katex inline %}y \in G{% endkatex %} [3]. In other words, pullback to the identity and pushforward to another object are commutative under left-translation.


{% katex %}
\begin{aligned}
(L_ y)_ \ast\tilde{u}(x) &= (L_ y)_ \ast(L_ x)_ \ast u \\
&= (L_ {yx})_ \ast u \\
&= \tilde{u}(yx) \\
& = \tilde{u}(L_ yx) \\
&= (\tilde{u} \circ L_ y)x.

\end{aligned}
{% endkatex %}


![Commutative diagram: left-invariance of the vector field. Pullback to the identity and pushforward under left-translation commute.](assets/ts/cd-left-invariant-field.png)

The left-translation maps give a useful way of defining Riemannian metrics on Lie groups. By definition the tangent space {% katex inline %}T_ eG{% endkatex %} of a Lie group {% katex inline %}G{% endkatex %} at the identity element, typically denoted {% katex inline %}\mathfrak{g}{% endkatex %}, is called a Lie algebra. Given an inner product {% katex inline %}\langle \cdot,\cdot \rangle_ \mathfrak{g}{% endkatex %} on the Lie algebra, we can extend it to an inner product on tangent spaces at all elements of the group by setting {% katex inline %}\langle u,v \rangle_ g = \langle (L_ {g^ {-1}})_ \ast u, (L_ {g^ {-1}})_ \ast v \rangle_ \mathfrak{g}{% endkatex %}. This defines a left-invariant Riemannian metric on {% katex inline %}G{% endkatex %} since {% katex inline %}\langle (L_ h)_ \ast u, (L_ h)_ \ast v \rangle_ {hg} = \langle u,v \rangle_ g{% endkatex %} for any {% katex inline %}u,v\in T_ gG{% endkatex %} [3].


{% katex %}
\begin{aligned}
\langle (L_ h)_ \ast u, (L_ h)_ \ast v \rangle_ {hg} &= \langle (L_ {(hg)^ {-1}})_ \ast(L_ h)_ \ast u, (L_ {(hg)^ {-1}})_ \ast(L_ h)_ \ast v \rangle_ \mathfrak{g} \\
&= \langle (L_ {(hg)^ {-1}h})_ \ast u, (L_ {(hg)^ {-1}h})_ \ast v \rangle_ \mathfrak{g} \\
&= \langle (L_ {g^ {-1}h^ {-1}h})_ \ast u, (L_ {g^ {-1}h^ {-1}h})_ \ast v \rangle_ \mathfrak{g} \\
&= \langle (L_ {g^ {-1}})_ \ast u, (L_ {g^ {-1}})_ \ast v \rangle_ \mathfrak{g} \\
&= \langle u,v \rangle_ g.
\end{aligned}
{% endkatex %}


![Commutative diagram: left-invariance of the Riemannian metric induced from the inner product on the Lie algebra.](assets/ts/cd-left-invariant-metric.png)

For a matrix {% katex inline %}P\in\mathbb{R}^ {n \times n}{% endkatex %} and any non-zero vector {% katex inline %}x\in\mathbb{R}^ n{% endkatex %}, if {% katex inline %}P=P^ \top{% endkatex %} and {% katex inline %}x^ \top P x>0{% endkatex %}, then {% katex inline %}P{% endkatex %} is an SPD matrix [5]. The space of SPD matrices is a smooth manifold, and not a vector space since it lacks an additive identity, additive inverses, and zero and negative real scalar multiplication [4]. The SPD manifold {% katex inline %}\text{Sym}_ n^ +{% endkatex %} of all SPD matrices is a Lie group with matrix multiplication as its group operation [3]. Therefore, we can derive invariant metrics and geodesics on the SPD manifold.

Let {% katex inline %}A{% endkatex %} be a matrix from the general linear group {% katex inline %}\text{GL}(n){% endkatex %} of non-singular matrices. Then {% katex inline %}APA^ \top\in\text{Sym}_ n^ +{% endkatex %} since {% katex inline %}(APA^ \top)^ \top = (A^ \top)^ \top P A^ \top = APA^ \top{% endkatex %} and for any non-zero vector {% katex inline %}x\in\mathbb{R}^ n{% endkatex %} then {% katex inline %}x^ \top(APA^ \top)x = (x^ \top A)P(A^ \top x) = (A^ \top x)^ \top P (A^ \top x) > 0{% endkatex %}. Given two matrices {% katex inline %}P,Q\in\text{Sym}_ n^ +{% endkatex %} we can derive the distance between them as a norm from the identity by choosing {% katex inline %}A=P^ {-1/2}{% endkatex %} [4]. That is, with left-invariance we can pullback to the identity before pushforward.


{% katex %}
\text{dist}(P,Q) = \text{dist}(\text{Id},P^ {-1/2}QP^ {-1/2}) = N(P^ {-1/2}QP^ {-1/2}).
{% endkatex %}


By left-invariance at the identity of a Lie group we have the vector field {% katex inline %}\tilde{u}(x)=(L_ x)_ \ast u{% endkatex %}. The geodesic starting at the identity {% katex inline %}e{% endkatex %} with initial velocity {% katex inline %}u{% endkatex %} satisfies {% katex inline %}x(0)=e{% endkatex %} and {% katex inline %}x'(t)=\tilde{u}(x(t)){% endkatex %}. For matrix groups, this ODE becomes {% katex inline %}x'(t)=x(t)u{% endkatex %} and is uniquely solved by the matrix exponential {% katex inline %}x(t)=\text{exp}(tu){% endkatex %}. In other words, the exponential map is the matrix exponential and its inverse the logarithmic map is the matrix logarithm [3].

![The exponential map {% katex inline %}\text{Exp}_ x(v)=\gamma(1)=y{% endkatex %} produces the point on the manifold {% katex inline %}\mathcal{M}{% endkatex %} reached after a unit time {% katex inline %}t=1{% endkatex %} along the geodesic {% katex inline %}\gamma(t){% endkatex %} starting at point {% katex inline %}x{% endkatex %} with initial velocity {% katex inline %}\gamma'(0)=v{% endkatex %}. The logarithmic map {% katex inline %}\text{Log}_ x(y)=v{% endkatex %} is its inverse and produces the initial velocity needed to reach {% katex inline %}y{% endkatex %} from {% katex inline %}x{% endkatex %} after the unit time {% katex inline %}t=1{% endkatex %}. On {% katex inline %}\text{Sym}_ n^ +{% endkatex %} the exponential map is the matrix exponential and the logarithmic map is the matrix logarithm.](assets/ts/ode.png)

From the figure take {% katex inline %}R=P^ {-1/2}QP^ {-1/2}{% endkatex %}. The matrix logarithm {% katex inline %}\log(R){% endkatex %} produces the vector for the norm {% katex inline %}N(R){% endkatex %}. This norm is given by the Frobenius norm {% katex inline %}\|\cdot\|_ F{% endkatex %}. Furthermore, since {% katex inline %}R{% endkatex %} is SPD, it has eigendecomposition {% katex inline %}R=V \Lambda V^ \top{% endkatex %} where {% katex inline %}\Lambda=\text{diag}(\lambda_ 1,\ldots,\lambda_ n){% endkatex %} and {% katex inline %}\lambda_ i>0{% endkatex %}. By the matrix logarithm {% katex inline %}\log(R)= V\text{diag}(\log\lambda_ 1,\ldots,\log\lambda_ n)V^ \top{% endkatex %}. Therefore, by the orthogonal invariance of the Frobenius norm, the norm {% katex inline %}N(R){% endkatex %} can be written as the square root of the sum of squared eigenvalue logarithms [4].


{% katex %}
\text{dist}(P,Q) = N(P^ {-1/2}QP^ {-1/2}) = \| \log(R) \|_ F = \left( \sum_ {i=1}^ n \log^ 2\lambda_ i\right)^ {1/2}.
{% endkatex %}


the figure gives a closed form solution for the distance between two SPD matrices on {% katex inline %}\text{Sym}_ n^ +{% endkatex %}. Not only is it exact and so does not require optimization, but it can be computed in the vector space of the tangent space and so does not require integration on the curve. Furthermore, by the nature of logarithms we see that matrices with zero or negative eigenvalue are in fact infinite distance from SPD matrices on {% katex inline %}\text{Sym}_ n^ +{% endkatex %}, contrary to Euclidean space and metrics [4].

We can also find closed form solutions for the logarithmic and exponential maps on {% katex inline %}\text{Sym}_ n^ +{% endkatex %}. Rather than solve for the norm of the logarithmic map, we can solve for the vector itself. This is done by pushing forward to {% katex inline %}P{% endkatex %} after we pulled back to the identity from {% katex inline %}P{% endkatex %}. Furthermore, as the inverse of the logarithmic map, the closed form solution for the exponential map takes a vector as input and outputs the point on {% katex inline %}\text{Sym}_ n^ +{% endkatex %} reached after unit time elapsed along the geodesic.


{% katex %}
\text{Log}_ P(Q) = P^ {1/2}\log(P^ {-1/2}QP^ {-1/2})P^ {1/2}.
{% endkatex %}



{% katex %}
\text{Exp}_ P(W) = P^ {1/2}\exp(P^ {-1/2}WP^ {-1/2})P^ {1/2}.
{% endkatex %}


At the foundation of statistics is the notion of a distance. The closed form solution of the mean in Euclidean space {% katex inline %}\frac{1}{N}\sum_ {i=1}^ N X_ i{% endkatex %} relies on the additive structure of vector space and does not generalize to Riemannian space. However, there are defining properties of the mean that do generalize: The geometric mean is a least-squares centroid that minimizes the sum-of-squared distances. A natural strategy for computing the geometric mean is gradient descent optimization [6].


{% katex %}
\bar{y} = \operatorname*{arg\,min}_ {y\in\mathcal{M}}\sum_ {i=1}^ N \text{dist}(y,y_ i)^ 2.
{% endkatex %}


The exponential and logarithmic map, distance, and mean on {% katex inline %}\text{Sym}_ n^ +{% endkatex %} are common Riemannian geometric statistics used by SOTA ML for EEG that takes across channel sample covariance matrices for classification [1, 2]. The minimum distance to the mean (MDM) classifier is trained by memorizing the mean of each class and is tested by predicting classes based on the minimum distance to the memorized means [1]. All operations occur on the SPD manifold. In the next section we describe in more detail an alternative algorithm that performs classification in the tangent space of {% katex inline %}\text{Sym}_ n^ +{% endkatex %}.

## Example

Consider two three-dimensional tensors of EEG recordings {% katex inline %}X_ 1,X_ 2\in\mathbb{R}^ {p \times q \times r}{% endkatex %} from separate classes where the dimensions {% katex inline %}p,q,r{% endkatex %} are the trials, channels, and time, respectively. For each trial, let sample covariance matrices (SCMs) be computed between channels across time so that {% katex inline %}\Sigma_ 1^ {(k)},\Sigma_ 2^ {(k)}\in\mathbb{R}^ {q \times q}{% endkatex %} for {% katex inline %}k=1,\ldots,p{% endkatex %}. Assume each SCM is conditioned so that it is SPD. Furthermore, let us define {% katex inline %}\bar{\Sigma}_ 1,\bar{\Sigma}_ 2\in\mathbb{R}^ {q \times q}{% endkatex %} as geometric mean SCMs averaged across all trials {% katex inline %}k{% endkatex %} of each class.

![Example of our data preprocessing pipeline. (Left) We receive a three-dimensional tensor ({% katex inline %}\text{trials}\times\text{channels}\times\text{time}{% endkatex %}) of raw EEG signals recorded from a brain-computer interface session. (Center) We transform each trial of signals into between channel sample covariance matrices (SCMs). (Right) We represent SCMs on the SPD manifold where they are naturally clustered by their label and the golden star is the geometric mean whose tangent space we map all SCMs to for ML in vector space.](assets/ts/pipeline.png)

With the geometric mean of each class {% katex inline %}\bar{\Sigma}_ 1,\bar{\Sigma}_ 2\in\text{Sym}_ n^ +{% endkatex %} we define {% katex inline %}\bar{\Sigma}\in\text{Sym}_ n^ +{% endkatex %} as the geometric mean of these means. Then, using the logarithmic map we find the vectors between all points in all clusters to {% katex inline %}\bar{\Sigma}{% endkatex %}. We represent these vectors in the tangent space {% katex inline %}T_ {\bar{\Sigma}}\text{Sym}_ n^ +{% endkatex %} of the mean point {% katex inline %}\bar{\Sigma}{% endkatex %}. This linearization of SPD matrices is done in a way that respects the metric space of {% katex inline %}\text{Sym}_ n^ +{% endkatex %}. Once in the tangent space {% katex inline %}T_ {\bar{\Sigma}}\text{Sym}_ n^ +{% endkatex %} we can train standard ML algorithms that are optimized for vector space.

![Example of our data preprocessing and classification pipeline. (Left) All SPD matrices are vectorized by the logarithmic map. (Center) The vectorized SPD matrices in tangent space. (Right) A learned decision boundary from a standard ML alorithm.](assets/ts/tangent_space.png)

Once in the tangent space {% katex inline %}T_ {\bar{\Sigma}}\text{Sym}_ n^ +{% endkatex %} we can train standard ML algorithms that are optimized for vector space. This method of linearization from the space of SPD matrices to vector space is the standard used by software libraries like PyRiemann [7]. As of now, SOTA EEG classifiers are those that learn and predict in the tangent space of the SPD manifold rather than on the manifold itself [1, 2]. An explanation for this is that machine learning is traditionally optimized for vector space.


## References

1. Barachant, Alexandre, Bonnet, Stéphane, Congedo, Marco, Jutten, Christian (2012) *Multiclass Brain–Computer Interface Classification by Riemannian Geometry*. IEEE Transactions on Biomedical Engineering.
2. Sylvain Chevallier, Emmanuel K. Kalunga, Quentin Barthélemy, Florian Yger (2018) *Riemannian Classification for SSVEP-Based BCI: Offline versus Online Implementations*. CRC Press.
3. Stefan Sommer, Tom Fletcher, Xavier Pennec (2020) *Introduction to differential and Riemannian geometry*. Academic Press.
4. Xavier Pennec (2020) *Manifold-valued image processing with SPD matrices*. Academic Press.
5. Kevin P. Murphy (2022) *Probabilistic Machine Learning: An Introduction*. MIT Press.
6. Tom Fletcher (2020) *Statistics on manifolds*. Academic Press.
7. Alexandre Barachant, Quentin Barthélemy, Jean-Rémi King, Alexandre Gramfort, Sylvain Chevallier, Pedro L. C. Rodrigues, Emanuele Olivetti, Vladislav Goncharenko, Gabriel Wagner vom Berg, Ghiles Reguig, Arthur Lebeurrier, Erik Bjäreholt, Maria Sayu Yamamoto, Pierre Clisson, Marie-Constance Corsi, Igor Carrara, Apolline Mellot, Bruna Junqueira Lopes, Brent Gaisford, Ammar Mian, Anton Andreev, Gregoire Cattan, Arthur Lebeurrier (2025) *pyRiemann*. Zenodo.
