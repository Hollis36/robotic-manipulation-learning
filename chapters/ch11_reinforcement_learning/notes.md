# Chapter 11 Notes

## 本章核心问题

强化学习如何把操作任务表达成状态、动作、奖励和策略学习问题？这种表达适合哪些 manipulation 场景？

## 关键概念

- RL 需要明确环境接口：reset、step、observation、reward、done。
- policy-gradient、value-based 和 model-based 方法关注不同的信息结构。
- 操作任务中的接触和视觉状态让 RL 很有吸引力，也让样本效率和泛化更难。

## 公式与图示

```text
s_t, a_t, r_t, s_{t+1}
```

## 实现想法

- 写一个小网格世界：移动到物体旁边，执行 grasp，得到奖励。
- 不训练复杂模型，先验证环境接口和奖励设计。

## 未解决问题

- 奖励设计如何避免投机行为？
- model-based RL 在操作任务中如何利用已知物理模型？

