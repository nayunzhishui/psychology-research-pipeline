---
name: cog-neuro-deep-reading
description: Local subskill for close reading of one level-3 or level-4 cognitive neuroscience paper at a time, producing a Chinese reading note, one reading-matrix row and evidence linked into the review evidence outline. Use only inside psych-cog-neuro-review after screening and full-text verification.
---

# 认知神经科学的精读与阅读笔记

## 目标

把一篇 3–4 级全文读透，产出四样东西：
1. 一篇给人读的阅读笔记；
2. 阅读矩阵和机制矩阵里的行；
3. 挂到证据提纲里的证据；
4. 必要时更新知识库的概念卡。

这是本工作流唯一的逐篇精读入口。方法子 skill 负责跨研究的方法评价，机制综合负责跨研究整合，来源对齐只做复核。

## 开始前读

同一会话里已经读过的，不用重复读：
1. `../../references/literature-operations-contract.md`；
2. `../../references/deep-reading-contract.md`：三轮阅读、七章节检查清单、四样东西的分工；
3. `../../references/reading-note-style.md`：笔记写成什么样；
4. `../../references/knowledge-vault-contract.md`：第一次写笔记，或要新建节点时读；
5. 项目的规则和模板，有的话以项目为准；以及样板笔记。

## 一篇文献的步骤

1. **开工核对**
   - 核对候选编号、阅读层级、研究家族；
   - 核对 PDF 身份：题名、作者、DOI 要与题录一致；
   - 旧笔记和旧摘录只当线索；
   - 项目还没有知识库的，先按 `../knowledge-vault/SKILL.md` 的“第一次建库”初始化，只做一次；
   - 证据提纲还没有骨架的，先按 `../../references/deep-reading-contract.md` 第 7 节建骨架，标“初稿”，请用户确认；
   - 没有全文的，标“受阻”，停在这一步。
2. **第一轮：定位。** 读题录、摘要、引言、讨论、结论和参考文献，边读边记“事实 + 页码”。
3. **第二轮：方法、数据与结果。**
   - 逐项记下范式、对照条件、试次、采集参数、预处理、伪迹和试次排除、ROI 或全脑、时间窗或频带、多重比较；
   - 行为、主观、神经和生理结果分开记，零结果和相反结果也记；
   - 脑图、波形、时频图做反向阅读；
   - 主要结果用 `scripts/check_reported_stats.py` 验算（`../../references/reading-note-style.md` 6.1），对不上的先查、再算，能判定的当场判定。
4. **第三轮：批判与写作转化。**
   - 把“作者声称”“结果显示”“我的机制推断”分开；
   - 检查有没有反向推断，有没有跨模态尺度的跳跃；
   - 对照七章节检查清单确认查清。
   读完三轮、动笔之前先**补课**：按 `../knowledge-vault/SKILL.md` 的“动笔前补课”，把这篇用到的概念、工具、结局、方法和样本过一遍；库里没有讲义或讲义不够的，联网查资料写成讲义。
5. **写阅读笔记**，用 `../../templates/reading_card.md`：
   - 先写“研究怎么做”（含“范式与模态”）和“主要发现”；
   - 再写评价和用处；
   - 最后写“30 秒看懂”。

   写之前先看 `../../references/reading-note-example-d1.md`（3 级看 `reading-note-example-d2.md`）和 `../../references/writing-before-after.md`。按 `reading-note-style.md` 第 0 节分三个区写：讲解区只讲这篇做了什么、发现了什么、数字是什么意思，一段最多一句限定；研究的局限写在“我的评价”；查过、算过仍定不下来的小出入写在“疑问与待核”。先把事实和页码列成底稿，再写成给新同学看的段落。每条发现的段落末尾空一格，加块编号。
6. **连知识库**：知识库靠这一步一篇一篇长起来，不能省。按 `../knowledge-vault/SKILL.md` 的“每写完一篇笔记”做七步：
   - 列节点、查重、新建或补讲义（动笔前已经做了的，这里只补漏）；
   - 补关联、写证据；
   - 连回笔记、记一笔。
7. **填阅读矩阵和机制矩阵**，各写一行：
   - 给人看的几列：一句话结论、研究概况、主要章节、其他章节与主张、证据强度、笔记路径；
   - 七章节状态和三轮状态。
