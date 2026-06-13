# Chapter 9 Notes

## 本章核心问题

在复杂场景中，深度学习的检测和分割如何帮助机器人找到要操作的对象？

## 关键概念

- 检测回答“物体在哪里”，分割回答“哪些像素或点属于物体”。
- 深度模型可以给几何算法提供更好的初始化或过滤。
- 数据集质量直接决定 perception pipeline 的可靠性。

## 公式与图示

- 记录数据流：RGB-D -> detection -> mask -> segmented point cloud -> pose/grasp planner。

## 实现想法

- 用小数组模拟 mask，把点云过滤成目标点云。
- 先实现接口和数据流，不引入训练框架。

## 未解决问题

- manipulation 场景需要怎样的数据标注？
- 分割错误如何传递到抓取失败？

