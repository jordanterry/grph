# Homebrew Integration

This directory contains the Homebrew formula and automation for distributing gfx-cli via Homebrew.

## Setup Instructions

### 1. Create a GitHub Personal Access Token

Create a fine-grained PAT with access to `jordanterry/homebrew-tap`:
- Go to GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
- Create a token with **Contents: Read and write** permission for `jordanterry/homebrew-tap`

### 2. Add the Token as a Secret

In the `jordanterry/gefx-cli` repository:
- Go to Settings → Secrets and variables → Actions
- Add a new secret: `HOMEBREW_TAP_TOKEN` with the PAT value

### 3. Set Up Your Tap Repository

In `jordanterry/homebrew-tap`:

1. Create the `Formula/` directory:
   ```bash
   mkdir -p Formula
   ```

2. Copy `update-formula.yml` to `.github/workflows/update-formula.yml`

3. Enable Actions in the repository settings

## How It Works

1. You push a tag like `v0.2.0` to gefx-cli
2. The `release.yml` workflow:
   - Builds the Python package
   - Creates a GitHub release with artifacts
   - Triggers a `repository_dispatch` event to the tap
3. The tap's `update-formula.yml` workflow:
   - Downloads the release tarball
   - Calculates the SHA256 hash
   - Updates the formula with the new version and hash
   - Commits and pushes the changes

## Creating a Release

```bash
# Update version in pyproject.toml first, then:
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git tag v0.2.0
git push && git push --tags
```

## Manual Formula Update

If you need to update the formula manually:

```bash
# Get the SHA256 of a release
curl -sL https://github.com/jordanterry/gefx-cli/archive/refs/tags/v0.1.0.tar.gz | sha256sum
```

Then update `gfx-cli.rb` with the new version and SHA256.
