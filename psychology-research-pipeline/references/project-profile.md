# Current project profile

Snapshot: 2026-06-23. Treat as intake evidence, not a frozen protocol.

## Workspace

Project root: `D:\codex\workspace\早期青少年父母冲突、抑郁与自伤之间的动态发展关系及性别差异`

Observed source material:

- SPSS file `2018、2019和2020怀化和韶山数据全.sav`: 882 rows, 673 columns, three apparent waves, repeated raw items and derived scores.
- Word instrument `施测问卷 （测量工具名）.doc`: adolescent survey with demographics, parent communication/care, school connectedness, CES-D depression, life satisfaction, friendship quality, social anxiety, 18-method NSSI, self-esteem, interparental conflict, and national identity.
- Seed paper on cumulative interpersonal risk, NSSI, suicide attempts, four waves, CLPM/RI-CLPM, and sex differences.
- Seed paper on identity confusion, alienation, NSSI, three-wave RI-CLPM, longitudinal mediation, and sex comparison.
- `build_matlab_learning_doc.py` appears unrelated to the research question; exclude unless provenance shows otherwise.

## Supported direction

Primary direction: dynamic longitudinal relations among interparental conflict, depressive symptoms, and adolescent NSSI, with sex differences, using three-wave Chinese school data.

Observed derived variables include parent-conflict resolution, conflict degree/total, depression, NSSI frequency/severity/level, and sex at T1-T3. Demographic, SES, family structure, parental communication, school connectedness, parental care, social anxiety, friendship quality, self-esteem, and life satisfaction may support covariate or sensitivity analyses, but must not be added opportunistically.

## Provisional questions

1. At the within-person level, do deviations in interparental conflict, depressive symptoms, and NSSI predict subsequent deviations in each other across three waves?
2. Does depressive symptom change temporally mediate the association between interparental conflict and later NSSI, and are reverse paths plausible?
3. Do structural paths differ by measured sex after measurement comparability is established?

## Required verification before methods freeze

- Confirm actual wave dates and intervals; the filename alone is insufficient.
- Confirm stable participant identifiers, duplicates, attrition, and whether 882 is the merged or complete-case sample.
- Recover exact scale provenance, scoring keys, reverse items, valid ranges, and derivation syntax for every T1-T3 score.
- Determine whether NSSI aggregates are continuous, ordinal, count-like, binary, or weighted composites and inspect zero inflation/skew.
- Verify measurement invariance feasibility and item consistency across waves.
- Decide whether the primary estimand is within-person dynamics, between-person differences, or both.
- Use “sex differences” unless the questionnaire demonstrably measured gender.

## Method candidates, not decisions

Primary candidate: three-variable RI-CLPM with clearly separated within-person paths and between-person random-intercept correlations. Compare a theoretically justified CLPM only as a sensitivity/contrast, not as proof. Consider longitudinal mediation and multi-group sex comparison only if identification, power, measurement invariance, and outcome distribution are adequate. Predefine robust alternatives for zero-heavy NSSI and run simulation-based power/sensitivity checks.
