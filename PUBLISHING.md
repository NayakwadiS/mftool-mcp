# Publishing a New Version

This document describes the full, repeatable process for releasing a new version of
`mftool-mcp` to **PyPI** and registering/updating it on the **MCP Registry**
(`io.github.NayakwadiS/mftool-mcp`).

> ⚠️ Never commit secrets. Auth tokens live only in local, git-ignored files
> (`.mcpregistry_github_token`, `.mcpregistry_registry_token`) or environment
> variables, and are never written into this repo's tracked files.

---

## Prerequisites (one-time setup)

1. **Python build tools**
   ```powershell
   python -m pip install --upgrade build twine
   ```

2. **`mcp-publisher` CLI** — the official MCP Registry publishing tool.
   Download the appropriate binary for your OS from the
   [modelcontextprotocol/registry releases](https://github.com/modelcontextprotocol/registry/releases)
   page and make sure it's on your `PATH` (verify with `mcp-publisher --help`).

3. **PyPI account access** to the `mftool-mcp` project (maintainer or token holder).

---

## Step-by-Step Release Process

### 1. Bump the version number (keep everything in sync)

Update the version string in **all** of the following files to the same new version
(e.g. `0.5.0`):

| File | Field |
|---|---|
| `pyproject.toml` | `project.version` |
| `src/mftool_mcp/__init__.py` | `__version__` |
| `server.json` | `packages[0].version` (PyPI package version) |
| `README.md` | PyPI badge version (`img.shields.io/badge/pypi-vX.Y.Z-orange`) |

Also bump `server.json`'s top-level `"version"` field (the *registry entry* version —
this can be a different, incrementing number, e.g. `1.2.0` → `1.3.0`; it does not need
to match the PyPI package version, but should always increase).

> 💡 Tip: `grep -rn "0\.4\.0"` (previous version) across the repo to make sure you
> didn't miss a spot.

### 2. Update README changelog / tool list (if applicable)

If new tools or capabilities were added, update the **Tools Available** table in
`README.md` so the registry listing / PyPI page stays accurate.

### 3. Build the package

```powershell
cd "C:\Drive D\mftool-mcp"
python -m build
```

This produces `dist/mftool_mcp-<version>-py3-none-any.whl` and
`dist/mftool_mcp-<version>.tar.gz`.

### 4. Validate `server.json` before publishing

```powershell
mcp-publisher validate .\server.json
```

Expect: `✅ server.json is valid`

### 5. Publish the package to PyPI

Using an API token (recommended — generate one at
https://pypi.org/manage/account/token/ scoped to the `mftool-mcp` project):

```powershell
$env:TWINE_USERNAME = "__token__"
$env:TWINE_PASSWORD = "<your-pypi-token>"   # never commit this
python -m twine upload dist/mftool_mcp-<version>* --non-interactive
Remove-Item Env:\TWINE_USERNAME
Remove-Item Env:\TWINE_PASSWORD
```

Confirm it's live: `https://pypi.org/project/mftool-mcp/<version>/`

> The MCP Registry cross-checks the `<!-- mcp-name: ... -->` comment in the PyPI
> package's README against `server.json`'s `name` field, so the PyPI release must
> exist **before** you publish to the registry.

### 6. Authenticate `mcp-publisher` (if not already logged in, or token expired)

Registry auth tokens are short-lived (weeks/months). If publishing fails with an
auth error, re-login:

```powershell
mcp-publisher login github
```

This prints a device code and URL, e.g.:

```
To authenticate, please:
1. Go to: https://github.com/login/device
2. Enter code: XXXX-XXXX
3. Authorize this application
Waiting for authorization...
```

Open the URL in a browser, enter the code, and click **Authorize**. The CLI will
print `Successfully authenticated!` and save a fresh token locally to
`.mcpregistry_github_token` / `.mcpregistry_registry_token` (both git-ignored).

### 7. Publish `server.json` to the MCP Registry

```powershell
mcp-publisher publish
```

Expect output similar to:

```
Publishing to https://registry.modelcontextprotocol.io...
✓ Successfully published
✓ Server io.github.NayakwadiS/mftool-mcp version <registry-version>
```

### 8. Verify the update is live

```powershell
curl.exe -s "https://registry.modelcontextprotocol.io/v0/servers?search=mftool-mcp"
```

Check that the newest entry has:
- `"version"` matching the registry version you set in `server.json`
- `"packages"[0].version"` matching the PyPI version you published
- `"_meta"."io.modelcontextprotocol.registry/official"."isLatest": true`

### 9. Commit and push the version bump

```powershell
git add pyproject.toml src/mftool_mcp/__init__.py server.json README.md
git commit -m "Release vX.Y.Z: <short summary of changes>"
git push origin <branch-name>
```

Open/merge a PR into `master` so the repository history matches what's published.

---

## Quick Reference Checklist

- [ ] Bump version in `pyproject.toml`, `__init__.py`, `server.json` (package + top-level), README badge
- [ ] Update README tools table / changelog if needed
- [ ] `python -m build`
- [ ] `mcp-publisher validate ./server.json`
- [ ] `twine upload dist/...` → verify on PyPI
- [ ] `mcp-publisher login github` (only if token expired)
- [ ] `mcp-publisher publish`
- [ ] Verify via registry search API (`isLatest: true`)
- [ ] Commit + push + merge to `master`

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `mcp-publisher publish` fails with 401/403 | Registry token expired — re-run `mcp-publisher login github` |
| Registry rejects `server.json` | Run `mcp-publisher validate` first; check the PyPI version referenced actually exists and is public |
| `twine upload` fails with 403 | PyPI token invalid/expired or lacks permission for the `mftool-mcp` project — generate a new project-scoped token |
| Registry shows old version as `isLatest` | Double-check `server.json`'s top-level `version` was actually incremented before publishing |

