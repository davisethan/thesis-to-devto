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
    # strip BibTeX capitalization-protection braces, e.g. {Markov} -> Markov
    clean = lambda s: s.replace("{", "").replace("}", "").strip()
    names = fields.get("author", "")
    is_editor = False
    if not names:                       # edited volumes use `editor`, not `author`
        names = fields.get("editor", "")
        is_editor = bool(names)
    author = clean(re.sub(r"\s+and\s+", ", ", names))
    if is_editor and author:
        author += " (Eds.)"
    title  = clean(fields.get("title", ""))
    year   = clean(fields.get("year", ""))
    pub    = clean(fields.get("publisher", fields.get("booktitle", fields.get("journal", ""))))
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
    # KaTeX has no \nicefrac; \frac takes the same two brace args
    body = re.sub(r"\\nicefrac(?![a-zA-Z])", r"\\frac", body)
    # Pandoc reads a leading [..] in an equation as an optional arg and DROPS it
    # (e.g. convolution `[w * x](i)`). Use \lbrack/\rbrack so it survives (and it
    # also avoids the `](` Markdown-link collision on dev.to).
    body = re.sub(r"\[([^\[\]]*\\circledast[^\[\]]*)\]", r"\\lbrack \1 \\rbrack", body)
    # \allowbreak is a spacing hint KaTeX doesn't know; drop it
    body = re.sub(r"\\allowbreak(?![a-zA-Z])", " ", body)
    # thesis-local operators (KaTeX-safe replacements)
    body = re.sub(r"\\argmin(?![a-zA-Z])", r"\\operatorname*{arg\\,min}", body)
    body = re.sub(r"\\argmax(?![a-zA-Z])", r"\\operatorname*{arg\\,max}", body)
    body = re.sub(r"\\cov(?![a-zA-Z])", r"\\operatorname{cov}", body)
    body = re.sub(r"\\var(?![a-zA-Z])", r"\\operatorname{var}", body)
    # dev.to has no theorem/definition environments; render as bold-led prose
    body = re.sub(r"\\begin\{definition\}", r"\\textbf{Definition.} ", body)
    body = re.sub(r"\\end\{definition\}", "", body)
    # drop \label; turn \autoref into label-aware prose ("the figure/table/equation")
    body = re.sub(r"\\label\{[^}]*\}", "", body)
    def autoref(m):
        prefix = m.group(1).split(":")[0].lower()
        noun = {"figure": "figure", "table": "table", "equation": "equation",
                "appendix": "appendix"}.get(prefix, "section")
        return f"the {noun}"
    body = re.sub(r"\\autoref\{([^}]*)\}", autoref, body)
    return body

def fix_ref_caps(md):
    """Capitalize 'the figure/table/equation/...' when it starts a sentence
    (a \\autoref that opened a sentence would otherwise be lowercase)."""
    return re.sub(r"(^|[.!?]\s+)the (figure|table|equation|section|appendix)",
                  lambda m: m.group(1) + "The " + m.group(2), md, flags=re.M)

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

def guard_math_linebreaks(md):
    """Dev.to runs Markdown before KaTeX, and CommonMark collapses `\\\\` (the row
    break in aligned/matrix) into a single `\\` — so KaTeX sees no line break and
    multi-line equations render on one row. Doubling to `\\\\\\\\` on disk means
    CommonMark hands KaTeX a real `\\\\`. Applied inside every katex block."""
    bs = "\\"
    def fix(m):
        return m.group(1) + m.group(2).replace(bs * 2, bs * 4) + m.group(3)
    return re.sub(r"(\{% katex(?: inline)? %\})(.*?)(\{% endkatex %\})",
                  fix, md, flags=re.S)

def guard_math_escapes(md):
    """CommonMark treats `\\{`, `\\}`, `\\|` as escaped punctuation and strips the
    backslash before KaTeX runs, breaking `\\Big\\{`, set braces, and norms. Doubling
    the backslash on disk makes CommonMark leave a single `\\` for KaTeX. Runs AFTER
    guard_math_linebreaks so it only touches single backslashes (lookbehind), not the
    already-quadrupled `\\\\` row breaks. Applied inside every katex block."""
    def fix(m):
        body = re.sub(r"(?<!\\)\\([{}|])", lambda x: "\\\\" + x.group(1), m.group(2))
        return m.group(1) + body + m.group(3)
    return re.sub(r"(\{% katex(?: inline)? %\})(.*?)(\{% endkatex %\})",
                  fix, md, flags=re.S)

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

def carry_over_fields(prev_path):
    """Read `id`/`date` (and published state) from an already-published post so
    regenerating updates that dev.to article instead of creating a duplicate.
    devto-cli writes `id` back into the file on first publish."""
    keep = {}
    if prev_path and os.path.exists(prev_path):
        txt = open(prev_path, encoding="utf-8").read()
        m = re.match(r"---\n(.*?)\n---", txt, re.S)
        if m:
            for key in ("id", "date", "published"):
                km = re.search(rf"^{key}:\s*(.+)$", m.group(1), re.M)
                if km:
                    keep[key] = km.group(1).strip()
    return keep

def front_matter(title, tags, series="", keep=None):
    keep = keep or {}
    taglist = ", ".join(t.strip() for t in tags.split(",") if t.strip())
    fm = []
    if keep.get("id"):
        fm.append(f"id: {keep['id']}")           # preserving this prevents duplicates
    fm.append(f"title: {yaml_quote(title)}")
    fm.append(f"published: {keep.get('published', 'false')}")
    fm.append(f"tags: {taglist}")
    if series:
        fm.append(f"series: {yaml_quote(series)}")
    if keep.get("date"):
        fm.append(f"date: {keep['date']}")
    return ("---\n" + "\n".join(fm) + "\n---\n\n"
            "> *Adapted from an appendix of my MS thesis.*\n\n")

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
    ap.add_argument("--prev", default="",
                    help="Path to the already-published post (e.g. posts/<slug>.md) to "
                         "carry its dev.to `id`/`date` forward and avoid duplicates.")
    args = ap.parse_args()

    tex = open(args.input, encoding="utf-8").read()
    entries = parse_bib(args.bib)

    body = extract_body(tex)
    body, order = collect_citations(body)
    body = expand_macros(body)

    md = run_pandoc(body)
    md = to_katex(md)
    md = guard_math_linebreaks(md)
    md = guard_math_escapes(md)
    md = guard_math_underscores(md)
    md = fix_ref_caps(md)
    md = fix_images(md, args.image_base)
    md = resolve_citations(md, order, entries)
    md = front_matter(args.title, args.tags, args.series,
                      carry_over_fields(args.prev)) + md

    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, "assets"), exist_ok=True)
    slug = args.slug or os.path.splitext(os.path.basename(args.input))[0]
    out_md = os.path.join(args.output_dir, f"{slug}.md")
    open(out_md, "w", encoding="utf-8").write(md)

    print(f"wrote {out_md}")
    print(f"citations resolved: {len(order)}")

if __name__ == "__main__":
    main()
