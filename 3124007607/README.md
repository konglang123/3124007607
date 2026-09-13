# 第一次个人编程作业：论文查重

学号：3124007607

## 环境与安装

- Python 3.10 或更高版本
- 程序运行仅使用 Python 标准库，不连接网络
- `requirements.txt` 中的依赖仅用于测试、覆盖率和代码质量检查

```powershell
python -m pip install -r requirements.txt
```

## 运行

三个参数依次是原文、抄袭版和答案文件的绝对路径：

```powershell
python main.py C:\tests\orig.txt C:\tests\orig_add.txt C:\tests\ans.txt
```

答案文件只包含一个 `[0.00, 1.00]` 范围内、保留两位小数的浮点数。输入文件必须为 UTF-8 编码。

## 算法

1. 将文本转为统一大小写并移除标点、空白和下划线。
2. 分别统计字符二元组和三元组的词频。
3. 计算两个稀疏词频向量的余弦相似度。
4. 按 `0.6 × 二元组相似度 + 0.4 × 三元组相似度` 得到结果。

字符二元组能容忍局部增删改，三元组能更好地保留语序信息。核心计算时间复杂度为 `O(n + m)`，空间复杂度为 `O(n + m)`。

## 验证

```powershell
python -m pytest
python -m coverage run -m pytest
python -m coverage report -m
python -m coverage html
python -m ruff check .
python profile_checker.py
```

覆盖率网页入口为 `htmlcov/index.html`；性能报告文件为 `profile.prof`，可用 SnakeViz 等可视化工具打开，也可以直接引用命令行统计结果。
