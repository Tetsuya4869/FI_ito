#!/usr/bin/env python3
"""docs/ 内の HTML のリンク切れ・アンカー切れを検査する (IMPROVEMENTS.md A-3)。

使い方:  python3 tools/check_links.py
終了コード: 問題ゼロなら 0、問題ありなら 1
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"

HREF_RE = re.compile(r'href="([^"]+)"')
ID_RE = re.compile(r'id="([^"]+)"')


def main() -> int:
    pages = sorted(DOCS.glob("*.html"))
    ids = {p.name: set(ID_RE.findall(p.read_text(encoding="utf-8"))) for p in pages}
    # script.js が注入するサイドバーのリンクも検査対象
    script = (DOCS / "script.js").read_text(encoding="utf-8")

    problems = []

    def check(src: str, href: str) -> None:
        if href.startswith(("http://", "https://", "mailto:")) or "${" in href:
            return  # 外部リンクと JS テンプレート文字列は対象外
        if href.startswith("#"):
            if href[1:] and href[1:] not in ids.get(src, set()):
                problems.append(f"{src}: 存在しないアンカー {href}")
            return
        target, _, frag = href.partition("#")
        if target and not (DOCS / target).exists():
            problems.append(f"{src}: リンク切れ {target}")
        elif frag and frag not in ids.get(target, set()):
            problems.append(f"{src}: {target} に無いアンカー #{frag}")

    for p in pages:
        for href in HREF_RE.findall(p.read_text(encoding="utf-8")):
            check(p.name, href)
    for href in HREF_RE.findall(script):
        check("script.js(サイドバー)", href)

    if problems:
        print(f"NG: {len(problems)} 件")
        for x in problems:
            print("  -", x)
        return 1
    print(f"OK: {len(pages)} ページ + サイドバー、リンク・アンカー異常なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
