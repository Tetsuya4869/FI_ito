"""
モンテカルロ法によるオプション価格計算

伊藤の公式 → GBM解析解 → モンテカルロシミュレーション → オプション価格
"""

import numpy as np
from scipy.stats import norm


def black_scholes_call(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0:
        return max(S - K, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def black_scholes_put(S: float, K: float, T: float, r: float, sigma: float) -> float:
    if T <= 0:
        return max(K - S, 0.0)
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def mc_european(
    S0: float, K: float, T: float, r: float, sigma: float,
    option_type: str = "call",
    n_paths: int = 100_000,
    seed: int = 42,
) -> dict:
    """
    欧州型オプションのモンテカルロ価格計算。

    GBM の解析解: S_T = S_0 exp((r - σ²/2)T + σ√T Z),  Z ~ N(0,1)

    Returns:
        価格・標準誤差・ブラック・ショールズ理論値
    """
    rng = np.random.default_rng(seed)
    Z = rng.standard_normal(n_paths)
    S_T = S0 * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(S_T - K, 0)
        bs_price = black_scholes_call(S0, K, T, r, sigma)
    else:
        payoffs = np.maximum(K - S_T, 0)
        bs_price = black_scholes_put(S0, K, T, r, sigma)

    discounted = np.exp(-r * T) * payoffs
    price = float(np.mean(discounted))
    stderr = float(np.std(discounted) / np.sqrt(n_paths))

    return {
        "mc_price": price,
        "stderr": stderr,
        "ci_95": (price - 1.96 * stderr, price + 1.96 * stderr),
        "bs_price": bs_price,
        "error": abs(price - bs_price),
    }


def mc_asian_call(
    S0: float, K: float, T: float, r: float, sigma: float,
    n_steps: int = 252, n_paths: int = 50_000, seed: int = 42,
) -> dict:
    """
    アジアン・コールオプション（算術平均）のモンテカルロ価格計算。
    閉形式解なし → モンテカルロの典型的な応用例。

    ペイオフ: max(Ā - K, 0),  Ā = (1/n) Σ S_ti
    """
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    Z = rng.standard_normal((n_paths, n_steps))

    log_S = np.log(S0) + np.cumsum(
        (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z, axis=1
    )
    S_paths = np.exp(log_S)
    avg_S = np.mean(S_paths, axis=1)

    payoffs = np.maximum(avg_S - K, 0)
    discounted = np.exp(-r * T) * payoffs
    price = float(np.mean(discounted))
    stderr = float(np.std(discounted) / np.sqrt(n_paths))

    return {
        "mc_price": price,
        "stderr": stderr,
        "ci_95": (price - 1.96 * stderr, price + 1.96 * stderr),
    }


def mc_barrier_call(
    S0: float, K: float, B: float, T: float, r: float, sigma: float,
    barrier_type: str = "down-out",
    n_steps: int = 252, n_paths: int = 50_000, seed: int = 42,
) -> dict:
    """
    バリア・コールオプションのモンテカルロ価格計算。

    Args:
        B: バリア水準
        barrier_type: "down-out"（ダウン・アンド・アウト）または "up-out"
    """
    rng = np.random.default_rng(seed)
    dt = T / n_steps
    Z = rng.standard_normal((n_paths, n_steps))

    log_S = np.log(S0) + np.cumsum(
        (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z, axis=1
    )
    S_paths = np.exp(log_S)

    if barrier_type == "down-out":
        alive = np.all(S_paths > B, axis=1)
    else:
        alive = np.all(S_paths < B, axis=1)

    S_T = S_paths[:, -1]
    payoffs = np.where(alive, np.maximum(S_T - K, 0), 0.0)
    discounted = np.exp(-r * T) * payoffs
    price = float(np.mean(discounted))
    stderr = float(np.std(discounted) / np.sqrt(n_paths))

    return {
        "mc_price": price,
        "stderr": stderr,
        "ci_95": (price - 1.96 * stderr, price + 1.96 * stderr),
        "knock_out_rate": float(1 - np.mean(alive)),
    }


def convergence_analysis(
    S0: float = 100, K: float = 100, T: float = 1.0, r: float = 0.05, sigma: float = 0.2,
    path_counts: list[int] | None = None,
) -> list[dict]:
    """パス数を変えてモンテカルロの収束を確認。"""
    if path_counts is None:
        path_counts = [100, 1_000, 10_000, 100_000, 1_000_000]

    bs = black_scholes_call(S0, K, T, r, sigma)
    results = []
    for n in path_counts:
        res = mc_european(S0, K, T, r, sigma, n_paths=n)
        results.append({"n_paths": n, "mc_price": res["mc_price"], "bs_price": bs, "error": res["error"], "stderr": res["stderr"]})
    return results


if __name__ == "__main__":
    params = dict(S0=100, K=100, T=1.0, r=0.05, sigma=0.2)

    print("[欧州型コール]")
    res = mc_european(**params, option_type="call", n_paths=200_000)
    print(f"  MC価格: {res['mc_price']:.4f}  BS理論値: {res['bs_price']:.4f}  誤差: {res['error']:.4f}")
    print(f"  95%CI: ({res['ci_95'][0]:.4f}, {res['ci_95'][1]:.4f})")

    print("\n[アジアン・コール（算術平均）]")
    res_a = mc_asian_call(**params, n_steps=252, n_paths=100_000)
    print(f"  MC価格: {res_a['mc_price']:.4f}  (閉形式解なし)")
    print(f"  95%CI: ({res_a['ci_95'][0]:.4f}, {res_a['ci_95'][1]:.4f})")

    print("\n[バリア・コール (down-out, B=90)]")
    res_b = mc_barrier_call(**params, B=90, barrier_type="down-out", n_steps=252, n_paths=100_000)
    print(f"  MC価格: {res_b['mc_price']:.4f}  ノックアウト率: {res_b['knock_out_rate']:.2%}")

    print("\n[収束分析]")
    print(f"  {'n_paths':>10}  {'MC価格':>8}  {'誤差':>8}  {'標準誤差':>10}")
    for row in convergence_analysis(**params):
        print(f"  {row['n_paths']:>10,}  {row['mc_price']:>8.4f}  {row['error']:>8.4f}  {row['stderr']:>10.6f}")
