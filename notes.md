# 伊藤の公式 (Itô's Formula) 学習ノート

## 1. 基本設定

### ブラウン運動 $W_t$
- $W_0 = 0$
- 増分 $W_t - W_s \sim \mathcal{N}(0, t-s)$（$t > s$）
- 独立増分
- 連続経路

### Itô 過程
$$dX_t = \mu_t \, dt + \sigma_t \, dW_t$$

## 2. 伊藤の公式

$f(t, x)$ が $C^{1,2}$（$t$ について $C^1$、$x$ について $C^2$）ならば：

$$df(t, X_t) = \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial x} dX_t + \frac{1}{2} \frac{\partial^2 f}{\partial x^2} d\langle X \rangle_t$$

展開すると：

$$df(t, X_t) = \left(\frac{\partial f}{\partial t} + \mu_t \frac{\partial f}{\partial x} + \frac{1}{2}\sigma_t^2 \frac{\partial^2 f}{\partial x^2}\right) dt + \sigma_t \frac{\partial f}{\partial x} \, dW_t$$

### 通常の微分との違い
通常の連鎖律では $\frac{1}{2}\sigma_t^2 \frac{\partial^2 f}{\partial x^2}$ の項が**ない**。  
これが伊藤の公式の本質的な修正項（**伊藤修正項**）。

理由: $dW_t \cdot dW_t = dt$（二次変分）

## 3. 重要な例

### 例1: $f(x) = x^2$, $X_t = W_t$

通常の微分: $d(W_t^2) = 2W_t \, dW_t$  
伊藤の公式: $d(W_t^2) = 2W_t \, dW_t + dt$

積分形:
$$W_t^2 = 2\int_0^t W_s \, dW_s + t$$

よって:
$$\int_0^t W_s \, dW_s = \frac{W_t^2 - t}{2}$$

### 例2: 幾何ブラウン運動（GBM）

$dS_t = \mu S_t \, dt + \sigma S_t \, dW_t$ を $f(x) = \ln x$ に適用:

$$d(\ln S_t) = \left(\mu - \frac{\sigma^2}{2}\right) dt + \sigma \, dW_t$$

解析解:
$$S_t = S_0 \exp\!\left[\left(\mu - \frac{\sigma^2}{2}\right)t + \sigma W_t\right]$$

> **注意**: $\mu - \frac{\sigma^2}{2}$ の修正項が伊藤修正項。

### 例3: ブラック・ショールズ方程式

オプション価格 $V(t, S)$ に伊藤の公式を適用すると、リスク中立条件のもとで:

$$\frac{\partial V}{\partial t} + rS\frac{\partial V}{\partial S} + \frac{1}{2}\sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} - rV = 0$$

コールオプションの解（ブラック・ショールズ公式）:
$$C = S N(d_1) - K e^{-r(T-t)} N(d_2)$$

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)(T-t)}{\sigma\sqrt{T-t}}, \quad d_2 = d_1 - \sigma\sqrt{T-t}$$

## 4. 多次元の伊藤の公式

$X_t = (X_t^1, \ldots, X_t^n)$ が $n$ 次元 Itô 過程のとき:

$$df(t, X_t) = \frac{\partial f}{\partial t} dt + \sum_i \frac{\partial f}{\partial x_i} dX_t^i + \frac{1}{2}\sum_{i,j} \frac{\partial^2 f}{\partial x_i \partial x_j} d\langle X^i, X^j \rangle_t$$

## 5. 参考文献

- Øksendal, B. *Stochastic Differential Equations* (6th ed.)
- Shreve, S. *Stochastic Calculus for Finance II*
- 藤田岳彦 *確率微分方程式入門*
