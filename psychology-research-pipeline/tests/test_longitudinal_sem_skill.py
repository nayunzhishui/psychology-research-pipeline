from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
SUBSKILL = SKILL / "subskills" / "empirical-longitudinal-sem"
SCRIPTS = SUBSKILL / "scripts"


class LongitudinalSemSkillTests(unittest.TestCase):
    def invoke(self, name: str, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args], capture_output=True,
            text=True, encoding="utf-8", check=check,
        )

    def test_plan_contains_complete_ordered_model_ladder_and_package_tiers(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = root / "spec.json"
            output = root / "plan.json"
            spec.write_text(json.dumps({
                "schema_version": 1, "analysis_id": "riclpm-primary", "waves": ["T1", "T2", "T3"],
                "constructs": ["conflict", "depression", "self_harm"], "group_variable": "sex",
                "cluster_variable": "school", "missing_strategy": "FIML-with-MI-sensitivity",
            }), encoding="utf-8")
            result = json.loads(self.invoke(
                "generate_analysis_plan.py", "--spec", str(spec), "--output", str(output),
            ).stdout)
            plan = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("draft-human-approval-required", result["status"])
            self.assertEqual(14, len(plan["model_ladder"]))
            self.assertEqual("data-and-scoring-freeze", plan["model_ladder"][0]["step_id"])
            self.assertEqual("independent-result-verification", plan["model_ladder"][-1]["step_id"])
            self.assertIn("powRICLPM", plan["packages"]["core"])
            self.assertIn("OpenMx", plan["packages"]["conditional"])
            self.assertIn("metaSEM", plan["packages"]["reserve"])

    def test_validator_fails_closed_when_measurement_gate_is_removed(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            spec = root / "spec.json"
            plan_path = root / "plan.json"
            spec.write_text(json.dumps({
                "schema_version": 1, "analysis_id": "riclpm-primary", "waves": ["T1", "T2", "T3"],
                "constructs": ["x", "y"], "missing_strategy": "FIML",
            }), encoding="utf-8")
            self.invoke("generate_analysis_plan.py", "--spec", str(spec), "--output", str(plan_path))
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            plan["model_ladder"] = [
                step for step in plan["model_ladder"] if step["step_id"] != "longitudinal-measurement-invariance"
            ]
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            result = self.invoke("validate_model_ladder.py", "--plan", str(plan_path), check=False)
            self.assertEqual(3, result.returncode)
            self.assertIn("longitudinal-measurement-invariance", result.stdout)


if __name__ == "__main__":
    unittest.main()
