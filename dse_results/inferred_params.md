# Inferred Learning Loop Space

This is an adapted use of `dse-loop`: each iteration is a chapter-learning pass rather than an EDA design point.

| Parameter | Source | Default | Inferred Range | Reasoning |
| --- | --- | --- | --- | --- |
| Unit | local PDFs | chapter | Preface, Ch1-Ch11, Appendix A-C | The source material is already split by chapter. |
| Depth | user request | full overview before teaching | section map, concept map, casebook connection, teaching hook | Covers the whole text without copying source prose. |
| Objective | user request | maximize teaching readiness | 0-100 coverage score | A unit is ready when it has topic summary, dependencies, artifacts, and teaching order. |
| Constraint | copyright and repo hygiene | no source reproduction | paraphrase only, PDFs ignored, raw extraction not committed | The GitHub repo should remain learner-owned. |

