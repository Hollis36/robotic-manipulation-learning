# 00 Manipulation Stack

机器人操作的核心不是某一个算法，而是一个闭环系统：

```text
task goal
  -> robot body and sensors
  -> state estimation
  -> geometry and kinematics
  -> grasp or contact choice
  -> motion planning
  -> control execution
  -> feedback and recovery
```

## Learning Objectives

- Describe manipulation as a closed-loop stack rather than a single grasping algorithm.
- Decompose a task into perception, geometry, grasping, planning, control, and recovery.
- Identify which layer is most likely to fail for a concrete task.

## Checkpoint

- You can map a pick-and-place task onto every layer of the stack.
- You can explain why a correct IK solution is not enough to guarantee task success.
- You can name one feedback signal that helps the robot recover from failure.

## Practice Task

Pick one everyday manipulation task and write a six-step stack for it. For each step, mark whether you would solve it with geometry, control, learning, or a hybrid method.

一个 pick-and-place 任务至少要回答：

- 目标物体在哪里？
- 夹爪应该从哪里接近？
- 机械臂能不能到达这个姿态？
- 路径会不会碰撞？
- 真实控制能不能稳定执行？
- 抓取失败后如何恢复？

## Mental Model

Manipulation 是把 perception、geometry、planning、control、contact 和 learning 连接起来，让机器人可靠改变物体状态。

## Exercise

选择一个日常任务，例如拿杯子、开抽屉、插 peg、叠衣服。把它拆成上面的 stack，并指出最难的一层。
