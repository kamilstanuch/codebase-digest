# Publishing your digest to the understand-quickly registry

[`looptech-ai/understand-quickly`](https://github.com/looptech-ai/understand-quickly) is a public, machine-readable registry of code-knowledge and code-context artifacts. It indexes Codebase Digest output through its [`bundle@1`](https://github.com/looptech-ai/understand-quickly/blob/main/schemas/bundle@1.json) format so AI agents (Claude, Codex, Cursor via MCP) can resolve a repo URL to its digest.

Publishing is opt-in. The digest body stays in your repo and is fetched from `raw.githubusercontent.com`; the registry only stores a small JSON pointer.

## One-time setup

1. Register your repo with the registry — `npx @understand-quickly/cli add`, the [wizard](https://looptech-ai.github.io/understand-quickly/add.html), or a manual PR per the [registry CONTRIBUTING.md](https://github.com/looptech-ai/understand-quickly/blob/main/CONTRIBUTING.md).
2. Create a fine-grained GitHub PAT scoped to `looptech-ai/understand-quickly` only with `Repository dispatches: write`. Add it as the `UNDERSTAND_QUICKLY_TOKEN` secret in your repo.

## Workflow

Add the following as `.github/workflows/understand-quickly-publish.yml`. It runs `cdigest`, commits the digest to a dedicated `understand-quickly` branch (so the `content_url` is actually reachable), writes a small `bundle@1` sidecar pinned to that commit SHA, then hands off to the [`looptech-ai/uq-publish-action`](https://github.com/looptech-ai/uq-publish-action) Marketplace Action.

```yaml
name: understand-quickly publish
on:
  push:
    branches: [main]
jobs:
  publish:
    runs-on: ubuntu-latest
    permissions: { contents: write }   # needs write to publish digest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.x' }
      - run: python -m pip install codebase-digest
      - run: cdigest . -o markdown -f digest.md
      - name: Commit digest to understand-quickly branch
        run: |
          git config user.name 'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git checkout --orphan understand-quickly
          git rm -rf --cached . >/dev/null 2>&1 || true
          git add -f digest.md
          git commit -m "chore(uq): publish $(date -u +%Y-%m-%dT%H:%M:%SZ)"
          git push --force origin understand-quickly
          echo "UQ_SHA=$(git rev-parse HEAD)" >> "$GITHUB_ENV"
      - name: Build bundle@1 sidecar
        env:
          REPO: ${{ github.repository }}
          SHA: ${{ env.UQ_SHA }}
        run: |
          python - <<'PY'
          import datetime, json, os
          b = os.path.getsize('digest.md')
          repo, sha = os.environ['REPO'], os.environ['SHA']
          json.dump({
            'format': 'bundle@1',
            'manifest': {'tool': 'codebase-digest',
              'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'byte_count': b, 'token_estimate': b // 4, 'format': 'markdown'},
            'content_url': f'https://raw.githubusercontent.com/{repo}/{sha}/digest.md'
          }, open('digest.bundle.json', 'w'), indent=2)
          PY
      - uses: looptech-ai/uq-publish-action@v0.1.0
        with:
          graph-path: digest.bundle.json
          format: bundle@1
          token: ${{ secrets.UNDERSTAND_QUICKLY_TOKEN }}
```

## Notes

- Submission is opt-in and gated entirely on the secret being set; without `UNDERSTAND_QUICKLY_TOKEN` the Action only stamps metadata locally and exits cleanly.
- Only suitable for public repos (the digest is fetched from `raw.githubusercontent.com`).
- See the [producer protocol](https://github.com/looptech-ai/understand-quickly/blob/main/docs/integrations/protocol.md) for the full contract and [`DATA-LICENSE.md`](https://github.com/looptech-ai/understand-quickly/blob/main/DATA-LICENSE.md) for the data-grant semantics.
