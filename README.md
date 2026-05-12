# pypvfs

**`pypvfs`** is the PyPI distribution name for **Pinnacle Technology PVFS** — a virtual filesystem used for physiological recordings. This is **not** related to the historical HPC “Parallel Virtual File System” or other unrelated “PVFS” acronyms.

After installation you import the **`pvfs_tools`** Python package (same module layout as in the former Morelia monolith):

```bash
pip install pypvfs
```

```python
from pvfs_tools.Core.pvfs_data_file import PvfsDataFile
```

## Optional extras

| Extra | Purpose |
|-------|---------|
| `video` | WebM/VP8 export (`WebMWriter` uses PyAV). `pip install "pypvfs[video]"` |
| `test` | `pytest` + `av` for running the test suite locally |
| `examples` | `pyedflib` + `av` for the Tk GUI EDF and WebM examples |

## Native library

The package ships platform-specific native libraries under `pvfs_tools.Core` (`.dll` on Windows, `.so` on Linux) when present in the wheel or source tree. If your platform binary is missing, build from `src/pvfs_tools/Core/` using `build_linux.sh` (Linux/WSL) or `build_pvfs_x64.ps1` (under `src/pvfs_tools/` on Windows), then from this repository root run `pip install -e .`.

## Examples (repository `examples/`)

Requires a working `pypvfs` install; GUI examples need a display.

| Script | Extra deps | Description |
|--------|------------|-------------|
| `examples/pvfs_create_cli.py` | — | CLI to create a synthetic PVFS file |
| `examples/pvfs_to_edf_converter.py` | `pyedflib` | Tk GUI: PVFS → EDF+ |
| `examples/pvfs_to_video_converter.py` | `pypvfs[video]` | Tk GUI: PVFS video → WebM |

```bash
pip install pyedflib
python examples/pvfs_to_edf_converter.py
```

## Documentation

- Quick reference: [docs/pvfsQuickStart.txt](docs/pvfsQuickStart.txt)

## Tests

```bash
pip install -e ".[test]"
pytest
```

## Repository

Source and issues: see **Repository** URL in `pyproject.toml`.

## Publishing releases

Do **not** rely on `twine upload` from a developer machine for routine releases (credentials drift and audit pain). Use the GitHub Action instead.

1. **Configure [trusted publishing](https://docs.pypi.org/trusted-publishers/)** on PyPI for this GitHub repository and workflow `publish.yml` (OIDC — no `PYPI_API_TOKEN` in repo secrets unless you choose that path).
2. **Bump** `version` in `pyproject.toml`, commit, then create and push a **version tag** matching your policy, e.g. `v0.1.2`:
   ```bash
   git tag v0.1.2
   git push origin v0.1.2
   ```
   Pushing tag `v*` runs [`.github/workflows/publish.yml`](.github/workflows/publish.yml): builds **sdist + wheels** on Ubuntu and Windows, merges artifacts, and uploads with `pypa/gh-action-pypi-publish`.
3. **Manual run:** Actions → **Publish to PyPI** → *Run workflow* (same build/upload path).

**Note:** `ptech-morelia` already uses a similar pattern (tag push + matrix build + OIDC) in its `packaging` workflow — keep both projects on the same release habit so versions stay aligned when you cut coordinated releases.
