"""Unit tests for the calculation module."""

import math

import pytest

from plagiarism_checker import _cosine_similarity, calculate_similarity, normalize_text


def test_normalize_removes_spaces_and_punctuation() -> None:
    assert normalize_text("今天，是 星期天！\n") == "今天是星期天"


def test_normalize_folds_english_case() -> None:
    assert normalize_text("Hello中文") == "hello中文"


def test_identical_text_is_one() -> None:
    assert calculate_similarity("今天天气晴朗", "今天天气晴朗") == 1.0


def test_formatting_changes_are_ignored() -> None:
    assert calculate_similarity("今天，天气晴。", "今 天 天气晴！") == 1.0


def test_completely_different_text_is_zero() -> None:
    assert calculate_similarity("甲乙丙丁", "春夏秋冬") == 0.0


def test_one_empty_text_is_zero() -> None:
    assert calculate_similarity("", "有内容") == 0.0


def test_two_empty_texts_are_identical() -> None:
    assert calculate_similarity(" ！？", "\n，。") == 1.0


def test_single_equal_character_is_one() -> None:
    assert calculate_similarity("甲", "甲") == 1.0


def test_single_different_character_is_zero() -> None:
    assert calculate_similarity("甲", "乙") == 0.0


def test_two_character_partial_change_is_zero() -> None:
    assert calculate_similarity("甲乙", "甲丙") == 0.0


def test_small_edit_has_intermediate_similarity() -> None:
    score = calculate_similarity("今天是星期天天气晴", "今天是周天天气晴朗")
    assert 0.3 < score < 1.0


def test_reordered_text_is_not_identical() -> None:
    score = calculate_similarity("甲乙丙丁戊己", "戊己甲乙丙丁")
    assert 0.0 < score < 1.0


def test_repeated_content_uses_term_frequency() -> None:
    score = calculate_similarity("哈哈哈哈天气好", "哈哈天气好")
    assert 0.5 < score < 1.0


def test_similarity_is_symmetric() -> None:
    left = "今天晚上我要去看电影"
    right = "我晚上要去影院看电影"
    assert calculate_similarity(left, right) == pytest.approx(calculate_similarity(right, left))


def test_cosine_handles_empty_vectors() -> None:
    assert _cosine_similarity({}, {"甲乙": 1}) == 0.0


def test_score_is_finite_and_bounded() -> None:
    score = calculate_similarity("论文" * 10_000, "论文" * 9_999 + "作业")
    assert math.isfinite(score)
    assert 0.0 <= score <= 1.0
