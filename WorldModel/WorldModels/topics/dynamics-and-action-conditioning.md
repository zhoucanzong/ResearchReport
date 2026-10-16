# 横切专题：环境动力学与动作条件化

> **定位**：把「世界模型的动力学到底学在哪、动作怎么进去」做成一张可判定的对照——这是本专题三条架构主线（action 条件化视频/3D 生成、潜空间预测模型、world foundation model 平台化）的机制分水岭。
> **主等级**：`[精读原文]`（结论均可在 `../papers/` 各篇找到正文级证据）。

---

## 0. 本章结论

1. **「动作条件化发生在哪一层」是第一条分水岭**：潜变量转移层（World Models / PlaNet / Dreamer 系）vs 像素/生成去噪层（GameNGen / Sora 式）vs 隐状态动力学但只出规划量（MuZero）vs 完全不条件化（V-JEPA）。`[精读原文]`
2. **「动力学该预测什么」是第二条分水岭**：重构观测（PlaNet，只作训练信号）→ 不重构只预测规划量（MuZero）→ 不重构只预测表征（V-JEPA）→ 像素即状态（GameNGen）。`[精读原文]`
3. **「治漂移/治误差」的手段因层而异**：潜空间用 free bits / 回报归一化（DreamerV3），像素扩散用噪声增强（GameNGen），实时用 few-step 蒸馏 / shortcut forcing（CausVid / Dreamer 4）。`[精读原文]`
4. **判据 (a)(b)(c) 管「算不算世界模型」，不管「怎么实现」**：同一判据下可有完全不同的机制。`[精读原文]`

---

## 1. 四根可判定的轴

把「环境动力学与动作条件化」拆成四根独立的轴，每根都能用正文级证据区分：

| 轴 | 取值 | 代表 | 证据 |
| :-- | :-- | :-- | :-- |
| **动作注入的层** | 潜变量转移层 | World Models / PlaNet / Dreamer 系 | [papers/1912.01603-dreamer.md](../papers/1912.01603-dreamer.md) |
| | 像素/扩散去噪层 | GameNGen / Hunyuan-GameCraft / Matrix-Game | [papers/2408.14837-gamengen.md](../papers/2408.14837-gamengen.md) |
| | 隐状态动力学（出规划量） | MuZero | [papers/1911.08265-muzero.md](../papers/1911.08265-muzero.md) |
| | 不条件化 | V-JEPA | [papers/2404.08471-vjepa.md](../papers/2404.08471-vjepa.md) |
| **预测目标** | 重构观测（训练信号） | PlaNet | [papers/1811.04551-planet.md](../papers/1811.04551-planet.md) |
| | 不重构，预测 reward/policy/value | MuZero | 同上 |
| | 不重构，预测表征 | V-JEPA | 同上 |
| | 像素即状态 | GameNGen | 同上 |
| **行为派生** | 在线规划（CEM/MPC） | PlaNet | 同上 |
| | 树搜索（MCTS） | MuZero | 同上 |
| | 想象里学策略（解析梯度） | Dreamer / DreamerV3 / Dreamer 4 | [papers/1912.01603-dreamer.md](../papers/1912.01603-dreamer.md) |
| | 进化控制器（免梯度） | World Models | [papers/1803.10122-world-models.md](../papers/1803.10122-world-models.md) |
| **治漂移/治误差** | free bits / 回报归一化 | DreamerV3 | [papers/2301.04104-dreamerv3.md](../papers/2301.04104-dreamerv3.md) |
| | 噪声增强 | GameNGen | 同上 |
| | 温度 τ | World Models | 同上 |
| | few-step 蒸馏 / shortcut forcing | CausVid / Self-Forcing / Dreamer 4 | 见主报告章 4 |

---

## 2. 两个端点：像素级 vs 潜变量级

**像素级动作条件化**（GameNGen）：动作流注入扩散去噪过程，逐帧生成像素。优点是**可读、可交互**（人能玩）；代价是误差以像素级累积、需噪声增强压制、单域。

**潜变量级动作条件化**（PlaNet/Dreamer）：动作进 RSSM 的确定性路径 `f(h_{t-1}, s_{t-1}, a_{t-1})`，动力学在潜空间演化。优点是**紧凑、规划快**；代价是 rollout 不可读、表征瓶颈。

**判据归属**：两者都满足 (a)(b)(c) → 都入本专题；但「机制不同」意味着它们的**失效模式不同**（像素级怕漂移、潜变量级怕表征瓶颈），评测也不能混用（见 [incomparability-checklist.md](incomparability-checklist.md)）。

---

## 3. 「预测什么」的光谱

```
重构观测 ←————————————————————→ 不重构
PlaNet        V-JEPA         MuZero
(重构作训练信号)  (预测表征)   (预测 reward/policy/value)
```

- **PlaNet**：重构观测，但观测模型只作训练信号、不用于规划——「重构是脚手架」；
- **V-JEPA**：预测表征空间中被遮挡区域——连重构都不做，只管表征；
- **MuZero**：完全不重构，只预测规划直接需要的三个量。

这条光谱说明：「世界模型该预测什么」没有共识——**预测目标越偏离观测，越不像「可交互环境」，越像「规划引擎」**。

---

## 4. 治漂移 / 治误差工具箱

| 失效 | 机制 | 代表 | 层 |
| :-- | :-- | :-- | :-- |
| 模型被策略钻空子 | 温度 τ（把模型做成随机的） | World Models | 潜变量 |
| 长程预测误差累积 | latent overshooting | PlaNet | 潜变量 |
| 动力学退化解 | free bits | DreamerV3 | 潜变量 |
| 自回归漂移发散 | 噪声增强 | GameNGen | 像素 |
| 跨域数值不稳 | 回报归一化 / twohot / symlog | DreamerV3 | 潜变量 |
| 实时性 | few-step 蒸馏 / shortcut forcing | CausVid / Self-Forcing / Dreamer 4 | 像素/潜变量 |

---

## 5. 对条目结论的影响

- 本专题「架构谱系」的三条主线，其实是**「动作注入层 × 预测目标 × 行为派生」三根轴的组合**——本章给出可判定的坐标系；
- **判据 (a)(b)(c) 与机制解耦**：同一判据下可有完全不同的实现，这正是「世界模型」一词歧义的根源；
- **失效模式随层而变**，因此「评测」也必须分层——见 [incomparability-checklist.md](incomparability-checklist.md)。

---

## 来源

- 全部结论可在 `../papers/` 各篇找到正文级证据（arXiv:1803.10122 / 1811.04551 / 1911.08265 / 1912.01603 / 2301.04104 / 2310.06114 / 2404.08471 / 2408.14837）。
