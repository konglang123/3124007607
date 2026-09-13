# 查重样例说明

本目录包含 10 组基础查重样例：根目录中的 `orig.txt`、`orig_add.txt`
和 `ans.txt` 是第 1 组；`case02` 至 `case10` 是另外 9 组。每个案例中：

- `orig.txt`：论文原文；
- `copy.txt`：待查重文本；
- `answer.txt`：运行 `main.py` 后生成的重复率。

| 案例 | 测试内容 |
|---|---|
| 根目录基础样例 | 局部词语替换 |
| case02_punctuation | 仅标点不同 |
| case03_replacement | 局部词语替换 |
| case04_addition | 增加内容 |
| case05_deletion | 删除内容 |
| case06_reordered | 调整语序 |
| case07_different | 完全不同主题 |
| case08_english_case | 英文字母大小写及标点变化 |
| case09_short | 短文本局部修改 |
| case10_repeated | 重复句式改写 |

`answer.txt` 是当前算法的实际输出，用于演示程序运行结果，不代表人工标注的标准答案。
