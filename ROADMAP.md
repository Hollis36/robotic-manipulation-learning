# Learning Roadmap

## Phase 1: Concept Foundations

- [x] Create the repository plan.
- [x] Scaffold repository metadata.
- [x] Add chapter folders and learner-owned note templates.
- [x] Implement deterministic Python examples for transforms, kinematics, differential IK, ICP, grasp scoring, RRT, PD control, perception flow, and gridworld RL.
- [x] Verify all examples with pytest and run scripts.

## Phase 2: Chapter Study Loop

For each chapter:

1. Read the local PDF chapter.
2. Fill in `notes.md` in Chinese using my own words.
3. Run the related casebook example.
4. Record the implementation lesson and remaining questions.
5. Decide whether the chapter needs a Drake lab.

Status: full-course overview completed via adapted `dse-loop`; chapter-by-chapter deep study continues from Chapter 2.

### Chapter Progress

| Chapter | First-pass notes | Exercises | Casebook link | Next action |
| --- | --- | --- | --- | --- |
| Ch1 Introduction | Done | Started | Conceptual | Check Drake docs and move to Ch2 |
| Ch2 Robot setup | Scaffolded | Not started | Future | Study robot model formats |
| Ch3 Basic pick-and-place | Scaffolded | Not started | `001`, `002`, `003` | Fill formulas while running cases |
| Ch4 Geometric pose estimation | Scaffolded | Not started | `004` | Study ICP failure modes |
| Ch5 Bin picking | Scaffolded | Not started | `005` | Extend grasp scoring |
| Ch6 Mobile manipulation | Waiting for source content | Not started | Future | Keep as future topic |
| Ch7 Motion planning | Scaffolded | Not started | `006` | Compare IK and RRT |
| Ch8 Manipulator control | Scaffolded | Not started | `007` | Study PD and impedance intuition |
| Ch9 Object detection and segmentation | Scaffolded | Not started | `008` | Define perception interface |
| Ch10 Deep perception | Scaffolded | Not started | `008` | Compare perception targets |
| Ch11 Reinforcement learning | Scaffolded | Not started | `009` | Expand gridworld environment |

## Phase 3: Drake Labs

- [ ] Document the local Drake or pydrake installation path.
- [ ] Add environment checks so Drake examples skip cleanly when unavailable.
- [ ] Port Chapter 3 pick-and-place ideas into a Drake lab.
- [ ] Port Chapter 4 and Chapter 5 perception examples into simulated point-cloud workflows.
- [ ] Add a motion-planning lab for Chapter 7.

## Phase 4: Public GitHub Polish

- [x] Review README and casebook entries for public clarity.
- [x] Add deep course companion, external resources, learning tracks, Drake setup, and capstone portfolio docs.
- [x] Add repository quality scoring and GitHub Actions tests.
- [x] Add small output plots where they clarify the idea.
- [x] Add process storyboards for core iterative examples.
- [x] Add a Jupyter Book learning path for interactive study.
- [x] Add GitHub Pages publishing for the Jupyter Book.
- [x] Create a GitHub repository.
- [x] Push a stable version into `main`.
