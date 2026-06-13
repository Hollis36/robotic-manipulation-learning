# Learning Roadmap

## Phase 1: Concept Foundations

- [x] Create the repository plan.
- [x] Scaffold repository metadata.
- [ ] Add chapter folders and learner-owned note templates.
- [ ] Implement deterministic Python examples for transforms, kinematics, differential IK, ICP, grasp scoring, RRT, PD control, perception flow, and gridworld RL.
- [ ] Verify all examples with pytest and run scripts.

## Phase 2: Chapter Study Loop

For each chapter:

1. Read the local PDF chapter.
2. Fill in `notes.md` in Chinese using my own words.
3. Run the related casebook example.
4. Record the implementation lesson and remaining questions.
5. Decide whether the chapter needs a Drake lab.

## Phase 3: Drake Labs

- [ ] Document the local Drake or pydrake installation path.
- [ ] Add environment checks so Drake examples skip cleanly when unavailable.
- [ ] Port Chapter 3 pick-and-place ideas into a Drake lab.
- [ ] Port Chapter 4 and Chapter 5 perception examples into simulated point-cloud workflows.
- [ ] Add a motion-planning lab for Chapter 7.

## Phase 4: Public GitHub Polish

- [ ] Review README and casebook entries for public clarity.
- [ ] Add small output plots where they clarify the idea.
- [ ] Create a GitHub repository.
- [ ] Push this branch and merge a stable version into `main`.

