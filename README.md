# 程序化道路：图、曲线与路口

生成的城市道路在路口错位、曲线抖动：点到线段距离没有夹紧，线段求交漏掉端点，Catmull-Rom 曲线没有按张力采样，路宽按车道数算错，图度数没去重，网格吸附四舍五入错，采样数按长度算错，退界深度重复计算，转角角度方向反，批量瓦片只提交一半。

## 目录结构

```
README.md
conftest.py
.gitignore
world/__init__.py
world/roads.py
tests/test_roads.py
```

## 当前状态

`world/roads.py` 中所有函数只保留签名与文档字符串，函数体统一
`raise NotImplementedError`。`tests/test_roads.py` 有 15 个参数化用例，
初始全部失败。

## 需要修复的 10 个问题

1. 点到线段距离夹紧端点
2. 线段求交含端点
3. Catmull-Rom 曲线采样
4. 路宽按车道与车道宽计算
5. 图度数去重
6. 网格吸附
7. 采样数按长度与步长
8. 退界深度计算
9. 转角角度方向
10. 批量瓦片统一提交

## 验收

```bash
python -m pytest -q
```

初始应得到 `15 failed`，且没有 collection error。实现 `world/roads.py`
后 15 条用例应全部通过。
