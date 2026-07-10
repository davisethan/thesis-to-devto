#!/usr/bin/env python3
"""
LaTeX (thesis subfile) -> Dev.to-ready Markdown converter.

Pipeline:
  1. Extract the body between \\begin{document} and \\end{document}.
  2. Expand custom macros so KaTeX can render them (\\bm -> \\boldsymbol, etc.).
  3. Tokenize \\autocite / \\cite so they survive Pandoc, then resolve them
     to numbered [n] references built from bibliography.bib.
  4. Run Pandoc (LaTeX -> GitHub Markdown) for prose, headings, math, figures.
  5. Post-process:
       - display math  $$...$$   -> {% katex %}...{% endkatex %}
       - inline  math  $...$     -> {% katex inline %}...{% endkatex %}
       - rewrite figure paths to ./assets/<basename>
       - append a References section
       - prepend Dev.to YAML front matter

Usage:
  convert.py <input.tex> <output_dir> --title "..." --tags a,b,c --bib <bibliography.bib>
"""

import argparse, os, re, subprocess, sys, shutil

# ---------------------------------------------------------------- bib parsing
def parse_bib(bib_path):
    """Very small BibTeX reader -> {key: {field: value}}."""
    if not bib_path or not os.path.exists(bib_path):
        return {}
    text = open(bib_path, encoding="utf-8", errors="ignore").read()
    entries = {}
    # split on @type{ ... } top-level entries
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),", text):
        key = m.group(2).strip()
        start = m.end()
        # find matching closing brace for this entry
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            if text[i] == "{": depth += 1
            elif text[i] == "}": depth -= 1
            i += 1
        body = text[start:i-1]
        fields = {}
        for fm in re.finditer(r"(\w+)\s*=\s*", body):
            fname = fm.group(1).lower()
            j = fm.end()
            if j >= len(body): break
            if body[j] == "{":
                depth = 1; k = j+1
                while k < len(body) and depth > 0:
                    if body[k] == "{": depth += 1
                    elif body[k] == "}": depth -= 1
                    k += 1
                fields[fname] = body[j+1:k-1].strip()
            else:  # bare / quoted value up to comma
                mm = re.match(r'"([^"]*)"|([^,]+)', body[j:])
                if mm:
                    fields[fname] = (mm.group(1) or mm.group(2)).strip()
    # NOTE: key captured above; store fields
        entries[key] = fields
    return entries

def format_reference(fields):
    author = re.sub(r"\s+and\s+", ", ", fields.get("author", "")).strip()
    title  = fields.get("title", "").strip()
    year   = fields.get("year", "").strip()
    pub    = fields.get("publisher", fields.get("booktitle", fields.get("journal", ""))).strip()
    parts = []
    if author: parts.append(author)
    if year:   parts.append(f"({year})")
    if title:  parts.append(f"*{title}*.")
    if pub:    parts.append(f"{pub}.")
    return " ".join(parts)

# ---------------------------------------------------------------- tex prep
def extract_body(tex):
    m = re.search(r"\\begin\{document\}(.*)\\end\{document\}", tex, re.S)
    return m.group(1) if m else tex

def collect_citations(body):
    """Replace \\autocite{a,b} / \\cite{a,b} with sentinel tokens; return order."""
    order = []
    def repl(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        toks = []
        for k in keys:
            if k not in order:
                order.append(k)
            toks.append(f"@@CITE:{k}@@")
        return "".join(toks)
    body = re.sub(r"\\autocite\{([^}]*)\}", repl, body)
    body = re.sub(r"\\cite\{([^}]*)\}", repl, body)
    return body, order

def expand_macros(body):
    # KaTeX has no \bm; use \boldsymbol
    body = re.sub(r"\\bm(?![a-zA-Z])", r"\\boldsymbol", body)
    # thesis-local operators (KaTeX-safe replacements)
    body = re.sub(r"\\argmin(?![a-zA-Z])", r"\\operatorname*{arg\\,min}", body)
    body = re.sub(r"\\argmax(?![a-zA-Z])", r"\\operatorname*{arg\\,max}", body)
    body = re.sub(r"\\cov(?![a-zA-Z])", r"\\operatorname{cov}", body)
    body = re.sub(r"\\var(?![a-zA-Z])", r"\\operatorname{var}", body)
    # drop \label / \autoref cross-refs that don't apply outside the thesis
    body = re.sub(r"\\label\{[^}]*\}", "", body)
    body = re.sub(r"\\autoref\{[^}]*\}", "the figure", body)
    return body

# ---------------------------------------------------------------- pandoc
def run_pandoc(tex_body):
    proc = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "gfm", "--wrap=none"],
        input=tex_body, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit("pandoc failed")
    return proc.stdout

