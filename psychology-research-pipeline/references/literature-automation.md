# 文献自动化契约

## 顺序

`plan-search` → 在数据库实际执行并填写 `检索记录_search_log.csv` → `import-evidence` → `dedupe-evidence` → `cluster-studies` → 人工筛选与证据标注 → `audit-evidence-coverage` → `build-retrieval-queue`。定稿前用 `refresh-search` 比较更新导出。

顺序开始前必须先通过 `prepare-presearch`；其 `ready_for_search=false` 时只允许完善协议、环境和目标集合，不得运行数据库检索或把题录写入正式候选集。

自动化只处理检索计划、已有合法导出、元数据和审计文件；不代替数据库登录、权限判断、人工纳排、全文判断或方法质量评价。

Chrome用于依赖现有登录态或Connector的可见页面操作；CLI负责队列、哈希和产物合同。`sync-zotero` 先核验本地API，再导出BibTeX、规范化题录并核验本地PDF头与哈希；Zotero未运行时必须返回明确阻断，不得伪造同步成功。

Zotero 同步只允许一个已核验的精确集合。记录 collection name/key、目标配置来源、集合题录数和导出哈希；禁止使用全库导出填充正式候选表。空集合预检应返回 `ready-empty`，不得覆盖已有候选记录。

正式纳排使用两个独立reviewer；分歧必须由第三位裁决者处理。`audit-screening` 输出双人一致/分歧/裁决依据、PRISMA计数和按研究设计选择工具的偏倚风险待评表，缺任一独立判断或裁决时返回`blocked`。

## 题录导入

支持 CSV、RIS、BibTeX、PubMed XML、Crossref JSON 和 OpenAlex JSON。每次导入写入原始文件绝对路径、格式、记录数和 SHA-256；规范化 DOI 并生成稳定 `candidate_id`。原始导出不可改写，人工标注应在筛选表或其派生副本完成。

身份优先级：DOI → PMID → OpenAlex ID → 规范化题名+首作者+年份。身份键只用于题录去重，不等于独立研究。

## 同研究多报告

`cluster-studies` 根据队列名、国家、样本量、招募年份和首作者生成候选对。输出始终为 `review_status=pending`，不得自动合并。复核应比较样本来源、招募时间、波次、基线样本量、干预/队列名称和作者重合。

## 证据覆盖

`schemas/evidence-coverage.schema.json` 定义核心与非核心 slot、最低文献数和证据条件，可显式要求撤稿核验状态和全文核验状态。撤稿或撤回记录不计入覆盖；本课题包的核心 slot 只接受 `retraction_status=clear` 且 `fulltext_status=verified` 的证据。核心 slot 未满足时命令返回 `blocked`/退出码 3，并输出覆盖矩阵和缺口备忘录。

## 全文和更新

全文队列优先直接实证，其次测量与方法，再到综述和背景；撤稿/撤回记录不入队。`access_route` 只允许人工授权或开放获取路径。`refresh-search` 输出新增、元数据变化和本轮未出现的旧记录；“未出现”只标记，不删除历史证据。
