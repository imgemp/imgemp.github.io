---
layout: post
title: Extragradient, Consensus, and The Cross Product
---

1) Let's derive a first order approximation to the Extragradient method (Korpelevich '76).
\begin{align}
  \hat{x}\_{k+1} &= x_k - \alpha F(x_k) \\\\
  x\_{k+1} &= x_k - \alpha F(\hat{x}\_{k+1}) \\\\
  F(x\_{k+1}) &= F(x_k) - \alpha J(F(x_k)) F(x_k) - \mathcal{O}(\alpha^2) \\\\
  x\_{k+1} &= x_k - \alpha (F(x_k) - \alpha J(F(x_k)) F(x_k)) + \mathcal{O}(\alpha^3) \\\\
  &= x_k - \alpha (I - \alpha J(F(x_k))) F(x_k) + \mathcal{O}(\alpha^3)
\end{align}

\begin{align}
  u \times v &= \[ u_2 v_3 - u_3 v_2 , u_3 v_1 - u_1 v_3 , u_1 v_2 - u_2 v_1 \]
\end{align}

\begin{align}
  \nabla \times F &= \Big\[ \frac{\partial F_3}{\partial x_2} - \frac{\partial F_2}{\partial x_3} , \frac{\partial F_1}{\partial x_3} - \frac{\partial F_3}{\partial x_1} , \frac{\partial F_2}{\partial x_1} - \frac{\partial F_1}{\partial x_2} \Big\]
\end{align}

\begin{align}
  (\nabla \times F) \times F &= -F \times (\nabla \times F) \\\\
  &= -v \times (\nabla \times F) \text{ where } v=F \\\\
  &= \nabla_F (v \cdot F) - (\nabla \cdot v) F \text{ where } \nabla_F \text{ is Feynman notation} \\\\
  &= \nabla ||F||^2 - tr(J(F)) F
\end{align}

\begin{align}
  F(x) &= \[x_2, -x_1, 0\]^T \\\\
  \nabla \times F &= \[ 0, 0, -2 \] \\\\
  (\nabla \times F) \times F &= \[ -2x_1 , -2x_2 , 0 \]
\end{align}

More generally,

\begin{align}
  F(x) &= \[ax_1 + bx_2, cx_1 + dx_2, 0\]^T \\\\
  \nabla \times F &= \[ 0, 0, c - b \] \\\\
  (\nabla \times F) \times F &= \[ -(c-b)(cx_1+dx_2) , (c-b)(ax_1+bx_2) , 0 \] \\\\
  &= (c-b)\[ -(cx_1+dx_2) , (ax_1+bx_2) , 0 \]
\end{align}