# ---------------------------------------------------------------- md post
def to_katex(md):
    # Pandoc gfm emits display math as \[ ... \] and inline as \( ... \).
    # Also handle $$...$$ / $...$ in case another pandoc target is used.
    # --- display first ---
    md = re.sub(r"\\\[(.+?)\\\]",
                lambda m: "\n{% katex %}\n" + m.group(1).strip() + "\n{% endkatex %}\n",
                md, flags=re.S)
    md = re.sub(r"\$\$(.+?)\$\$",
                lambda m: "\n{% katex %}\n" + m.group(1).strip() + "\n{% endkatex %}\n",
                md, flags=re.S)
    # --- inline ---
    md = re.sub(r"\\\((.+?)\\\)",
                lambda m: "{% katex inline %}" + m.group(1).strip() + "{% endkatex %}",
                md, flags=re.S)
    md = re.sub(r"(?<!\$)\$([^\$\n]+?)\$(?!\$)",
                lambda m: "{% katex inline %}" + m.group(1).strip() + "{% endkatex %}",
                md)
    return md

def guard_math_underscores(md):
    """Dev.to runs Markdown before KaTeX, so `_`/`^` inside inline math get eaten
    as emphasis (e.g. `}_i` opens <em>), corrupting subscripts. A space AFTER the
    operator stops CommonMark from treating it as an emphasis opener, while KaTeX
    ignores math-mode spaces so sub/superscripts still bind. Applied inside every
    katex span."""
    def fix(m):
        body = re.sub(r"([_^])", r"\1 ", m.group(2))
        return m.group(1) + body + m.group(3)
    return re.sub(r"(\{% katex(?: inline)? %\})(.*?)(\{% endkatex %\})",
                  fix, md, flags=re.S)

def fix_images(md, image_base="./assets"):
    # rewrite any image path to <image_base>/<basename>
    base = image_base.rstrip("/")
    return re.sub(r"!\[([^\]]*)\]\(([^)]+)\)",
                  lambda m: f"![{m.group(1)}]({base}/{os.path.basename(m.group(2))})",
                  md)

def resolve_citations(md, order, entries):
    idx = {k: i+1 for i, k in enumerate(order)}
    # emit as a superscript-style token first, then merge adjacent runs
    md = re.sub(r"@@CITE:([^@]+)@@", lambda m: f"@@N{idx.get(m.group(1).strip(),'?')}@@", md)
    # merge adjacent tokens @@N1@@@@N2@@ -> @@N1, 2@@
    prev = None
    while prev != md:
        prev = md
        md = re.sub(r"@@N([\d, ]+)@@@@N([\d, ]+)@@", r"@@N\1, \2@@", md)
    md = re.sub(r"@@N([\d, ]+)@@", lambda m: f"[{m.group(1)}]", md)
    lines = ["", "## References", ""]
    for k in order:
        n = idx[k]
        ref = format_reference(entries.get(k, {})) or k
        lines.append(f"{n}. {ref}")
    return md + "\n" + "\n".join(lines) + "\n"

def yaml_quote(s):
    """Double-quote a YAML scalar so colons, #, etc. are safe."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'

def front_matter(title, tags, series=""):
    taglist = ", ".join(t.strip() for t in tags.split(",") if t.strip())
    fm = [f"title: {yaml_quote(title)}", "published: false", f"tags: {taglist}"]
    if series:
        fm.append(f"series: {yaml_quote(series)}")
    return ("---\n" + "\n".join(fm) + "\n---\n\n"
            f"> *Adapted from an appendix of my MS thesis. "
            f"Equations render via Dev.to's KaTeX support.*\n\n")

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("output_dir")
    ap.add_argument("--title", required=True)
    ap.add_argument("--tags", default="machinelearning, datascience, computerscience, tutorial")
    ap.add_argument("--bib", default="")
    ap.add_argument("--slug", default="")
    ap.add_argument("--image-base", default="./assets",
                    help="Prefix for image links. For GitHub sync use the repo-root-relative "
                         "path, e.g. 'posts/assets/csp'.")
    ap.add_argument("--series", default="", help="dev.to series name to group posts.")
    args = ap.parse_args()

    tex = open(args.input, encoding="utf-8").read()
    entries = parse_bib(args.bib)

    body = extract_body(tex)
    body, order = collect_citations(body)
    body = expand_macros(body)

    md = run_pandoc(body)
    md = to_katex(md)
    md = guard_math_underscores(md)
    md = fix_images(md, args.image_base)
    md = resolve_citations(md, order, entries)
    md = front_matter(args.title, args.tags, args.series) + md

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, "assets"), exist_ok=True)
    slug = args.slug or os.path.splitext(os.path.basename(args.input))[0]
    out_md = os.path.join(args.output_dir, f"{slug}.md")
    open(out_md, "w", encoding="utf-8").write(md)

    print(f"wrote {out_md}")
    print(f"citations resolved: {len(order)}")

if __name__ == "__main__":
    main()
