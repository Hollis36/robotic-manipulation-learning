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

## GitHub Pages Publication Check

Checked on 2026-06-14 after enabling public Pages deployment.

Current state:

- Repository: `Hollis36/robotic-manipulation-learning`
- Visibility: public
- GitHub account plan reported by `gh api user`: free
- Pages API: enabled with `build_type: workflow`
- Public URL: `https://hollis36.github.io/robotic-manipulation-learning/`
- First verified deployed commit: `2a86495`
- GitHub Actions `tests`: passed
- GitHub Actions `pages`: build passed, uploaded the Pages artifact, and deployed successfully
- Verified public routes: `/`, `/favicon.ico`, `/labs.html`, `/book/`, and `/lite/lab/index.html?path=notebooks/02_transforms_kinematics_ik.ipynb`

The deploy gate is:

```yaml
if: github.ref == 'refs/heads/main' && github.event.repository.private == false
```

This keeps automatic deployment tied to a public repository. If the repository is made private again, the workflow can still validate the build artifact, but deploy will be skipped unless the account plan and repository settings support private Pages.

To recheck the published site:

```bash
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/favicon.ico
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/labs.html
curl -I -L https://hollis36.github.io/robotic-manipulation-learning/book/
```
