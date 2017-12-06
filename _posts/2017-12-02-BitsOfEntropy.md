---
layout: post
title: Entropy & Bits
---

All of this information can be found on Wikipedia, but this post is meant to present a summary of what is important for understanding entropy vs cross-entropy vs KL divergence.

## Information Content / Surprisal

Let $$Q(x)$$ be my personal distribution over what I think the chances are of different events happening in the world. If I’m positive some event $$x'$$ is going to happen, i.e., $$Q(x')=1$$ and you tell me that $$x'$$ just happened, then you’ve given me zero new information. I already knew that.

Example: You tell me it will be dark tonight at midnight. Me: Ok, duh. I already knew that. But if you tell me it will be light tonight at midnight. Me: What! No way! How?! Is this some crazy astronomical event or something?! Therefore, the information content that comes with observing a high probability event is low and the information content of an event with low probability is high. We will assume from now on that decreasing the probability of an event strictly decreases its information content and vice versa.

A somewhat innocuous property that we'll also assume (black holes aside) is that information content is always nonnegative.

Let's consider one more property. If two events are independent, then the information content of both events happening should just be the sum of each event's information content. Intuitively, information about one event doesn't change the amount of information contained in another independent event.

From now on, for sake of clarity, we'll use $$q=Q(x')$$ and $$p=Q(y')$$. Summarizing what we've observed so far, we see we have three properties for an information content function $$IC(q)$$:
1. $$q = 1 \Rightarrow IC(q) = 0$$
2. $$IC(q) \ge 0$$
3. $$\frac{\partial IC(z)}{\partial z} < 0$$
4. $$Q(x',y') = qp \Rightarrow IC(Q(x',y')) = IC(qp) = IC(q) + IC(p)$$

The last property is crucial to deriving the form of the function that will capture the proerpties of information content.

We'll denote the derivative of $$IC$$ evaluated at $$z$$ as $$IC'(z)$$: $$IC'(z) = \frac{\partial IC(r)}{\partial r}\vert_z$$. The first step (not obvious) is to start with property 4 and take its derivative (both sides) with respect to $$q$$.

$$\begin{align}
\frac{\partial IC(qp)}{\partial q} &= \frac{\partial}{\partial q} \{IC(q) + IC(p)\} & \\
\Rightarrow IC'(qp)p &= IC'(q)  &\text{took derivative wrt } q \\
IC''(qp)qp + IC'(qp) &= 0 &\text{took derivative wrt } p \\
IC''(z)z + IC'(z) &= 0 &\text{rename } z=qp\\
\frac{\partial}{\partial z} \{ zIC'(z) \} &= 0 &\text{recognize above as derivative of single form} \\
zIC'(z) &= \hat{K} &\text{ integrate (} \hat{K} \text{ is integration constant)} \\
IC(z) &= \hat{K} \ln(z) + C &\text{move z to right and integrate (} C \text{ is integ. con.)}\\
\end{align}$$

So now we have the functional form. Let's start considering the other properties that the function needs to satisfy.

Take property 1: $$IC(1) = C = 0$$. That was easy.

Take property 2: $$IC(z) \ge 0 \Rightarrow \hat{K} \le 0$$, so let $$K = -\hat{K} \ge 0$$.

Take property 3: $$IC'(z) = -\frac{K}{z} \le 0 \,\, \surd$$. This property is satisfied for any nonnegative $$K$$.

That's it! Our information content function is just the negative logarithm multiplied by some constant! This constant effectively changes the base of our logarithm and leads to different measurement units. We'll come to this in a moment.

## Entropy & Cross-Entropy

Let’s say $$P(x)$$ represents the true distribution over events (my $$Q(x)$$ might not be exactly correct). So if we’re walking around in the world, observing events $$x'$$, the amount of information content we would *expect* to receive at any moment is
$$\begin{align}
E_P(x)[IC(x)] = -\sum P(x) log Q(x)
\end{align}$$
which is also called *cross-entropy*. If my $$Q(x)$$ is actually correct, then my expected information content is
$$\begin{align}
E_P(x)[IC(x)] = -\sum P(x) log P(x)
\end{align}$$
which is called *entropy*.

If the base of the logarithm is 2, the units for cross-entropy and entropy are called "bits"; if the base is $$e$$, "nats", if 10, then "bans".

Why bits? How does this relate to base 2 representation of digits? Let’s assume $$Q(x)=P(x)$$, i.e., our assumption for the distribution is actually correct. Consider a boolean random variable $$X \in \{\text{True},\text{False}\}$$.

If $$P(X) = [1,0]$$ is the probability distribution over the values True and False, we don’t need any bits to convey the value of $$X$$ because the answer is always True:

$$\begin{align}
H(p) &= -P[True] \log (P[True]) - P[False] \log (P[False]) = 0
\end{align}$$

This is exactly what entropy tells us! Coincidence? Let's try again.

Let $$P(X) = [0.5,0.5]$$, then we need 1 bit to convey the value of $$X$$ because the answer could be True or False:

$$\begin{align}
H(p) &= -P[True] \log (P[True]) - P[False] \log (P[False]) = 0.5 + 0.5 = 1
\end{align}$$

Again! In general, $$\log_2 (N)$$ bits are needed to convey $$N$$ uniformly distributed events, i.e., $$\forall i$$ $$P(x_i)=1/N$$.

$$\begin{align}
H(p) &= \sum_{i=1}^N -P_i \log (P_i) = \sum_{i=1}^N -\frac{1}{N} \log (\frac{1}{N}) = \log(N)
\end{align}$$

So entropy measures the number of bits that we would expect to need in order to convey information content in a world with events distributed according to $$P(x)$$. Running with this, cross-entropy measures the number of bits we would expect to need in order to convey information content in the world distributed according to $$P(x)$$ but assuming $$Q(x)$$. If we assume $$Q(x)$$, and $$P(x)$$ is the true world, we would expect to be surprised way more often. So it would make sense that someone would need way more bits to convey information to us about what’s going on in this strange world $$P(x)$$.

## Kulllback-Liebler Divergence

The difference between these, cross-entropy & entropy, is called the *Kullback-Leibler divergence*, $$KL(P \vert Q)$$, and it measures how many more bits you need to convey a message when you are assuming $$Q(x)$$ and the real world is really given by $$P(x)$$. So this tells you how much worse $$Q(x)$$ is when you should be using $$P(x)$$. The KL divergence is used a lot in ML to measure the difference between two distributions, i.e., how much worse Q is than P at encoding a message. Technically, it is not a distance because $$KL(P \vert Q) \ne KL(Q \vert P)$$. It also doesn’t satisfy the triangle inequality. And sometimes we end up trying to minimize $$KL(Q \vert P)$$ just because $$KL(P \vert Q)$$ is impossible. If $$KL(Q \vert P) = 0$$, then $$Q=P$$ almost everywhere.
