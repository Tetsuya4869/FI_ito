/* ── Sidebar definition ── */
const SIDEBAR_HTML = `
  <div class="sidebar-logo">
    <a href="index.html">
      <div class="logo-icon">∑</div>
      <div><div class="logo-text">高等数学</div><div class="logo-sub">Higher Mathematics</div></div>
    </a>
  </div>
  <div class="sidebar-search">
    <input type="text" id="nav-search" placeholder="トピックを検索…" autocomplete="off">
  </div>
  <div class="sidebar-section">
    <nav><a href="index.html"><span class="nav-icon">⌂</span>ホーム</a></nav>
  </div>
  <div class="sidebar-section">
    <div class="sidebar-label">解析系</div>
    <nav>
      <a href="analysis.html"><span class="nav-icon">ε</span>解析学</a>
      <a href="complex-analysis.html"><span class="nav-icon">ℂ</span>複素解析</a>
      <a href="fourier-analysis.html"><span class="nav-icon">∿</span>フーリエ解析</a>
      <a href="pde.html"><span class="nav-icon">∂</span>偏微分方程式</a>
      <a href="functional-analysis.html"><span class="nav-icon">ℋ</span>関数解析</a>
    </nav>
  </div>
  <div class="sidebar-section">
    <div class="sidebar-label">代数系</div>
    <nav>
      <a href="linear-algebra.html"><span class="nav-icon">⊞</span>線形代数</a>
      <a href="abstract-algebra.html"><span class="nav-icon">∘</span>抽象代数学</a>
      <a href="number-theory.html"><span class="nav-icon">ℤ</span>数論</a>
    </nav>
  </div>
  <div class="sidebar-section">
    <div class="sidebar-label">幾何・位相</div>
    <nav>
      <a href="topology.html"><span class="nav-icon">⊙</span>位相空間論</a>
      <a href="differential-geometry.html"><span class="nav-icon">∇</span>微分幾何学</a>
      <a href="algebraic-topology.html"><span class="nav-icon">π</span>代数的位相幾何</a>
    </nav>
  </div>
  <div class="sidebar-section">
    <div class="sidebar-label">確率・統計</div>
    <nav>
      <a href="measure-theory.html"><span class="nav-icon">μ</span>測度論</a>
      <a href="probability.html"><span class="nav-icon">𝑃</span>確率論</a>
      <a href="stochastic.html"><span class="nav-icon">W</span>確率微分方程式</a>
    </nav>
  </div>
  <div class="sidebar-section">
    <div class="sidebar-label">応用数学</div>
    <nav>
      <a href="dynamical-systems.html"><span class="nav-icon">↻</span>力学系</a>
      <a href="optimization.html"><span class="nav-icon">▽</span>最適化・変分法</a>
      <a href="numerical-analysis.html"><span class="nav-icon">≈</span>数値解析</a>
    </nav>
  </div>
`;

document.addEventListener("DOMContentLoaded", function () {

  /* ── Inject sidebar ── */
  const sidebar = document.querySelector(".sidebar");
  if (sidebar) sidebar.innerHTML = SIDEBAR_HTML;

  /* ── KaTeX auto-render ── */
  if (typeof renderMathInElement !== "undefined") {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "$$",  right: "$$",  display: true  },
        { left: "$",   right: "$",   display: false },
        { left: "\\[", right: "\\]", display: true  },
        { left: "\\(", right: "\\)", display: false },
      ],
      throwOnError: false,
    });
  }

  /* ── Active nav link ── */
  const current = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".sidebar nav a").forEach(a => {
    const href = a.getAttribute("href")?.split("/").pop();
    if (href === current || (current === "" && href === "index.html")) {
      a.classList.add("active");
    }
  });

  /* ── Sidebar search ── */
  const searchInput = document.getElementById("nav-search");
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const q = this.value.toLowerCase().trim();
      document.querySelectorAll(".sidebar nav a").forEach(a => {
        const match = !q || a.textContent.toLowerCase().includes(q);
        a.style.display = match ? "" : "none";
      });
      document.querySelectorAll(".sidebar-section").forEach(sec => {
        const visible = [...sec.querySelectorAll("nav a")].some(a => a.style.display !== "none");
        sec.style.display = visible ? "" : "none";
      });
    });
  }

  /* ── Mobile sidebar toggle ── */
  const hamburger = document.querySelector(".hamburger");
  const overlay   = document.querySelector(".overlay");

  function openSidebar()  { sidebar?.classList.add("open");  overlay?.classList.add("show"); }
  function closeSidebar() { sidebar?.classList.remove("open"); overlay?.classList.remove("show"); }

  hamburger?.addEventListener("click", openSidebar);
  overlay?.addEventListener("click",   closeSidebar);

  /* ── Smooth scroll for TOC ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener("click", e => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target) { e.preventDefault(); target.scrollIntoView({ behavior: "smooth" }); }
    });
  });

  /* ── TOC active section ── */
  const headings = document.querySelectorAll("h2[id]");
  const tocLinks = document.querySelectorAll(".toc a");
  if (headings.length && tocLinks.length) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          tocLinks.forEach(a => a.classList.remove("active"));
          document.querySelector(`.toc a[href="#${e.target.id}"]`)?.classList.add("active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    headings.forEach(h => obs.observe(h));
  }

});
