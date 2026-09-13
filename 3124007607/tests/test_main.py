"""Integration and error-handling tests for the command-line interface."""

from pathlib import Path

from main import read_text, run, write_result


def test_run_writes_two_decimal_places(tmp_path: Path) -> None:
    original = tmp_path / "orig.txt"
    suspected = tmp_path / "copy.txt"
    answer = tmp_path / "answer.txt"
    original.write_text("今天是星期天，天气晴。", encoding="utf-8")
    suspected.write_text("今天是周天，天气晴朗。", encoding="utf-8")

    assert run([str(original), str(suspected), str(answer)]) == 0
    result = answer.read_text(encoding="utf-8")
    assert result.count(".") == 1
    assert len(result.split(".")[1]) == 2
    assert 0.0 <= float(result) <= 1.0


def test_run_rejects_wrong_argument_count(capsys) -> None:
    assert run([]) == 2
    assert "用法" in capsys.readouterr().err


def test_run_reports_missing_input(tmp_path: Path, capsys) -> None:
    answer = tmp_path / "answer.txt"
    arguments = [
        str(tmp_path / "missing.txt"),
        str(tmp_path / "also-missing.txt"),
        str(answer),
    ]
    assert run(arguments) == 1
    assert "无法读取文件" in capsys.readouterr().err
    assert not answer.exists()


def test_read_text_accepts_utf8_bom(tmp_path: Path) -> None:
    source = tmp_path / "bom.txt"
    source.write_bytes(b"\xef\xbb\xbf" + "中文".encode())
    assert read_text(source) == "中文"


def test_read_text_rejects_invalid_utf8(tmp_path: Path) -> None:
    source = tmp_path / "invalid.txt"
    source.write_bytes(b"\xff\xfe\x00")
    try:
        read_text(source)
    except ValueError as error:
        assert "UTF-8" in str(error)
    else:
        raise AssertionError("invalid UTF-8 should fail")


def test_write_result_reports_directory_target(tmp_path: Path) -> None:
    try:
        write_result(tmp_path, 0.5)
    except ValueError as error:
        assert "无法写入答案文件" in str(error)
    else:
        raise AssertionError("writing to a directory should fail")
