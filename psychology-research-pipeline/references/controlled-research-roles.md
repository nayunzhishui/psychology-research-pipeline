# 受控研究角色与有界 Loop

## 六个角色

| role | 允许职责 | 禁止事项 |
|---|---|---|
| `evidence` | 检索、题录核验、合法全文获取、来源登记 | 决定主要假设或因果结论 |
| `research-design` | 明确问题、估计对象、分析层级和替代方案 | 自行冻结协议 |
| `data-measurement` | 变量映射、计分、测量不变性和质量审计 | 把未知量表来源写成已核实 |
| `statistics` | 执行冻结规格并记录环境/输出 | 看结果后改变主模型 |
| `result-verification` | 独立检查收敛、拟合、异常估计、哈希和数字 | 代替研究者作理论决策 |
| `manuscript-submission` | 使用已验证结果与证据账本写作和构建投稿包 | 直接读取未核验模型输出 |

每次执行必须使用 `task-envelope.schema.json`，返回 `role-result.schema.json`。`dispatch-task` 校验角色—阶段、敏感输入和输入哈希；`resume-task` 记录每轮输出、错误类型、重试次数与停止原因；`verify-task` 再验输入输出哈希。

## 有界 Loop

- 仅 `tool-transient`、`network-transient`、`format-repair` 可重试；
- 默认最多 2 次，任务最大 5 次；
- `significance-driven` 永不重试；
- 资料缺失、伦理未核验、方法无效、敏感数据风险、人工决策和 gate 失败立即阻断；
- 读取主结果后发生的方法修改必须进入偏离记录，并按规则标为次要或探索性。

不得无限循环，也不得重试到出现显著结果。