8. **挂证据提纲**
   - 方向按 `../../references/deep-reading-contract.md` 第 7 节的定义判断：检验了这条主张、结果一致就是“支持”；“限定”只用于结果本身划出了主张成立的边界，不是“这篇有局限”。
   - 在对应主张下加证据行，更新证据概述和证据强度；
   - 机制主张的措辞，不超过设计和模态允许的上限；
   - 做问题涌现检查（`../../references/deep-reading-contract.md` 第 7 节第 5 条）：新问题、问题的新角度、相反结果、结构问题，以及找不到合适主张的发现，都记进结构改良记录（模板 `../../templates/结构改良记录模板_structure_findings.csv`），不自己加主张。
9. **收尾**
   - 运行 `scripts/check_reading_outputs.py`（命令见 `../../references/reading-note-style.md` 第 7 节），本篇的问题清零；“数字核对”页列出的数字逐条回原文看。
   - 这篇是核心文献的，登记进引文追踪种子表，按 `../../references/literature-operations-contract.md` 4.1 做前向和后向追踪；读参考文献时看到的相关文献，也登记进候选表。
   - 在笔记的“提取记录”里写执行人和日期，状态写“已读全文，单人提取”；
   - 需要第二人核对的，交给核对人。
   - 交接记录写成完整的中文句子：读了哪篇，笔记在哪里，挂到了哪几条主张，还有什么待核。不用内部缩写、代号和“父核”“子任务”这类过程用语，用户要能直接看懂。

一次任务只做一篇 4 级文献，或最多三篇 3 级文献。不要为了赶进度压缩笔记。

## 每批结束后

每读完一批（或每天结束时）运行一次，不必每篇都跑。`<skill>` 指本 skill 的目录。

```text
python <skill>/scripts/format_reading_matrix.py --矩阵 <阅读矩阵> --知识库 <主题>知识库 --文章结构 <论文结构.md> --全文目录 <PDF文件夹>
python <skill>/scripts/export_evidence_outline.py --提纲目录 <证据提纲文件夹> --知识库 <主题>知识库 --输出csv <主张证据对应表_claim_evidence_map.csv>
python <skill>/scripts/spreading_activation.py --知识库 <主题>知识库
python <skill>/scripts/check_reading_outputs.py --根 <库根目录> --知识库 <主题>知识库 --模板 <阅读笔记模板> --矩阵 <阅读矩阵> --输出 <自检.xlsx>
```

第三个脚本（激活扩散）约每 10 篇或每周运行一次即可。第四个是自检，报告里的问题改完再收尾；矩阵问题按项目的取值表改，解释写进单元格批注或笔记。

每批结束时还要做两件事：
- 把这一批的结构改良记录按章节汇总给用户，等用户决定要不要改问题和结构（`../../references/deep-reading-contract.md` 第 7 节第 5 条）；
- 引文追踪种子表里还有“待做”或“待续”的种子，运行 `python <skill>/scripts/citation_tracking.py --种子表 <引文追踪种子表.csv> --输出目录 <引文追踪原始导出目录> --候选表 <候选文献表.csv> --检索记录 <检索记录.csv>`，新增的题录照常筛选。

## 认知神经覆盖层

在公共要求之外，要核验：
- 任务、对照和试次；
- 模态与采集；
- 预处理；
- 伪迹处理和试次排除；
- ROI 还是全脑；
- 时间窗或频带；
- 多重比较校正；
- 分析灵活性；
- 交叉验证和数据泄漏；
- 反向推断；
- 跨模态尺度。

## 完成条件

- 自检脚本对本篇报告的问题已清零：没有句号后或连着排的页码，讲解区没有项目代号和内部用语，块编号前有空格，矩阵受控字段都在取值表里。
- 七章节和领域覆盖层都有状态和 PDF 页码。
- 知识库已按七步更新，新建或补过的节点卡都写成了讲义，笔记里放了补课框，“提取记录”里写明新建和更新了哪些节点。
- 零、相反和混合结果，方法不透明处，以及替代解释，都没有删。
- `professor_briefing_status` 只有在公共合同的全部条件满足后，才能标为“就绪”。

## 不能做的

- 不伪造页码、结果、坐标、时间窗、样本或统计方法。
- 没有全文，不写笔记，不做强引用。
- 机制措辞不超过设计和模态允许的上限。
