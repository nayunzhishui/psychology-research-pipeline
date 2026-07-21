# Current project profile

Snapshot: 2026-07-21. Treat as audited intake evidence, not a frozen protocol.

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
- Preserve the verified item map and raw-item rescoring rules in `measurement-map.json`; obtain original SPSS syntax only as corroborating provenance.
- Determine whether NSSI aggregates are continuous, ordinal, count-like, binary, or weighted composites and inspect zero inflation/skew.
- Verify measurement invariance feasibility and item consistency across waves.
- Decide whether the primary estimand is within-person dynamics, between-person differences, or both.
- Use “sex differences” unless the questionnaire demonstrably measured gender.

## Current data-audit red flags

These are audit triggers, not final error determinations:

- ID格式规范化后，871行三波一致、11行存在可由两波多数支持的单波差异、无三波全部不同；原始ID不进入分析数据，11行仍应由来源匹配表复核。
- 性别按问卷记为sex（1男、2女）；T1有869个有效编码、13个缺失，跨波有效编码有41行不一致。主分析仅使用T1有效编码，其他波次不用于覆盖或强制纠正。
- CES-D为20题、1–4分，反向题4/8/12/16；T1/T2旧总分完全复现，T3改由有效原始题项重算。
- NSSI为18种方式，次数0–3、程度0–4、逐项乘积后求和；T3越界原始单元格仅在派生数据中置缺失，并预设两部分敏感性分析。
- 父母冲突采用18题统一高冲突方向，反向题1/3/4/5/7/9/13/16。禁止跨波混用旧“解决情况/冲突程度”派生变量。
- 学号首字母仅派生匿名学校代码a–i；九所学校不支持常规聚类稳健推断，使用学校固定效应或敏感性分析。

## Method candidates, not decisions

Primary candidate: three-variable RI-CLPM with clearly separated within-person paths and between-person random-intercept correlations. Compare a theoretically justified CLPM only as a sensitivity/contrast, not as proof. Consider longitudinal mediation and multi-group sex comparison only if identification, power, measurement invariance, and outcome distribution are adequate. Predefine robust alternatives for zero-heavy NSSI and run simulation-based power/sensitivity checks.
