---
id: 2
kind: iter
date: 2026-06-29T03:29:27Z
parent-round: 1
skill-commit: 2ab29ad44dec
criteria-version: 0
user-confirmation: accepted
---


## Hypothesis

把 okf-memex SKILL.md 摄入工作流第 8 步从"运行 `gen_index.py` 或手动更新"改成明确指导"优先 `gen_index.py` 自动生成；手动则整体重写而非逐条插入"，预期减少多条目新增时的反复编辑和出错；若实际摄入中 `gen_index.py` 脚本不可用且整体重写反而比逐条插入更易出错，则该假设被证伪。

## Outcome

用户接受。改进基于实际摄入 2 篇文章、新增 24 个 wiki 页面时的真实经验：逐条 `replace_in_file` 插入 index.md 触发了 7 次编辑和系统反复修改警告，而整体重写或脚本生成是更可靠的做法。

## Reflection

当需要对同一文件做多处结构性插入时，整体重写比逐条替换更可靠；摄入工作流的高频操作应优先使用自动化脚本而非手动编辑。
