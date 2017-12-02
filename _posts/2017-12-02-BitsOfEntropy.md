---
layout: post
title: Entropy & Bits
---

Information Content / Surprisal: Let $$Q(x)$$ be my distribution over what I think the chances are of things happening in the world. If I’m positive something is going to happen $$Q(x)=1$$ and you tell me that it just happened, then you’ve given me zero information.

Example: You tell me it will be dark tonight at midnight. Me: Ok, duh. I already knew that. But if you tell me it will be light tonight at midnight. Me: What! No way! How?! Is this some crazy astronomical event or something?! Therefore, the information content that comes with observing a high probability event is low and the information content of an event with low probability is high. The logarithm has this property:
$$IC(x) = -\log(Q[x])$$ * can use any base

Let’s say $$P(x)$$ represents the true distribution over events (my $$Q(x)$$ might not be exactly correct). So if we’re walking around in the world, observing events $$x_i$$, the amount of information content we would EXPECT to receive at any moment is $$E_P(x)[IC(x)] = -sum P(x) log Q(x)$$ which is also called \emph{cross-entropy}. If my $$Q(x)$$ is actually correct, then my expected information content is $$E_P(x)[IC(x)] = -sum P(x) log P(x)$$ which is called \emph{entropy}.
If the base of the logarithm is 2, the units for cross-entropy and entropy are called ``bits''; if the base is $$e$$, ``nats'', if 10, then ``bans''.

Why bits? How does this relate to base 2 representation of digits? Let’s assume $$Q(x)=P(x)$$, i.e., our assumption for the distribution is actually correct.
X = [True,False]
$$P[X] = [1,0] \rightarrow$ we don’t need any bits to convey value of $x$ because the answer is always True:
$$\begin{align}
H(p) &= -P[True]log(P[True]) - P[False]log(P[False]) = 0
\end{align}$$

$$P[X] = [0.5,0.5] \rightarrow$$ we need 1 bit to convey the value of $x$ because answer could be True or False ( 1 or 0 ):
$$\begin{align}
H(p) &= -P[True]log(P[True]) - P[False]log(P[False]) = 0.5 + 0.5 = 1
\end{align}$$

So entropy measures the number of bits that we would expect to need in order to convey information content in the world given by $$P(x)$$. Running with this, cross-entropy measures the number of bits we would expect to need in order to convey information content in the world given by $$P(x)$$ but assuming $$Q(x)$$. If we assume $$Q(x)$$, and $$P(x)$$ is the true world, we would expect to be surprised way more often. So it would make sense that someone would need way more bits to convey information to us about what’s going on in this strange world $$P(x)$$.
The difference between these, cross-entropy $$-$$ entropy, is called the Kullback-Leibler divergence, $$KL(P|Q)$$, and it measures how many more bits you need to convey a message when you are assuming Q(x) and the real world is really given by P(x). So this tells you how much worse Q(x) is when you should be using P(x). The KL divergence is used a lot in ML to measure the difference between two distributions, i.e., how much worse Q is than P at encoding a message. Technically, it is not a distance because $$KL(P|Q) \ne KL(Q|P)$$. It also doesn’t satisfy the triangle inequality. And sometimes we end up trying to minimize $$KL(Q|P)$$ just because $$KL(P|Q)$$ is impossible. If $$KL(Q|P) = 0$$, then $$Q=P$$ almost everywhere.
