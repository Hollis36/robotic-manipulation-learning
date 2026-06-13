# Math Notes

## SE(2) Transform

A 2D rigid transform combines a rotation matrix `R` and translation vector `p`:

```text
T = [R p]
    [0 1]
```

Composition applies the inner transform first:

```text
T_AC = T_AB T_BC
```

## Planar Forward Kinematics

For a serial planar arm, link `i` contributes an angle equal to the cumulative joint angle up to `i`. The end-effector position is the sum of link vectors:

```text
x = sum_i l_i cos(q_1 + ... + q_i)
y = sum_i l_i sin(q_1 + ... + q_i)
```

## Damped Least-Squares IK

For task error `e` and Jacobian `J`, a stable local update is:

```text
dq = J^T (J J^T + lambda^2 I)^-1 e
```

The damping term reduces unstable updates near singular configurations.

