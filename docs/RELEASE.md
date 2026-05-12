# Releasing `pypvfs` to PyPI

## Normal flow

1. Bump `version` in `pyproject.toml` and commit (e.g. on `integration` or `main`).
2. Create an annotated tag whose name starts with **`v`**, e.g. `v1.0.0`, on that commit.
3. **Push the tag to `origin`** (separate from pushing a branch). Example:
   ```bash
   git push origin v1.0.0
   ```
4. On GitHub: **Actions** → open **Publish to PyPI** → confirm a run started for the tag.
5. After green: check [PyPI project](https://pypi.org/project/pypvfs/) and `pip index versions pypvfs`.

## If nothing runs when you push the tag

| Check | What to do |
|-------|------------|
| Tag on GitHub? | **Code** → switch to **Tags** — `v1.0.0` must appear. If not, the tag never left your machine; push it explicitly. |
| Workflow on the tagged commit? | Browse the repo at tag `v1.0.0` — `.github/workflows/publish.yml` must exist on **that** commit. |
| Default branch | Merge workflow changes into the repo **default branch** (often `main`) so GitHub fully registers the workflow. **Run workflow** (manual) in the Actions tab only lists workflows present on the default branch. |
| Actions disabled? | **Settings** → **Actions** → **General** — workflows must be allowed. |
| Tag pattern | This repo expects tags like **`v1.0.0`**, not `1.0.0` (no `v`). |

## Manual test (no tag)

**Actions** → **Publish to PyPI** → **Run workflow** (uses the selected branch’s latest commit). Confirms build + PyPI trusted publishing without cutting a tag.

## PyPI trusted publishing

**PyPI** → your project → **Publishing** → **Add a new pending publisher** (GitHub → pick this repo → workflow file `publish.yml`). No long-lived API token in GitHub secrets is required when OIDC is configured.

### OIDC / “trusted publishing exchange failure” (e.g. HTTP 504)

PyPI may email errors like `OpenID Connect token retrieval failed: GitHub: OIDC token request failed (code=504, …)`. That is often a **transient GitHub outage or timeout** talking to the OIDC endpoint — **re-run the failed workflow** from the Actions tab.

If failures persist, ensure the workflow that runs `pypa/gh-action-pypi-publish` sets **`id-token: write` on the publish job** (see `.github/workflows/publish.yml`). GitHub’s default token does not mint OIDC tokens unless that permission is granted on the job that requests the token.

When a job sets `permissions:`, omitted scopes default to **no access** for that job — the publish job also needs **`actions: read`** (and **`contents: read`**) so it can **download** build artifacts before upload.
