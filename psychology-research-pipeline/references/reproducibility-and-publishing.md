# 可复现环境与投稿构建

## R 环境

仓库中的 `renv.lock` 是可解析的初始化种子，不代表任一真实分析环境已经冻结。复制到具体研究运行后，在该运行目录执行：

```powershell
& <Rscript.exe> <skill>/scripts/bootstrap_r_environment.R
```

脚本建立项目本地库、安装核心包并用 `renv::snapshot(type = "all")` 替换种子锁文件。只有新的锁文件、Rscript 哈希、包版本清单与生成代码一起保存后，才能声明环境已冻结。

`templates/_targets.R` 组织 R 内部依赖图；Python 十二阶段 gate 仍是唯一跨阶段调度器。`targets` 不得绕过数据冻结、结果核验或人工批准。

## 文献数据链

- Crossref 与 OpenAlex 返回值先规范化，再执行 DOI、题名、年份和作者冲突检查；冲突不得静默覆盖。
- PDF 先用 PyMuPDF 检查结构和可提取文本；需要章节/参考文献结构时再连接 GROBID。
- ASReview 及类似主动学习仅输出排序队列，`decision` 固定为 `human-review-required`。

## 投稿构建

`templates/manuscript.qmd` 是 Quarto 单源模板，正文只能读取已验证结果和 `claim-verified` 证据。Quarto/papaja/Pandoc 缺失时明确标记降级，禁止把普通格式转换称为可复现构建。

最后用 `pipeline.py export-ro-crate` 为选定产物生成哈希和关系图；原始敏感数据及 `.private/` 文件不得进入 RO-Crate 或投稿包。
