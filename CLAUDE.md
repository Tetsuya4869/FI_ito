# CLAUDE.md — AI Assistant Guide for FI_ito

## Project Overview

**FI_ito** (伊藤の公式に基づく検証) is an educational Python project implementing and numerically verifying **Itô's Formula** from stochastic calculus, with applications to financial derivatives pricing.

**Core purpose**: Demonstrate that the Itô integral approximation (Euler-Maruyama method) converges to the analytical solution of Itô's Formula, and apply this to Geometric Brownian Motion and Black-Scholes option pricing.

---

## Repository Structure

```
FI_ito/
├── ito_formula.py   # Core implementation (single executable module)
├── notes.md         # Theoretical notes on Itô's Formula (LaTeX math, Japanese)
├── README.md        # Minimal project title
├── .gitignore       # Python/Jupyter/IDE/OS ignore rules
└── LICENSE          # MIT License
```

This is intentionally a **minimal, single-file project**. Do not introduce unnecessary directories or abstractions.

---

## Running the Code

```bash
python3 ito_formula.py
```

This runs the `__main__` block, which outputs:
- Exponential process verification (analytical vs. Euler-Maruyama)
- GBM simulation end price
- Black-Scholes call option price

### Dependencies

No `requirements.txt` exists. Install manually:

```bash
pip install numpy scipy
```

- `numpy` — all numerical operations
- `scipy.stats.norm` — CDF in Black-Scholes (imported lazily inside `black_scholes_call`)

---

## Core Functions (`ito_formula.py`)

| Function | Purpose |
|---|---|
| `simulate_brownian_motion(T, n, seed)` | Generates Brownian motion path via cumulative normal increments |
| `ito_formula_exp(T, n, mu, sigma)` | Validates Itô's Formula by comparing analytical vs. Euler-Maruyama for f(x) = exp(μt + σW_t) |
| `geometric_brownian_motion(S0, mu, sigma, T, n, seed)` | Simulates GBM path using the closed-form solution |
| `black_scholes_call(S, K, T, r, sigma)` | Prices European call options via the Black-Scholes formula |

---

## Code Conventions

- **Language**: Python 3 with type hints on all function signatures
- **Style**: PEP 8, functional (no classes), snake_case function/variable names
- **Math variable naming**: Preserve academic notation — `T` (terminal time), `n` (steps), `S` (stock price), `K` (strike), `mu`/`sigma` (parameters), `W` (Brownian motion), `dt` (time increment)
- **Docstrings**: Japanese descriptions, Google-style `Args`/`Returns` sections
- **Comments**: Japanese inline comments explaining mathematical meaning
- **No OOP**: Keep all logic as pure functions; avoid introducing classes
- **Lazy imports**: `scipy` is imported inside the function that needs it — maintain this pattern

---

## Key Mathematical Concepts

**Itô's Formula** (for f(X_t) where dX_t = μ dt + σ dW_t):
```
df = (∂f/∂t + μ ∂f/∂x + ½σ² ∂²f/∂x²) dt + σ ∂f/∂x dW_t
```
The critical term is `½σ² ∂²f/∂x²` — absent in classical calculus, present in stochastic calculus.

**Euler-Maruyama scheme** (numerical SDE solver):
```
X_{i+1} = X_i + drift·dt + diffusion·dW_i
```

**GBM closed form**:
```
S_t = S_0 · exp((μ - σ²/2)t + σW_t)
```

**Black-Scholes call**:
```
C = S·N(d1) - K·e^{-rT}·N(d2)
d1 = (ln(S/K) + (r + σ²/2)T) / (σ√T)
d2 = d1 - σ√T
```

---

## Development Workflow

### Branch

Always develop on `claude/add-claude-documentation-9EKUJ` (or the branch specified for the current task). Never push to `main` directly.

### Making Changes

1. Read the file before editing — understand existing logic before modifying
2. Keep changes minimal and focused
3. Preserve mathematical accuracy — do not alter numerical methods without verifying correctness
4. Maintain Japanese docstrings and comments for consistency

### Committing & Pushing

```bash
git add <specific-files>
git commit -m "descriptive message"
git push -u origin <branch-name>
```

---

## Testing

There is **no test framework**. Validation is built into `ito_formula_exp()`:
- Returns `error = |X_true[-1] - X_ito[-1]|`
- With `n=100_000` steps, expect error on the order of `1e-3` or smaller

When adding new numerical methods, include an analogous error metric.

If formal tests are added in the future, use `pytest` and place tests in a `tests/` directory.

---

## What NOT to Do

- Do not add a web framework, API layer, or database
- Do not introduce classes or OOP patterns unless the project scope fundamentally changes
- Do not add CI/CD, Docker, or deployment configuration unless explicitly requested
- Do not alter the mathematical formulas without verifying against `notes.md`
- Do not create `requirements.txt` or packaging config unless requested
- Do not add logging, argument parsing, or CLI flags unless explicitly asked
