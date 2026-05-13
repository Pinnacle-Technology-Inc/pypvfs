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

The package ships platform-specific native libraries under `pvfs_tools.Core` (`.dll` on Windows, `.so` on Linux). On PyPI you receive a prebuilt wheel for your platform, so `pip install pypvfs` does **not** require a C++ toolchain.

If you install from source (sdist or a checkout), `pip` will invoke [`scikit-build-core`](https://scikit-build-core.readthedocs.io/) which compiles `src/pvfs_tools/Core/pvfs.cpp` and `pvfs_wrapper.cpp` via CMake. You will need:

- CMake ≥ 3.15 (pip installs `cmake` from PyPI into the isolated build env if your system lacks it)
- A C++17 compiler (`g++`/`clang++` on Linux/macOS, MSVC 2019+ on Windows)

```bash
pip install -e ".[test]"   # builds the native libs and installs in editable mode
pytest
```

## Examples

The runnable example scripts ship **inside the installed package**, so they are available immediately after `pip install pypvfs` — no repo clone required.

| Module | Extra deps | Description |
|--------|------------|-------------|
| `pvfs_tools.examples.pvfs_create_cli` | — | CLI to create a synthetic PVFS file |
| `pvfs_tools.examples.pvfs_to_edf_converter` | `pypvfs[examples]` (`pyedflib`) | Tk GUI: PVFS → EDF+ |
| `pvfs_tools.examples.pvfs_to_video_converter` | `pypvfs[video]` (`av`) | Tk GUI: PVFS video → WebM |

```bash
# Locate or list the installed examples
pypvfs-examples
pypvfs-examples --list

# Copy them out to a directory you can edit freely
pypvfs-examples --copy-to ./my-pvfs-examples

# Or run any of them directly
python -m pvfs_tools.examples.pvfs_create_cli --help
python -m pvfs_tools.examples.pvfs_to_edf_converter
python -m pvfs_tools.examples.pvfs_to_video_converter
```

The same scripts also live at the top of the GitHub repo under [`examples/`](examples/) for easy browsing; both copies are identical, the package build just relocates them into `pvfs_tools/examples/` so they are usable without cloning.

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

Step-by-step (tags, GitKraken, PyPI checks): **[docs/RELEASE.md](docs/RELEASE.md)**.

Do **not** rely on `twine upload` from a developer machine for routine releases (credentials drift and audit pain). Use the GitHub Action instead.

1. **Configure [trusted publishing](https://docs.pypi.org/trusted-publishers/)** on PyPI for this GitHub repository and workflow `publish.yml` (OIDC — no `PYPI_API_TOKEN` in repo secrets unless you choose that path).
2. **Bump** `version` in `pyproject.toml`, commit, then create and push a **version tag** matching your policy, e.g. `v1.0.2`:
   ```bash
   git tag v1.0.2
   git push origin v1.0.2
   ```
   Pushing tag `v*` runs [`.github/workflows/publish.yml`](.github/workflows/publish.yml): [`cibuildwheel`](https://cibuildwheel.pypa.io/) builds a `manylinux_2_28_x86_64` wheel inside the PyPA manylinux Docker image and a `win_amd64` wheel on a Windows runner, then uploads both (plus the sdist) with `pypa/gh-action-pypi-publish`. The manylinux image guarantees a low glibc baseline so the published Linux wheel works on RHEL/CentOS/Rocky/Alma 8+, Ubuntu 20.04+, Debian 11+, and Amazon Linux 2023 — not just the build host.
3. **Manual run:** Actions → **Publish to PyPI** → *Run workflow* (same build/upload path).

**Note:** `ptech-morelia` already uses a similar pattern (tag push + matrix build + OIDC) in its `packaging` workflow — keep both projects on the same release habit so versions stay aligned when you cut coordinated releases.
