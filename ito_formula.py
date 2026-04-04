"""
伊藤の公式 (Itô's Formula) の基本実装と数値検証

伊藤の公式:
  X_t がItô過程で dX_t = μ_t dt + σ_t dW_t のとき、
  f(t, X_t) に対して:

  df(t, X_t) = (∂f/∂t + μ_t ∂f/∂x + (1/2)σ_t² ∂²f/∂x²) dt + σ_t ∂f/∂x dW_t
"""

import numpy as np


def simulate_brownian_motion(T: float, n: int, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """ブラウン運動の経路をシミュレート。

    Args:
        T: 終端時刻
        n: ステップ数
        seed: 乱数シード

    Returns:
        (時刻グリッド, ブラウン運動の経路)
    """
    rng = np.random.default_rng(seed)
    dt = T / n
    t = np.linspace(0, T, n + 1)
    dW = rng.normal(0, np.sqrt(dt), n)
    W = np.concatenate([[0], np.cumsum(dW)])
    return t, W


def ito_formula_exp(T: float = 1.0, n: int = 10_000, mu: float = 0.0, sigma: float = 1.0) -> dict:
    """
    伊藤の公式の検証例: f(x) = exp(μt + σW_t)

    通常の微積分では df = (μ + σ²/2)f dt + σf dW だが、
    伊藤の公式では修正項 (1/2)σ² が加わる。

    解析解: exp(μt + σW_t) = exp((μ - σ²/2)t + σW_t) × exp(σ²t/2)
    幾何ブラウン運動の解: S_t = S_0 exp((μ - σ²/2)t + σW_t)
    """
    t, W = simulate_brownian_motion(T, n)
    dt = T / n

    # 直接計算（真値）
    X_true = np.exp(mu * t + sigma * W)

    # 伊藤積分による近似（オイラー・丸山法）
    X_ito = np.zeros(n + 1)
    X_ito[0] = 1.0
    dW = np.diff(W)
    for i in range(n):
        drift = (mu + 0.5 * sigma**2) * X_ito[i] * dt
        diffusion = sigma * X_ito[i] * dW[i]
        X_ito[i + 1] = X_ito[i] + drift + diffusion

    error = np.abs(X_true[-1] - X_ito[-1])
    return {
        "t": t,
        "X_true": X_true,
        "X_ito": X_ito,
        "final_true": X_true[-1],
        "final_ito": X_ito[-1],
        "error": error,
    }


def geometric_brownian_motion(S0: float, mu: float, sigma: float, T: float, n: int, seed: int = 42) -> tuple[np.ndarray, np.ndarray]:
    """
    幾何ブラウン運動 (GBM) のシミュレーション。
    ブラック・ショールズモデルの株価過程。

    dS_t = μ S_t dt + σ S_t dW_t
    解析解: S_t = S_0 exp((μ - σ²/2)t + σW_t)

    Args:
        S0: 初期株価
        mu: ドリフト
        sigma: ボラティリティ
        T: 終端時刻
        n: ステップ数
        seed: 乱数シード

    Returns:
        (時刻グリッド, GBM経路)
    """
    t, W = simulate_brownian_motion(T, n, seed)
    S = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)
    return t, S


def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """
    ブラック・ショールズ公式（コールオプション価格）。
    伊藤の公式を用いてオプション価格の偏微分方程式を導出した結果。

    C(S,t) = S N(d1) - K e^{-rT} N(d2)
    d1 = (ln(S/K) + (r + σ²/2)T) / (σ√T)
    d2 = d1 - σ√T

    Args:
        S: 現在の株価
        K: 行使価格
        T: 満期（年）
        r: リスクフリーレート
        sigma: ボラティリティ

    Returns:
        コールオプション価格
    """
    from scipy.stats import norm

    if T <= 0:
        return max(S - K, 0.0)

    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


if __name__ == "__main__":
    print("=" * 50)
    print("伊藤の公式 - 数値検証")
    print("=" * 50)

    result = ito_formula_exp(T=1.0, n=100_000, mu=0.05, sigma=0.2)
    print(f"\n[exp過程の検証]")
    print(f"  真値  : {result['final_true']:.6f}")
    print(f"  伊藤法: {result['final_ito']:.6f}")
    print(f"  誤差  : {result['error']:.2e}")

    print(f"\n[幾何ブラウン運動 (GBM)]")
    t, S = geometric_brownian_motion(S0=100, mu=0.05, sigma=0.2, T=1.0, n=252)
    print(f"  初期株価: 100.00")
    print(f"  終端株価: {S[-1]:.2f}")

    print(f"\n[ブラック・ショールズ コールオプション価格]")
    C = black_scholes_call(S=100, K=100, T=1.0, r=0.05, sigma=0.2)
    print(f"  C(100, K=100, T=1, r=5%, σ=20%) = {C:.4f}")
    print()
