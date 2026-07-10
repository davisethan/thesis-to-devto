# thesis-to-devto

Turns LaTeX appendix subfiles from my MS thesis into **dev.to articles**. The
converter (`scripts/convert.py`) rewrites LaTeX into Markdown with math in dev.to's
KaTeX liquid tags (`{% katex %}` / `{% katex inline %}`), and the finished articles
in `posts/` **auto-publish to dev.to on every push** via a GitHub Action.

For the publishing setup (API key, secret, draft vs. live), see
[PUBLISHING.md](PUBLISHING.md). This file covers the converter.

## Layout

```
thesis-to-devto/
  posts/                     # the articles that publish to dev.to
    <slug>.md                #   one article per appendix (has YAML front matter)
    assets/<slug>/*.png      #   its figures, hosted from this repo
  scripts/
    convert.py               # LaTeX -> dev.to Markdown pipeline
    preprocess_ts.py         # renders tikz-cd diagrams to images (TS appendix)
  src/<slug>/                # copied LaTeX source + assets (thesis originals untouched)
  .github/workflows/         # publish-devto Action (runs on push to posts/)
  output/                    # scratch space for local conversions
```

## What the converter does

1. Extracts the body between `\begin{document}` and `\end{document}`.
2. Expands thesis macros KaTeX can't read: `\bm`->`\boldsymbol`, `\argmin/\argmax/\cov/\var`->`\operatorname` forms; strips `\label`/`\autoref`.
3. Resolves `\autocite{key}` / `\cite{key}` to numbered `[n]` references built from the thesis `bibliography.bib`.
4. Runs Pandoc (LaTeX -> GitHub Markdown) for prose, headings, math, and figures.
5. Converts math delimiters to KaTeX liquid tags and rewrites image links to a repo-relative path (`--image-base`).
6. Prepends dev.to YAML front matter (`title`, `tags`, `published: false`, optional `series`) and appends a References section.

## Add another appendix

```bash
# 1. copy the appendix source + its figures into src/
mkdir -p src/mcmc/assets
cp <thesis>/appendix/methods/pipelines/mcmc.tex        src/mcmc/
cp <thesis>/appendix/methods/pipelines/assets/mcmc/*.png src/mcmc/assets/

# 2. convert straight into posts/, with images pointed at the repo path
python3 scripts/convert.py src/mcmc/mcmc.tex /tmp/stage \
  --title "Your Title Here" \
  --tags "machinelearning, math, eeg, tutorial" \
  --series "Feature Engineering: Electroencephalogram" \
  --bib <thesis>/bibliography.bib \
  --slug mcmc --image-base "posts/assets/mcmc"
cp /tmp/stage/mcmc.md posts/mcmc.md
mkdir -p posts/assets/mcmc && cp src/mcmc/assets/*.png posts/assets/mcmc/

# 3. commit + push -> the Action publishes it as a draft
git add posts && git commit -m "feat: add mcmc post" && git push
```

Appendices with tikz-cd commutative diagrams (e.g. Tangent Space) need
`scripts/preprocess_ts.py` first, which renders each diagram to a PNG (KaTeX/dev.to
can't display tikz-cd) before the normal convert step.

## Current posts

Series **"Feature Engineering: Electroencephalogram"**:

- `posts/csp.md` — Common Spatial Pattern: a correctness proof.
- `posts/ts.md` — The tangent space of the SPD manifold for EEG classification.

Both are `published: false` (drafts) until flipped to `true`.

## Notes / limits

- dev.to has **no equation numbering or `\ref`** — cross-references are removed. If a
  proof needs to point back to a result, use prose ("the whitening step above").
- Multi-line aligned environments (`align`, `cases`) render, but each `{% katex %}`
  block is standalone; skim alignment-heavy appendices by eye.
- Relative image links only resolve once pushed to GitHub, since the Action rewrites
  them to `raw.githubusercontent.com` URLs and verifies each is reachable.
