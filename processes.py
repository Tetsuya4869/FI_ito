"""
確率過程コレクション — 伊藤の公式の応用

各モデルの SDE と解析解（存在する場合）を実装。
"""

import numpy as np


def ornstein_uhlenbeck(
    x0: float, theta: float, mu: float, sigma: float,
    T: float, n: int, seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """
    Ornstein-Uhlenbeck (OU) 過程 — 平均回帰過程。
    金利モデル（Vasicek）の基礎。

    SDE: dX_t = θ(μ - X_t) dt + σ dW_t
    解析解: X_t = μ + (X_0 - μ)e^{-θt} + σ∫₀ᵗ e^{-θ(t-s)} dW_s

    Args:
        x0: 初期値
        theta: 平均回帰速度
        mu: 長期平均
        sigma: ボラティリティ
    """
    rng = np.random.default_rng(seed)
    dt = T / n
    t = np.linspace(0, T, n + 1)

    # オイラー・丸山法
    X = np.zeros(n + 1)
    X[0] = x0
    dW = rng.normal(0, np.sqrt(dt), n)
    for i in range(n):
        X[i + 1] = X[i] + theta * (mu - X[i]) * dt + sigma * dW[i]

    # 解析解（条件付き期待値と分散）
    E_X = mu + (x0 - mu) * np.exp(-theta * t)
    Var_X = (sigma**2 / (2 * theta)) * (1 - np.exp(-2 * theta * t))

    return t, X, E_X, Var_X


def cir_process(
    x0: float, kappa: float, theta: float, sigma: float,
    T: float, n: int, seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """
    Cox-Ingersoll-Ross (CIR) 過程 — 常に非負の平均回帰過程。
    金利・ボラティリティモデルに使用。

    SDE: dX_t = κ(θ - X_t) dt + σ√X_t dW_t
    Feller条件（非負性保証）: 2κθ ≥ σ²

    Args:
        kappa: 平均回帰速度
        theta: 長期平均
        sigma: ボラティリティ係数
    """
    rng = np.random.default_rng(seed)
    dt = T / n
    t = np.linspace(0, T, n + 1)

    X = np.zeros(n + 1)
    X[0] = x0
    dW = rng.normal(0, np.sqrt(dt), n)
    for i in range(n):
        X[i + 1] = X[i] + kappa * (theta - X[i]) * dt + sigma * np.sqrt(max(X[i], 0)) * dW[i]
        X[i + 1] = max(X[i + 1], 0)  # 非負性を強制

    feller = 2 * kappa * theta >= sigma**2
    return t, X, feller


def heston_model(
    S0: float, v0: float,
    mu: float, kappa: float, theta: float, sigma_v: float, rho: float,
    T: float, n: int, seed: int = 42
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Hestonモデル — 確率的ボラティリティモデル。
    ブラック・ショールズの定数ボラティリティ仮定を緩和。

    SDE:
      dS_t = μ S_t dt + √v_t S_t dW_t^S
      dv_t = κ(θ - v_t) dt + σ_v √v_t dW_t^v
      dW_t^S · dW_t^v = ρ dt  （相関ブラウン運動）

    Args:
        S0: 初期株価
        v0: 初期分散
        mu: 株価ドリフト
        kappa: 分散の平均回帰速度
        theta: 長期分散
        sigma_v: ボラティリティ・オブ・ボラティリティ
        rho: 株価と分散の相関
    """
    rng = np.random.default_rng(seed)
    dt = T / n
    t = np.linspace(0, T, n + 1)

    S = np.zeros(n + 1)
    v = np.zeros(n + 1)
    S[0], v[0] = S0, v0

    # 相関ブラウン運動の生成
    Z1 = rng.normal(0, 1, n)
    Z2 = rng.normal(0, 1, n)
    dW_S = Z1 * np.sqrt(dt)
    dW_v = (rho * Z1 + np.sqrt(1 - rho**2) * Z2) * np.sqrt(dt)

    for i in range(n):
        v_pos = max(v[i], 0)
        S[i + 1] = S[i] * (1 + mu * dt + np.sqrt(v_pos) * dW_S[i])
        v[i + 1] = v[i] + kappa * (theta - v[i]) * dt + sigma_v * np.sqrt(v_pos) * dW_v[i]
        v[i + 1] = max(v[i + 1], 0)

    return t, S, v


def merton_jump_diffusion(
    S0: float, mu: float, sigma: float,
    lambda_: float, mu_j: float, sigma_j: float,
    T: float, n: int, seed: int = 42
) -> tuple[np.ndarray, np.ndarray]:
    """
    Mertonジャンプ拡散モデル — 株価のジャンプを考慮。

    SDE: dS_t = (μ - λk̄) S_t dt + σ S_t dW_t + S_{t-} (e^J - 1) dN_t
    J ~ N(μ_j, σ_j²),  k̄ = E[e^J - 1] = exp(μ_j + σ_j²/2) - 1

    Args:
        lambda_: ジャンプ強度（単位時間あたりの平均ジャンプ回数）
        mu_j: ジャンプサイズの対数正規平均
        sigma_j: ジャンプサイズの対数正規標準偏差
    """
    rng = np.random.default_rng(seed)
    dt = T / n
    t = np.linspace(0, T, n + 1)

    k_bar = np.exp(mu_j + 0.5 * sigma_j**2) - 1
    S = np.zeros(n + 1)
    S[0] = S0

    dW = rng.normal(0, np.sqrt(dt), n)
    n_jumps = rng.poisson(lambda_ * dt, n)

    for i in range(n):
        jump = 0.0
        if n_jumps[i] > 0:
            J = rng.normal(mu_j, sigma_j, n_jumps[i])
            jump = np.sum(np.exp(J) - 1)
        S[i + 1] = S[i] * (1 + (mu - lambda_ * k_bar) * dt + sigma * dW[i] + jump)
        S[i + 1] = max(S[i + 1], 0)

    return t, S


if __name__ == "__main__":
    print("[Ornstein-Uhlenbeck 過程]")
    t, X, E_X, Var_X = ornstein_uhlenbeck(x0=2.0, theta=1.5, mu=0.5, sigma=0.3, T=5.0, n=10_000)
    print(f"  初期値: {X[0]:.2f}  終端値: {X[-1]:.4f}  理論 E[X_T]: {E_X[-1]:.4f}")

    print("\n[CIR 過程]")
    t, r, feller = cir_process(x0=0.05, kappa=0.5, theta=0.04, sigma=0.1, T=10.0, n=50_000)
    print(f"  Feller条件充足: {feller}  終端金利: {r[-1]:.4f}  最小値: {r.min():.4f}")

    print("\n[Hestonモデル]")
    t, S, v = heston_model(S0=100, v0=0.04, mu=0.05, kappa=2.0, theta=0.04, sigma_v=0.3, rho=-0.7, T=1.0, n=10_000)
    print(f"  終端株価: {S[-1]:.2f}  終端分散: {v[-1]:.4f}  終端ボラティリティ: {np.sqrt(v[-1]):.4f}")

    print("\n[Mertonジャンプ拡散]")
    t, S_j = merton_jump_diffusion(S0=100, mu=0.05, sigma=0.2, lambda_=1.0, mu_j=-0.1, sigma_j=0.15, T=1.0, n=10_000)
    print(f"  終端株価: {S_j[-1]:.2f}")
