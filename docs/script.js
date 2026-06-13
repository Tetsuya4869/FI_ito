document.addEventListener("DOMContentLoaded", function () {

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
      errorColor: "#ff7b72",
    });
  }

  /* ── Sidebar mobile toggle ── */
  const sidebar  = document.querySelector(".sidebar");
  const hamburger = document.querySelector(".hamburger");
  const overlay  = document.querySelector(".overlay");

  function openSidebar()  { sidebar?.classList.add("open");  overlay?.classList.add("show"); }
  function closeSidebar() { sidebar?.classList.remove("open"); overlay?.classList.remove("show"); }

  hamburger?.addEventListener("click", openSidebar);
  overlay?.addEventListener("click",   closeSidebar);

  /* ── Active nav link ── */
  const current = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".sidebar nav a").forEach(a => {
    const href = a.getAttribute("href")?.split("/").pop();
    if (href === current || (current === "" && href === "index.html")) {
      a.classList.add("active");
    }
  });

  /* ── Smooth scroll for TOC ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener("click", e => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });

  /* ── Section highlight on scroll ── */
  const headings = document.querySelectorAll("h2[id]");
  const tocLinks = document.querySelectorAll(".toc a");
  if (headings.length && tocLinks.length) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          tocLinks.forEach(a => a.classList.remove("active"));
          const active = document.querySelector(`.toc a[href="#${e.target.id}"]`);
          active?.classList.add("active");
        }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    headings.forEach(h => obs.observe(h));
  }

});
