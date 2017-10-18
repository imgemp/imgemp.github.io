---
layout: post
title: Extragradient, Consensus, and The Cross Product
---

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
