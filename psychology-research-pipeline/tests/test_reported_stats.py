"""验算统计量脚本的回归测试：分布函数对照 scipy 算好的参考值，判定对照阅读中遇到过的几类不一致。"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import check_reported_stats as crs  # noqa: E402


def test_distributions_match_reference_values() -> None:
    # 参考值由 scipy.stats 算出：2*t.sf(2, 10)、chi2.sf(3.96, 1)、f.sf(2.5, 3, 40)、fisher_exact、norm.ppf(.975)
    assert abs(crs.p_t(2.0, 10) - 0.07338803477074039) < 1e-10
    assert abs(crs.p_chi2(3.96, 1) - 0.046593703371131986) < 1e-10
    assert abs(crs.p_f(2.5, 3, 40) - 0.07325435201794982) < 1e-10
    assert abs(crs.fisher_two_sided(7, 9, 2, 18) - 0.049137017533274804) < 1e-10
    assert abs(crs.z_crit(0.95) - 1.959963984540054) < 1e-9


def test_coefficient_with_shifted_decimal_is_flagged() -> None:
    out = crs.main(["系数", "--估计", "-.26", "--标准误", ".47", "--自由度", "83", "--报告t", "-5.5", "--报告p", "<.001"])
    assert "报告的 t = -5.5：不相符（相差约 10 倍" in out
    assert "报告的 p < .001：不相符" in out


def test_interval_settles_a_missing_zero_in_p() -> None:
    bad = crs.main(["区间", "--估计", "2.21", "--下限", "1.0", "--上限", "4.7", "--比值", "--报告p", ".42"])
    good = crs.main(["区间", "--估计", "2.21", "--下限", "1.0", "--上限", "4.7", "--比值", "--报告p", ".042"])
    assert "不相符" in bad and "10 倍" in bad
    assert "报告的 p = .042：相符" in good


def test_chi_square_p_and_rounding() -> None:
    assert "报告的 p < .001：不相符" in crs.main(["卡方", "--值", "3.96", "--自由度", "1", "--报告p", "<.001"])
    assert "报告的 p = .047：相符" in crs.main(["卡方", "--值", "3.96", "--自由度", "1", "--报告p", ".047"])


def test_two_by_two_tells_which_chi_square_was_reported() -> None:
    out = crs.main(["四格", "7", "9", "2", "18", "--报告卡方", "3.75"])
    assert "不校正 χ²(1) = 5.40" in out
    assert "与连续性校正的卡方相符" in out


def test_two_groups_and_percentages() -> None:
    out = crs.main(["两组", "--均值", "3.88", "4.75", "--标准差", "1.10", "0.92", "--人数", "20", "25", "--报告t", "2.90"])
    assert "合并方差 t(43) = -2.89" in out and "：相符" in out
    assert "没有哪个整数分子" in crs.main(["比例", "--分子", "25", "--分母", "40", "--报告", "62.0"])
    assert "报告的 62.5%：相符" in crs.main(["比例", "--分子", "25", "--分母", "40", "--报告", "62.5"])


def test_command_line_prints_utf8() -> None:
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run([sys.executable, str(SCRIPTS / "check_reported_stats.py"), "相关", "--r", ".32", "--人数", "115"],
                            capture_output=True, text=True, encoding="utf-8", env=env)
    assert result.returncode == 0
    assert "t(113) = 3.59" in result.stdout
