#!/usr/bin/env python3
"""
TS-specific preprocessing: the Tangent Space appendix wraps an aligned equation
and a tikz-cd commutative diagram side-by-side in a `tabular`. KaTeX can't render
tikz-cd, and Pandoc would mangle the tabular. So we:
  - keep the aligned equation as real display math, and
  - replace the commutative diagram with a pre-rendered image (compiled separately).
Run BEFORE convert.py.
"""
import re, sys

src, dst = sys.argv[1], sys.argv[2]
tex = open(src, encoding="utf-8").read()

# rendered diagram images (compiled from the tikzcd blocks), in document order
DIAGRAMS = [
    ("appendix/methods/pipelines/assets/ts/cd-left-invariant-field.png",
     "Commutative diagram: left-invariance of the vector field. Pullback to the "
     "identity and pushforward under left-translation commute."),
    ("appendix/methods/pipelines/assets/ts/cd-left-invariant-metric.png",
     "Commutative diagram: left-invariance of the Riemannian metric induced from "
     "the inner product on the Lie algebra."),
]

_idx = {"i": 0}

def replace_tabular(m):
    block = m.group(0)
    # extract the aligned display-math from the first minipage
    am = re.search(r"\\\[\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\\\]", block, re.S)
    aligned = am.group(1).strip() if am else ""
    # strip stray latex comments inside the math
    aligned = "\n".join(re.sub(r"(?<!\\)%.*$", "", ln).rstrip() for ln in aligned.splitlines())
    # FIX known thesis typo: (L_{(g^{-1}h^{-1}h}) -> (L_{g^{-1}h^{-1}h})
    aligned = aligned.replace("(L_{(g^{-1}h^{-1}h})", "(L_{g^{-1}h^{-1}h})")

    i = _idx["i"]; _idx["i"] += 1
    img, cap = DIAGRAMS[i] if i < len(DIAGRAMS) else ("", "")
    out = []
    if aligned:
        out.append("\\[\n\\begin{aligned}\n" + aligned + "\n\\end{aligned}\n\\]")
    fig = (
        "\\begin{figure}[!htbp]\n\\centering\n"
        + "\\includegraphics[width=0.5\\linewidth]{" + img + "}\n"
        + "\\caption[Commutative diagram]{" + cap + "}\n"
        + "\\end{figure}"
    )
    out.append(fig)
    return "\n\n".join(out) + "\n"

tex = re.sub(r"\\begin\{tabular\}.*?\\end\{tabular\}", replace_tabular, tex, flags=re.S)
open(dst, "w", encoding="utf-8").write(tex)
print(f"replaced {_idx['i']} tabular/tikz-cd block(s)")
