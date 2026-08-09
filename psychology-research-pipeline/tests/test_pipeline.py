from __future__ import annotations

import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))

from pipeline_schema import CSV_HEADERS, RUN_ROOT, SCHEMA_VERSION, STAGE_IDS, STAGES  # noqa: E402


class PipelineTests(unittest.TestCase):
    def run_script(self, name: str, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *args],
            text=True, encoding="utf-8", capture_output=True, check=check, env=environment,
        )

    def test_schema_is_single_twelve_stage_contract(self) -> None:
        self.assertEqual(12, len(STAGES))
        self.assertEqual(12, len(set(STAGE_IDS)))
        self.assertEqual("00_scope", STAGE_IDS[0])
        self.assertEqual("11_review", STAGE_IDS[-1])
        self.assertTrue(all("_" in stage["dir"] for stage in STAGES))
        self.assertNotIn("01_scope", {stage["dir"] for stage in STAGES})

    def test_machine_contracts_and_project_pack_are_versioned(self) -> None:
        expected = {
            "project-pack.schema.json", "data-decisions.schema.json", "analysis-spec.schema.json",
            "analysis-output.schema.json", "journal-policy.schema.json", "search-plan.schema.json",
            "evidence-record.schema.json", "evidence-coverage.schema.json",
            "presearch-protocol.schema.json", "zotero-target.schema.json",
            "task-envelope.schema.json", "role-result.schema.json", "tool-capability.schema.json",
            "loop-policy.schema.json", "evidence-ledger.schema.json",
        }
        schema_dir = SKILL / "schemas"
        self.assertEqual(expected, {path.name for path in schema_dir.glob("*.json")})
        for path in schema_dir.glob("*.json"):
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("https://json-schema.org/draft/2020-12/schema", payload["$schema"])
            self.assertTrue(payload["title"])
            Draft202012Validator.check_schema(payload)
        pack = json.loads((
            SKILL / "project-packs" / "interparental-conflict-depression-nssi" / "pack.json"
        ).read_text(encoding="utf-8"))
        self.assertEqual(1, pack["schema_version"])
        self.assertEqual("interparental-conflict-depression-nssi", pack["id"])
        pack_schema = json.loads((schema_dir / "project-pack.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator(pack_schema).validate(pack)
        pack_dir = SKILL / "project-packs" / "interparental-conflict-depression-nssi"
        for file_name, schema_name in [
            (pack["presearch_protocol"], "presearch-protocol.schema.json"),
            (pack["zotero_target"], "zotero-target.schema.json"),
            (pack["search_plan"], "search-plan.schema.json"),
            (pack["evidence_coverage"], "evidence-coverage.schema.json"),
        ]:
            instance = json.loads((pack_dir / file_name).read_text(encoding="utf-8"))
            schema = json.loads((schema_dir / schema_name).read_text(encoding="utf-8"))
            Draft202012Validator(schema).validate(instance)

    def test_init_creates_canonical_run_and_gate_advances(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            result = self.run_script(
                "init_research_run.py", "--project", str(project), "--title", "青少年纵向研究",
                "--mode", "standard", "--run-id", "test-run",
            )
            run_dir = Path(result.stdout.strip())
            self.assertEqual(project / RUN_ROOT / "test-run", run_dir)
            self.assertFalse((project / "research-pipeline").exists())
            state = json.loads((run_dir / "状态记录_state.json").read_text(encoding="utf-8"))
            self.assertEqual(SCHEMA_VERSION, state["schema_version"])
            self.assertEqual("standard", state["mode"])
            self.assertEqual("00_scope", state["current_stage"])
            self.assertTrue((run_dir / "日志" / "决策记录_decisions.md").is_file())

            failed = self.run_script(
                "pipeline_gate.py", "--run-dir", str(run_dir), "--stage", "00_scope", "--check", check=False,
            )
            self.assertEqual(1, failed.returncode)
            self.assertIn("placeholder remains", failed.stdout)

            scope = run_dir / "00_项目定标"
            common = (
                "本项目的主要研究问题聚焦三波纵向关联，主要估计对象为个体内变化。"
                "推论边界限定为时间顺序上的预测关联，不做未经识别的因果解释。"
                "样本、变量和测量工具均需在数据审计后冻结；未知事项进入阻断清单。"
                "研究对象、施测时间、学校聚类和量表计分依据均要从源材料逐项核验。"
                "主要分析、次要分析与探索性分析分开登记，任何计划外修改写入偏离记录。"
            )
            (scope / "项目定标简报_project_brief.md").write_text("# 项目定标\n\n" + common, encoding="utf-8")
            (scope / "研究问题与假设_research_questions_hypotheses.md").write_text("# 研究问题\n\n" + common, encoding="utf-8")
            csv_path = scope / "构念变量关系表_construct_variable_map.csv"
            headers = CSV_HEADERS[csv_path.name]
            with csv_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=headers)
                writer.writeheader()
                writer.writerow({header: "已核验" for header in headers})

            passed = self.run_script(
                "pipeline_gate.py", "--run-dir", str(run_dir), "--stage", "00_scope", "--advance",
            )
            self.assertIn("GATE PASSED", passed.stdout)
            state = json.loads((run_dir / "状态记录_state.json").read_text(encoding="utf-8"))
            self.assertEqual("01_protocol", state["current_stage"])


if __name__ == "__main__":
    unittest.main()
