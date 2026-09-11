# 人话线性代数

> 用生活场景，重讲一遍 MIT 18.06。

把 Gilbert Strang 的线代课，从公式堆里捞出来，放回生活里。
每一期一个钩子、一个原理、一段教材原文。

**在线浏览**：`https://soneei.github.io/linear-algebra-daily/`

---

## 这是什么

中文互联网上的线性代数笔记很多，但大多数长这样：定义、定理、例题、习题。

这个项目的写法不太一样——每一期都从**一个日常现象**切入：

- 开空调的同时开微波炉，电流为什么自动分流？→ 关联矩阵与基尔霍夫定律
- 一张 Excel 里「两两配对」的表，凭什么被 Strang 称为世界最重要的矩阵？→ 对称矩阵与谱定理
- 你手机里的每一张照片，都被数学「精简」过一遍 → 基变换与图像压缩
- 你搜一个品牌名，官网为什么永远排第一 → 特征向量与 PageRank

然后才是原理、教材原文、以及 Strang 本人在书里说的那几句话。

## 内容结构

| | 期数 | 说明 |
|---|---|---|
| **课程日** Day 1–39 | 36 期 | 跟着 MIT 18.06 的进度走，一讲一期 |
| **番外篇** Vol.1–23 | 23 期 | 课程结束后继续写，挑那些「特别好玩」的点深挖 |

三个单元覆盖：向量与子空间 / 正交与行列式与特征值 / 对称矩阵与 SVD。

## 项目结构

```
linear-algebra-daily/
├── data/
│   └── episodes.json      # 唯一数据源：每一期的全部内容
├── templates/             # Jinja2 模板
│   ├── base.html
│   ├── index.html         # 首页（矩阵墙 + 列表）
│   └── episode.html       # 单期内页
├── assets/
│   └── style.css          # 样式
├── tools/
│   └── import_log.py      # 从学习日志导入期目元数据
├── build.py               # 静态站点生成器
└── docs/                  # 生成结果（GitHub Pages 根目录）
```

## 自己跑一遍

```bash
python3 build.py
# ✓ 生成 59 期 + 首页 → docs/

cd docs && python3 -m http.server 8090
# 打开 http://localhost:8090
```

改内容只需要编辑 `data/episodes.json`，然后重新 `python3 build.py`。

## 关于首页那面「矩阵墙」

首页上那 59 个格子，就是这 59 期本身：

- **方块** = 课程日，**圆点** = 番外篇
- 颜色由期号确定性生成，同一期永远是同一个颜色
- 淡色的格子 = 该期正文还在整理

它既是导航，也是一张进度图。

## 版权与来源

- **内容**（每期正文、站点代码）由本项目作者整理创作，采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 授权。
- **教材引用**：文中引用的英文原文出自 Gilbert Strang, *Introduction to Linear Algebra* (5th Edition, Wellesley-Cambridge Press)，仅作**学习与评论用途的短引用**，版权归原作者与出版方所有。本项目**不包含**该教材的任何电子版。
- **课程**：MIT 18.06 Linear Algebra，Gilbert Strang 主讲。原课程材料见 [MIT OpenCourseWare](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)（CC BY-NC-SA 4.0）。
- **致谢**：本项目在整理过程中参考了多个开源的 18.06 中文笔记项目，在此致谢所有开源作者。

本项目为个人学习笔记，与 MIT 及原作者无隶属关系。

## 生成方式说明

这些推送最初是作为「每日学习推送」逐日生成的：选定当天的课题 → 从教材定位原文 → 提炼一个生活钩子 → 写成一篇短笔记。本仓库是对这批内容的系统性整理与重建。

---

<p align="center"><sub>把约束定得越死，剩下的可能性越少，剩下那几种就越必然。</sub></p>
