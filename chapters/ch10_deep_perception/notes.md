# Chapter 10 Notes

## 本章核心问题

对于操作任务，除了检测和分割之外，机器人还需要哪些更贴近动作决策的感知表示？

## 关键概念

- pose estimation、grasp selection、dense descriptor 和 task-level state 都可能成为感知目标。
- 预训练和微调可以降低特定操作任务的数据成本。
- 端到端 visuomotor policy 是另一条路线，但需要更谨慎地评估数据和泛化。

## 公式与图示

- 记录 perception target -> action module 的映射表。

## 实现想法

- 在 Chapter 9 的 pipeline 上增加 task-state 输出字段。
- 对每种感知任务写出输入、输出和下游使用方式。

## 未解决问题

- dense descriptor 在真实操作中如何标注和验证？
- 学习式抓取选择如何和几何约束结合？

