---
layout: post
title: Extragradient, Consensus, and Crossing the Curl
---

The projection method is known to fail at solving monotone variational inequalities: $$x_{k+1} = x_k - \alpha F(x_k)$$.

1) Let's derive a first order approximation to the Extragradient method (Korpelevich '76). Let $$J(x)$$ be the Jacobian of $$F$$ at $$x$$.

$$\begin{align}
  \hat{x}_{k+1} &= x_k - \alpha F(x_k) \\
  x_{k+1} &= x_k - \alpha F(\hat{x}_{k+1}) \\
  F(\hat{x}_{k+1}) &= F(x_k) - \alpha J(x_k) F(x_k) - \mathcal{O}(\alpha^2) \\
  x_{k+1} &= x_k - \alpha (F(x_k) - \alpha J(x_k) F(x_k)) + \mathcal{O}(\alpha^3) \\
  &= x_k - \alpha (I - \alpha J(x_k)) F(x_k) + \mathcal{O}(\alpha^3)
\end{align}$$

From this, we can see that the Extragradient method is capturing higher order information with $$J$$.

2) Let's compare this to the consensus algorithm which includes a $$\gamma \nabla \|F\|^2$$ term.

$$\begin{align}
  x_{k+1} &= x_k - \alpha (F(x_k) - \gamma \nabla ||F||^2) \\
  &= x_k - \alpha (I + \gamma J(x_k)^T) F(x_k)
\end{align}$$

The consensus algorithm is using $$J^T$$ while the extragradient algorithm is using $$-J$$. If $$J$$ is skew-symmetric (which is this case for a field with only rotation), then these are the same. However, this is not common in practice (zero-sum games for instance). Also, extragradient uses the factor $$\alpha$$ and the consensus algorithm uses an additional user defined scalar $$\gamma$$. I'll also note that the consensus paper explores the use of a preconditioning matrix, $$I-\gamma J^T$$, which is also covered by VI theory (see Dafermos - general iterative algorithm).

3) The problem with monotone fields is that they contain cycles or loops. In that case, we want to travel perpendicularly to the cycle. We can compute this direction using the curl and a cross-product. Intuitively (in 3d), the curl of a vector field gives it's axis of rotation (convention is counter clockwise rotation). The vector that is both perpendicular to the vector field (direction we are traveling if on a merry-go-round) and the axis of rotation will be a vector that points directly towards the center of the merry-go-round (it could also point radially outward, so we just need to get the sign right). Let $$F = F(x)$$ and $$J = J(F)(x)$$. Also, in the following derivations, $$x_i$$ refers to the ith component of the vector $$x$$, not $$x$$ at iteration $$i$$ of the algorithm.

$$\begin{align}
  u \times v &= \[ u_2 v_3 - u_3 v_2 , u_3 v_1 - u_1 v_3 , u_1 v_2 - u_2 v_1 \]
\end{align}$$

$$\begin{align}
  \nabla \times F &= \Big\[ \frac{\partial F_3}{\partial x_2} - \frac{\partial F_2}{\partial x_3} , \frac{\partial F_1}{\partial x_3} - \frac{\partial F_3}{\partial x_1} , \frac{\partial F_2}{\partial x_1} - \frac{\partial F_1}{\partial x_2} \Big\]
\end{align}$$

$$\begin{align}
  (\nabla \times F) \times F &= -F \times (\nabla \times F) \\
  &= -v \times (\nabla \times F) \text{ where } v=F \\
  &= -\nabla_F (v \cdot F) + (v \cdot \nabla) F \text{ where } \nabla_F \text{ is Feynman notation} \\
  &= -\Big( v_1 \[ \frac{\partial F_1}{\partial x_1}, \ldots, \frac{\partial F_1}{\partial x_n}) \] + \ldots + v_n \[ (\frac{\partial F_n}{\partial x_1}, \ldots, \frac{\partial F_n}{\partial x_n}) \] \Big) \\
  &+ (v_1 \frac{\partial}{\partial x_1} + \ldots + v_n \frac{\partial}{\partial x_n}) F \\
  &= (J-J^T)F
\end{align}$$

Let's test our derivation with some simple examples.

$$\begin{align}
  F(x) &= \[x_2, -x_1, 0\]^T \\
  \nabla \times F &= \[ 0, 0, -2 \] \\
  (\nabla \times F) \times F &= \[ -2x_1 , -2x_2 , 0 \] \\
  J &= \begin{bmatrix} 0 & 1 \\ -1 & 0 \end{bmatrix} \\
  (J-J^T) &= \begin{bmatrix} 0 & 2 \\ -2 & 0 \end{bmatrix} \\
  (J-J^T)F &= \[ -2x_1 , -2x_2 \] \surd
\end{align}$$

More generally,

$$\begin{align}
  F(x) &= \[ax_1 + bx_2, cx_1 + dx_2, 0\]^T \\
  \nabla \times F &= \[ 0, 0, c - b \] \\
  (\nabla \times F) \times F &= \[ -(c-b)(cx_1+dx_2) , (c-b)(ax_1+bx_2) , 0 \] \\
  &= (c-b)\[ -(cx_1+dx_2) , (ax_1+bx_2) , 0 \] \\
  J &= \begin{matrix} a & b \\\\ c & d \end{matrix} \\
  (J-J^T) &= \begin{bmatrix} 0 & b-c \\\\ c-b & 0 \end{bmatrix} \\
  (J-J^T)F &= \[ -(c-b)(cx_1 + dx_2) , (c-b)(ax_1 + bx_2) \] \surd
\end{align}$$

This suggests the following algorithm

$$\begin{align}
  x\_{k+1} &= x_k - \alpha (I - \gamma(J-J^T))F
\end{align}$$

Putting all three algorithms side by side, we see that extragradient incorporates $$J$$, consensus incorporates $$J^T$$, and our proposed algorithm incorporates both. What's appealing about our proposed algorithm is that $$J-J^T = 0$$ for optimization problems (i.e., 1-player systems), so that this approach nicely generalizes gradient descent.
