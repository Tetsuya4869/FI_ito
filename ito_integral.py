"""
Itô積分 vs Stratonovich積分の比較

Itô積分:      ∫₀ᵀ f(W_t) dW_t  ← 左端点で評価（非先読み）
Stratonovich積分: ∫₀ᵀ f(W_t) ∘ dW_t  ← 中点で評価

変換関係:
  ∫₀ᵀ f(W_t) ∘ dW_t = ∫₀ᵀ f(W_t) dW_t + (1/2)∫₀ᵀ f'(W_t) dt
"""

import numpy as np


def ito_integral(f, T: float = 1.0, n: int = 10_000, seed: int = 42) -> float:
    """Itô積分 ∫₀ᵀ f(W_t) dW_t を左リーマン和で近似。"""
    rng = np.random.default_rng(seed)
    dt = T / n
    dW = rng.normal(0, np.sqrt(dt), n)
    W = np.concatenate([[0.0], np.cumsum(dW)])
    return float(np.sum(f(W[:-1]) * dW))


def stratonovich_integral(f, T: float = 1.0, n: int = 10_000, seed: int = 42) -> float:
    """Stratonovich積分 ∫₀ᵀ f(W_t) ∘ dW_t を中点リーマン和で近似。"""
    rng = np.random.default_rng(seed)
    dt = T / n
    dW = rng.normal(0, np.sqrt(dt), n)
    W = np.concatenate([[0.0], np.cumsum(dW)])
    W_mid = 0.5 * (W[:-1] + W[1:])
    return float(np.sum(f(W_mid) * dW))


def verify_ito_isometry(n_paths: int = 5_000, T: float = 1.0, n: int = 1_000, seed: int = 0) -> dict:
    """
    伊藤等長性の検証: E[|∫₀ᵀ f(t) dW_t|²] = E[∫₀ᵀ f(t)² dt]

    f(t) = 1 のとき: E[W_T²] = T
    """
    rng = np.random.default_rng(seed)
    dt = T / n
    results = []
    for _ in range(n_paths):
        dW = rng.normal(0, np.sqrt(dt), n)
        results.append(np.sum(dW) ** 2)

    empirical = float(np.mean(results))
    theoretical = T
    return {"empirical_E[W_T^2]": empirical, "theoretical_T": theoretical, "error": abs(empirical - theoretical)}


def compare_ito_stratonovich(n_steps: int = 100_000, seed: int = 42) -> None:
    """
    例: f(x) = x のとき

    Itô:          ∫₀¹ W_t dW_t = (W_1² - 1) / 2
    Stratonovich: ∫₀¹ W_t ∘ dW_t = W_1² / 2
    差:           Stratonovich - Itô = 1/2 = [W]_1 / 2
    """
    rng = np.random.default_rng(seed)
    dt = 1.0 / n_steps
    dW = rng.normal(0, np.sqrt(dt), n_steps)
    W = np.concatenate([[0.0], np.cumsum(dW)])
    W_T = W[-1]

    ito_val = np.sum(W[:-1] * dW)
    strat_val = np.sum(0.5 * (W[:-1] + W[1:]) * dW)

    ito_exact = (W_T**2 - 1.0) / 2
    strat_exact = W_T**2 / 2

    print("[Itô vs Stratonovich 比較: ∫W dW]")
    print(f"  Itô  数値: {ito_val:.6f}  解析: {ito_exact:.6f}  差: {abs(ito_val - ito_exact):.2e}")
    print(f"  Strat数値: {strat_val:.6f}  解析: {strat_exact:.6f}  差: {abs(strat_val - strat_exact):.2e}")
    print(f"  Strat - Itô = {strat_val - ito_val:.6f}  (理論値 1/2 = 0.5)")


if __name__ == "__main__":
    compare_ito_stratonovich()

    iso = verify_ito_isometry()
    print(f"\n[伊藤等長性] E[W_T²] ≈ {iso['empirical_E[W_T^2]']:.4f}  理論値 T=1: {iso['theoretical_T']}")
