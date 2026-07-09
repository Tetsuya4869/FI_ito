#!/usr/bin/env python3
"""KaTeX 区切り記号の対応漏れを検査する (IMPROVEMENTS.md A-4)。

throwOnError:false のため壊れた数式は黙って素通りする。
ファイル単位で $ / $$ / \\( \\) / \\[ \\] の対応を数え、奇数なら警告。

使い方:  python3 tools/check_katex.py
"""
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent.parent / "docs"


def main() -> int:
    problems = []
    for p in sorted(DOCS.glob("*.html")):
        text = p.read_text(encoding="utf-8")
        # script/style 内は数式でないので除外
        text = re.sub(r"<script[\s\S]*?</script>", "", text)
        text = re.sub(r"<style[\s\S]*?</style>", "", text)

        dollars = text.count("$")
        if dollars % 2 != 0:
            problems.append(f"{p.name}: '$' が奇数個 ({dollars}) — 閉じ忘れの可能性")
        # \\[6pt] のような LaTeX の行間指定（\\ 直後の [ ）は区切りではないので除外
        open_br = len(re.findall(r"(?<!\\)\\\[", text))
        close_br = len(re.findall(r"(?<!\\)\\\]", text))
        if open_br != close_br:
            problems.append(f"{p.name}: \\[ ({open_br}) と \\] ({close_br}) の数が不一致")
        if len(re.findall(r"(?<!\\)\\\(", text)) != len(re.findall(r"(?<!\\)\\\)", text)):
            problems.append(f"{p.name}: \\( と \\) の数が不一致")

    if problems:
        print(f"NG: {len(problems)} 件")
        for x in problems:
            print("  -", x)
        return 1
    print("OK: KaTeX 区切り記号の対応異常なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
