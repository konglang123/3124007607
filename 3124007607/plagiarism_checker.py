"""核心算法评价论文相似度"""

from __future__ import annotations

import math
import re
from collections import Counter

_IGNORED_CHARACTERS = re.compile(r"[\W_]+", flags=re.UNICODE)


def normalize_text(text: str) -> str:
    """通过删除标点和空白返回可比较的文本。 """

    return _IGNORED_CHARACTERS.sub("", text.casefold())


def _character_ngrams(text: str, size: int) -> Counter[str]:
    """计算文本中size的所有字符n-grams"""

    if len(text) < size:
        return Counter()

    # 使用内置的 zip 和 join 构造滑动窗口，减少 Python 层循环调用。
    shifted_texts = (text, *(text[offset:] for offset in range(1, size)))
    return Counter(map("".join, zip(*shifted_texts, strict=False)))


def _cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    """计算向量值"""

    if not left or not right:
        return 0.0

    # 迭代较小的映射以减少字典查找。
    smaller, larger = (left, right) if len(left) <= len(right) else (right, left)
    dot_product = sum(count * larger.get(term, 0) for term, count in smaller.items())
    left_norm = math.sqrt(sum(count * count for count in left.values()))
    right_norm = math.sqrt(sum(count * count for count in right.values()))
    return dot_product / (left_norm * right_norm)


def calculate_similarity(original: str, suspected: str) -> float:
    """返回封闭区间[0.0,1,0]内的相似度得分。"""

    normalized_original = normalize_text(original)
    normalized_suspected = normalize_text(suspected)

    if not normalized_original and not normalized_suspected:
        return 1.0
    if not normalized_original or not normalized_suspected:
        return 0.0
    if normalized_original == normalized_suspected:
        return 1.0

    # 一个字符的文档不能形成一个n-gram.
    if min(len(normalized_original), len(normalized_suspected)) < 2:
        return 0.0

    bigram_score = _cosine_similarity(
        _character_ngrams(normalized_original, 2),
        _character_ngrams(normalized_suspected, 2),
    )

    # 两字符文本没有三元组；没有公共二元组时也不可能存在公共三元组。
    if min(len(normalized_original), len(normalized_suspected)) < 3:
        return bigram_score
    if bigram_score == 0.0:
        return 0.0

    trigram_score = _cosine_similarity(
        _character_ngrams(normalized_original, 3),
        _character_ngrams(normalized_suspected, 3),
    )

    return max(0.0, min(1.0, 0.6 * bigram_score + 0.4 * trigram_score))
