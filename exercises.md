# 練習問題 — 伊藤の公式

## 問題 1（基本）: $f(x) = x^3$

$W_t$ をブラウン運動とするとき、伊藤の公式を用いて $d(W_t^3)$ を求めよ。

また、$\int_0^t W_s^2 \, dW_s$ を $W_t^3$ を使って表せ。

<details>
<summary>解答</summary>

$f(x) = x^3$ に伊藤の公式を適用（$f'=3x^2$, $f''=6x$）:

$$d(W_t^3) = 3W_t^2 \, dW_t + \frac{1}{2} \cdot 6W_t \, dt = 3W_t^2 \, dW_t + 3W_t \, dt$$

積分形:

$$W_t^3 = 3\int_0^t W_s^2 \, dW_s + 3\int_0^t W_s \, ds$$

よって:

$$\int_0^t W_s^2 \, dW_s = \frac{W_t^3}{3} - \int_0^t W_s \, ds$$
</details>

---

## 問題 2（基本）: 指数マルチンゲール

$M_t = \exp\!\left(\sigma W_t - \frac{\sigma^2}{2} t\right)$ がマルチンゲールであることを示せ。

<details>
<summary>解答</summary>

$f(t, x) = e^{\sigma x - \sigma^2 t/2}$ として伊藤の公式を適用:

$$\frac{\partial f}{\partial t} = -\frac{\sigma^2}{2} M_t, \quad \frac{\partial f}{\partial x} = \sigma M_t, \quad \frac{\partial^2 f}{\partial x^2} = \sigma^2 M_t$$

$$dM_t = \left(-\frac{\sigma^2}{2} M_t + \frac{1}{2}\sigma^2 M_t\right) dt + \sigma M_t \, dW_t = \sigma M_t \, dW_t$$

$dM_t$ に $dt$ 項がないため $M_t$ は（局所）マルチンゲール。  
$E[M_t] = M_0 = 1$ も確認できる。
</details>

---

## 問題 3（中級）: OU過程の明示解

Ornstein-Uhlenbeck 過程 $dX_t = -\theta X_t \, dt + \sigma \, dW_t$（$X_0 = x_0$）の解析解を求めよ。

ヒント: $Y_t = e^{\theta t} X_t$ とおいて $dY_t$ を計算せよ。

<details>
<summary>解答</summary>

$f(t, x) = e^{\theta t} x$ として伊藤の公式:

$$dY_t = \theta e^{\theta t} X_t \, dt + e^{\theta t} dX_t = \theta e^{\theta t} X_t \, dt + e^{\theta t}(-\theta X_t \, dt + \sigma \, dW_t) = \sigma e^{\theta t} \, dW_t$$

積分すると:

$$e^{\theta t} X_t = x_0 + \sigma \int_0^t e^{\theta s} \, dW_s$$

$$\boxed{X_t = x_0 e^{-\theta t} + \sigma \int_0^t e^{-\theta(t-s)} \, dW_s}$$

これはガウス過程であり:
- $E[X_t] = x_0 e^{-\theta t}$
- $\mathrm{Var}(X_t) = \dfrac{\sigma^2}{2\theta}(1 - e^{-2\theta t})$
</details>

---

## 問題 4（中級）: 二次変分

$X_t$ と $Y_t$ が Itô 過程のとき、積の公式（伊藤の積公式）を導け:

$$d(X_t Y_t) = X_t \, dY_t + Y_t \, dX_t + d\langle X, Y \rangle_t$$

<details>
<summary>解答</summary>

$f(x, y) = xy$ として二変数の伊藤の公式を適用:

$$df = \frac{\partial f}{\partial x} dX_t + \frac{\partial f}{\partial y} dY_t + \frac{1}{2}\frac{\partial^2 f}{\partial x^2} d\langle X \rangle_t + \frac{1}{2}\frac{\partial^2 f}{\partial y^2} d\langle Y \rangle_t + \frac{\partial^2 f}{\partial x \partial y} d\langle X, Y \rangle_t$$

$f_{xx} = f_{yy} = 0$, $f_{xy} = 1$ なので:

$$d(X_t Y_t) = Y_t \, dX_t + X_t \, dY_t + d\langle X, Y \rangle_t$$
</details>

---

## 問題 5（発展）: ブラック・ショールズ PDE の導出

株価が $dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$ に従うとする。  
オプション価格 $V(t, S_t)$ に伊藤の公式を適用し、デルタヘッジ戦略を構成して  
ブラック・ショールズ PDE を導け:

$$\frac{\partial V}{\partial t} + rS\frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - rV = 0$$

<details>
<summary>解答のスケッチ</summary>

**Step 1**: 伊藤の公式を適用:
$$dV = \left(\frac{\partial V}{\partial t} + \mu S \frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}\right) dt + \sigma S \frac{\partial V}{\partial S} \, dW_t$$

**Step 2**: デルタヘッジポートフォリオ $\Pi = V - \Delta S$（$\Delta = \partial V / \partial S$）を構成:
$$d\Pi = dV - \Delta \, dS = \left(\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}\right) dt$$

（$dW_t$ 項が消えてリスクフリーに！）

**Step 3**: 裁定なし条件 $d\Pi = r\Pi \, dt$:
$$\frac{\partial V}{\partial t} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} = r\left(V - S\frac{\partial V}{\partial S}\right)$$

整理してブラック・ショールズ PDE を得る。
</details>

---

## 問題 6（発展）: Girsanov の定理の応用

$W_t^P$ をリアル測度 $P$ のもとでのブラウン運動とし、株価 $dS_t = \mu S_t \, dt + \sigma S_t \, dW_t^P$ とする。  
リスク中立測度 $Q$ のもとで $W_t^Q = W_t^P + \frac{\mu - r}{\sigma} t$（市場価格のリスク）が  
ブラウン運動になることを確認し、$Q$ のもとでの株価過程を求めよ。

<details>
<summary>解答</summary>

市場価格のリスク $\lambda = \frac{\mu - r}{\sigma}$ とおくと、Girsanov の定理より

$$W_t^Q = W_t^P + \lambda t$$

はリスク中立測度 $Q$ のもとでのブラウン運動。これを代入すると:

$$dS_t = \mu S_t \, dt + \sigma S_t (dW_t^Q - \lambda \, dt) = (\mu - \sigma\lambda) S_t \, dt + \sigma S_t \, dW_t^Q = r S_t \, dt + \sigma S_t \, dW_t^Q$$

$Q$ のもとでドリフトがリスクフリーレート $r$ になる。
</details>
