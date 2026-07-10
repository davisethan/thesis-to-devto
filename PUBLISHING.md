# Publishing to dev.to

The `posts/` articles publish to [dev.to](https://dev.to) automatically on every
push, via the [`publish-devto`](https://github.com/sinedied/publish-devto) GitHub
Action (`.github/workflows/publish.yml`). Images are hosted from this repo (relative
links are rewritten to GitHub raw URLs at publish time).

## One-time setup

1. **Get a dev.to API key.** dev.to → Settings → Extensions → "DEV Community API Keys"
   (or https://developers.forem.com/api/#section/Authentication/api_key). Generate one.
2. **Add it as a secret.** Repo → Settings → Secrets and variables → Actions →
   **New repository secret**, named `DEVTO_TOKEN`, value = your API key.

That's it. The workflow in `.github/workflows/publish.yml` runs on every push that
touches `posts/`.

## Publishing a post

1. Add/edit a markdown file under `posts/` (must have a `title` in its front matter).
2. Put its images under `posts/assets/<slug>/` and link them **relative to the post
   file** (which lives in `posts/`), e.g. `![caption](assets/csp/scms.png)` — the action
   resolves these against the file's folder and swaps them for raw GitHub URLs.
3. Commit and push to `main`.

The action then:
- creates the article on dev.to (as a **draft** while `published: false`),
- writes the new dev.to `id` back into the file's front matter via an auto-commit,
- so future edits **update** that same article instead of duplicating it.

### Avoiding duplicate drafts (important)

dev.to has no notion of "the same file" — it only matches on the `id` in front
matter. Two rules keep you from creating duplicates:

1. **`git pull` after every push.** The action auto-commits the `id` back to the
   repo. If you don't pull, your local file still has no `id`, and your next push
   creates a *new* article.
2. **Regenerate with `--prev`.** The converter rewrites front matter from scratch,
   which would drop the `id`. Passing `--prev posts/<slug>.md` carries the existing
   `id`/`date` forward so the push updates instead of duplicating.

If you already have duplicates: delete the extra drafts on dev.to (Dashboard →
each article → Delete), keep one per post, then `git pull` so the surviving `id`
is in your local file before the next regenerate.

### Draft vs. live

- `published: false` → created as a private draft you can preview on dev.to first.
- Flip to `published: true` and push again → it goes live. On publish the action also
  records a `date` field.

## Posts (series: "Feature Engineering: Electroencephalogram")

Both start as drafts (`published: false`) and share the same `series`, so dev.to
groups them with next/previous navigation.

- `posts/csp.md` — Common Spatial Pattern correctness proof. Figures in `posts/assets/csp/`.
- `posts/ts.md` — Tangent Space of the SPD manifold. Figures in `posts/assets/ts/`,
  including two commutative diagrams (`cd-*.png`) that were rendered from the thesis
  tikz-cd source because KaTeX/dev.to can't display tikz-cd natively.

To go live: change `published: false` to `published: true` in a post, commit, push.

## Adding the rest of the appendices

Generate each new post with the converter in `scripts/convert.py`, pointing
`--image-base` at the repo-relative asset path:

```bash
python3 scripts/convert.py <appendix>.tex /tmp/stage \
  --title "..." --tags "machinelearning, datascience, computerscience, tutorial" \
  --bib <bibliography.bib> --slug mcmc --image-base "assets/mcmc" \
  --prev posts/mcmc.md          # keeps dev.to id on re-runs; no-op for a new post
cp /tmp/stage/mcmc.md posts/mcmc.md
mkdir -p posts/assets/mcmc && cp <appendix-assets>/*.png posts/assets/mcmc/
git add posts && git commit -m "feat: add mcmc post" && git push
```

## Optional: push from your laptop

You don't need this — the Action handles publishing — but if you want to preview a
push locally: `npm i -g @sinedied/devto-cli`, copy `.env.example` to `.env`, fill in
`DEVTO_TOKEN`, then `dev push --dry-run` to preview or `dev push` to publish.
