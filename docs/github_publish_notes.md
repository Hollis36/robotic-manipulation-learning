# GitHub Publish Notes

## Recommended Repository Name

`robotic-manipulation-learning`

## First Publish Flow

After local verification:

```bash
git remote add origin git@github.com:<your-user>/robotic-manipulation-learning.git
git push -u origin build-learning-repo-v1
```

Then open a pull request from `build-learning-repo-v1` into `main`, or merge locally after review.

## Visibility

Use a public repository if the content remains learner-owned and the source PDFs stay ignored. Use a private repository if you later include copied source material or large local datasets.

## GitHub Pages Readiness Check

Checked on 2026-06-14.

Current state:

- Repository: `Hollis36/robotic-manipulation-learning`
- Visibility: private
- GitHub account plan reported by `gh api user`: free
- Pages API: `GET /repos/Hollis36/robotic-manipulation-learning/pages` returns 404
- Public URL: `https://hollis36.github.io/robotic-manipulation-learning/` returns 404
- Latest checked commit: `4bac389`
- GitHub Actions `tests`: passed
- GitHub Actions `pages`: build passed and uploaded the Pages artifact
- GitHub Actions `pages` deploy job: skipped because `.github/workflows/pages.yml` intentionally gates deployment to public repositories

The deploy gate is:

```yaml
if: github.ref == 'refs/heads/main' && github.event.repository.private == false
```

This means the current 404 is a publication-setting issue, not a site-build issue.

To publish the online learning platform:

1. Make the repository public, or use a GitHub plan that supports Pages deployment from private repositories.
2. In repository Settings -> Pages, use GitHub Actions as the Pages source if GitHub asks for a source.
3. Rerun the `pages` workflow on `main`.
4. Verify:

```bash
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/favicon.ico
```

Do not remove the private-repository deploy gate unless the repository is intended to be published or the account plan has been verified to support private Pages safely.
