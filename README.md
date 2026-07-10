# thesis-to-devto

Converts thesis LaTeX appendix subfiles into **Dev.to-ready Markdown** with
math rendered via Dev.to's KaTeX liquid tags (`{% katex %}` / `{% katex inline %}`).

## Layout

```
thesis-to-devto/
  scripts/convert.py     # the reusable pipeline
  src/<name>/            # copied LaTeX source + assets (originals are never touched)
  output/<name>/
    <name>.md            # paste this into the Dev.to editor
    assets/*.png         # upload these; the editor gives you a URL per image
```

## What the pipeline does

1. Extracts the body between `\begin{document}` and `\end{document}`.
2. Expands thesis macros KaTeX can't read: `\bm`->`\boldsymbol`, `\argmin/\argmax/\cov/\var`->`\operatorname` forms; strips `\label`/`\autoref`.
3. Resolves `\autocite{key}` / `\cite{key}` to numbered `[n]` references built from `bibliography.bib`.
4. Runs Pandoc (LaTeX -> GitHub Markdown) for prose, headings, math, figures.
5. Converts math delimiters to KaTeX liquid tags; rewrites figure paths to `./assets/`.
6. Adds Dev.to YAML front matter (`published: false`) and a References section.

## Run it on another appendix

```bash
# 1. copy the source + assets into src/
cp /path/to/thesis/appendix/methods/pipelines/mcmc.tex src/mcmc/
cp /path/to/thesis/appendix/methods/pipelines/assets/mcmc/*.png src/mcmc/assets/

# 2. convert
python3 scripts/convert.py src/mcmc/mcmc.tex output/mcmc \
  --title "Your Title Here" \
  --tags "machinelearning, math, eeg, tutorial" \
  --bib /path/to/thesis/bibliography.bib \
  --slug mcmc

# 3. copy figures into the output folder
cp src/mcmc/assets/*.png output/mcmc/assets/
```

## Notes / limits

- Dev.to has **no equation numbering or `\ref`** — cross-references were removed. If a
  proof needs to point back to an equation, add prose ("the whitening step above").
- Multi-line aligned environments (`align`, `cases`) render but each line is its own
  `{% katex %}` block; check alignment-heavy appendices by eye.
