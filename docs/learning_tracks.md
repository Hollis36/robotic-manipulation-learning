# Learning Tracks

Use these tracks depending on the goal of a study session. They share the same chapter material but optimize for different outcomes.

## Track A: Fast Concept Pass

**Goal:** understand the manipulation stack quickly.

**Time:** 1-2 weeks.

| Step | Read | Run | Output |
| --- | --- | --- | --- |
| 1 | Ch1 | none | One-page task decomposition |
| 2 | Ch2 | none | Robot system block diagram |
| 3 | Ch3 | `001`, `002`, `003` | Transform and IK notes |
| 4 | Ch4-Ch5 | `004`, `005` | Perception-to-grasp pipeline sketch |
| 5 | Ch7-Ch8 | `006`, `007` | Planning vs control comparison |
| 6 | Ch9-Ch11 | `008`, `009` | Learning and perception summary |

## Track B: Coding-First Casebook

**Goal:** turn each chapter into executable intuition.

**Time:** 3-5 weeks.

| Case | Modification Task | Skill Tested |
| --- | --- | --- |
| `001` | Add inverse transform and tests | frame reasoning |
| `002` | Add link endpoint visualization | kinematics |
| `003` | Add unreachable-target handling | numerical IK |
| `004` | Add outliers and compare error | geometric perception |
| `005` | Add collision penalty | grasp scoring |
| `006` | Add rectangular obstacles | planning |
| `007` | Compare underdamped and overdamped gains | control |
| `008` | Add mask noise and downstream effect | perception interface |
| `009` | Add Q-learning baseline | RL environment design |

## Track C: Drake Transition

**Goal:** move from NumPy examples to Drake labs.

**Time:** 4-8 weeks after Track A.

| Step | Repository Area | Outcome |
| --- | --- | --- |
| 1 | `docs/drake_setup.md` | pydrake environment check |
| 2 | Chapter 2 `drake_labs/` | load a robot model |
| 3 | Chapter 3 `drake_labs/` | inspect frames and model instances |
| 4 | Chapter 3 `drake_labs/` | solve a simple IK problem |
| 5 | Chapter 4 `drake_labs/` | create a synthetic point cloud |
| 6 | Chapter 7 `drake_labs/` | run a basic planning example |

## Track D: Portfolio Track

**Goal:** produce GitHub-visible projects that demonstrate competence.

**Time:** 8-12 weeks.

| Project | Chapters | Public Artifact |
| --- | --- | --- |
| Planar pick-and-place simulator | Ch3 | animation, tests, explanation |
| Synthetic pose-estimation lab | Ch4 | ICP comparison and failure cases |
| Bin-picking loop simulator | Ch5 | grasp scoring + retry logic |
| RRT manipulation planner | Ch7 | path visualization and benchmark |
| Contact-control toy lab | Ch8 | controller comparison |
| Perception-to-grasp demo | Ch9-Ch10 | mask perturbation study |
| RL grasping gridworld | Ch11 | learning curve and policy analysis |

## Track E: Research Reading Track

**Goal:** read papers without losing the course foundation.

**Entry condition:** complete Track A.

Process:

1. Pick one stack layer.
2. Read one survey or curated list entry.
3. Identify the course chapter it extends.
4. Add one note to `docs/research_notes.md`.
5. Add one experiment idea to `docs/capstone_portfolio.md`.

