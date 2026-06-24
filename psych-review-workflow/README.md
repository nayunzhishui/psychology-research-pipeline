# psych-review-workflow

通用心理学综述写作 skill。默认用于“宽研究方向 → 聚焦综述方向 → 正式检索 → Zotero 入库 → 文献分类与评级 → 深度阅读矩阵 → HTML 文献星图 → APA 综述写作 → 原文引用对齐 → 模拟投稿审稿”的完整流程。

## 设计定位

- 以中文工作流为主，保留必要英文检索式、术语、APA 引文和题录字段。
- 可用于人格功能损害综述，也可复用到健康心理学、临床心理学、发展心理学、认知神经科学等方向。
- 强制保留检索日志、题录来源、筛查理由、证据位置、引用对齐和模拟审稿记录。
- 不处理未授权全文获取，不绕过权限，不保存账号密码、验证码、cookie 或 token。

## 推荐启动提示词

```markdown
请使用 psych-review-workflow。

我的初始研究方向是：<写方向>。
当前阶段：<宽方向探索 / 已聚焦正式综述 / 修改已有综述>。
目标用途：<开题 / 学位论文 / 中文期刊 / 英文期刊 / 课程作业>。
重点人群或范围：<如青少年、大学生、临床样本、普通人群>。
Zotero collection：<collection 名称，如无则写“先不导入 Zotero”>。
输出要求：中文为主，保留英文术语；需要文献矩阵、HTML 文献星图、综述正文和引用对齐表。

请先完成宽方向探索，给出 2–5 个可聚焦综述方向，不要直接大规模下载全文。
```

## 人格功能损害综述示例启动提示词

```markdown
请使用 psych-review-workflow。

我的初始研究方向是：人格功能损害与青少年自伤/自杀、情绪调节的关系。
当前阶段：宽方向探索。
目标用途：研究生阶段综述和后续开题准备。
重点范围：人格功能水平、DSM-5 AMPD/LPFS、STiP-5.1、LoPF-Q、OPD 结构轴，青少年或年轻人，自伤/自杀风险，情绪调节机制。
语言：中文为主，英文术语和 APA 引文准确保留。
Zotero：先给候选文献清单，正式聚焦后再导入本地 Zotero。

请先搜集代表性综述、测量/方法文章和近年核心实证文章，帮助我聚焦综述方向。
```

## 主要产物

- `00_exploration/scoping_brief.md`
- `01_protocol/review_protocol.md`
- `02_search/search_log.csv`
- `03_library/zotero_manifest.csv`
- `04_screening/relevance_ratings.csv`
- `05_matrix/evidence_matrix.csv`
- `06_synthesis/claim_evidence_map.csv`
- `07_star_map/reference_star_map.html`
- `09_manuscript/manuscript.md`
- `10_alignment/source_alignment_table.csv`
- `11_submission/simulated_reviews.md`

## 使用边界

真实投稿、账号登录、MFA、验证码、付费确认、数据库权限决策由用户处理。该 skill 只能做合法、可审计、可复现的研究辅助工作。
