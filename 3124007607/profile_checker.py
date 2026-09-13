"""产生一个报告用来记录module"""

import cProfile
import pstats

from plagiarism_checker import calculate_similarity


def benchmark() -> None:
    """用两个中等大小的中文文档练习checker"""

    original = "今天是星期天，天气晴朗，我晚上要去看电影。" * 20_000
    suspected = "今天是周天，天气晴，我晚上准备去看一场电影。" * 20_000
    for _ in range(10):
        calculate_similarity(original, suspected)


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.runcall(benchmark)
    profiler.dump_stats("profile.prof")
    pstats.Stats(profiler).strip_dirs().sort_stats("cumulative").print_stats(15)
