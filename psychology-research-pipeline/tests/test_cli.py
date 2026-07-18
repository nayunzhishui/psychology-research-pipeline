from __future__ import annotations

import json
import os
import csv
from datetime import date
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
CLI = SKILL / "scripts" / "pipeline.py"


class PipelineCliTests(unittest.TestCase):
    def invoke(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "utf-8"
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [sys.executable, str(CLI), *args], text=True, encoding="utf-8",
            capture_output=True, check=check, env=environment,
        )

    def test_user_can_initialize_and_read_status_through_one_cli(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            created = self.invoke(
                "init", "--project", temp, "--title", "三波纵向研究",
                "--mode", "strict", "--run-id", "cli-run",
            )
            init_payload = json.loads(created.stdout)
            run_dir = Path(init_payload["run_dir"])
            self.assertEqual("active", init_payload["status"])
            self.assertEqual("00_scope", init_payload["current_stage"])
            self.assertTrue(run_dir.is_dir())

            status = self.invoke("status", "--run-dir", str(run_dir))
            status_payload = json.loads(status.stdout)
            self.assertEqual("cli-run", status_payload["run_id"])
            self.assertEqual("strict", status_payload["mode"])
            self.assertEqual(0, status_payload["completion_percent"])

            verification = self.invoke("verify-run", "--run-dir", str(run_dir), check=False)
            self.assertEqual(3, verification.returncode)
            verification_payload = json.loads(verification.stdout)
            self.assertEqual("blocked", verification_payload["status"])
            self.assertEqual("00_scope", verification_payload["stages"][0]["stage"])

            autopilot = self.invoke("autopilot", "--run-dir", str(run_dir), check=False)
            self.assertEqual(3, autopilot.returncode)
            self.assertEqual("00_scope", json.loads(autopilot.stdout)["blocked_stage"])

    def test_source_inventory_hashes_files_without_reading_sensitive_rows(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "inventory", "--run-id", "inventory-run",
            ).stdout)["run_dir"])
            sources = project / "资料"
            sources.mkdir()
            (sources / "data.csv").write_text("id,self_harm\np1,1\n", encoding="utf-8")
            (sources / "protocol.md").write_text("protocol", encoding="utf-8")
            result = json.loads(self.invoke(
                "inventory", "--run-dir", str(run_dir), "--source", str(sources),
            ).stdout)
            self.assertEqual("ready", result["status"])
            self.assertEqual(2, result["file_count"])
            inventory = json.loads(Path(result["inventory_json"]).read_text(encoding="utf-8"))
            data_item = next(item for item in inventory["files"] if item["name"] == "data.csv")
            self.assertEqual("participant-data", data_item["category"])
            self.assertNotIn("p1", json.dumps(inventory))

    def test_legacy_migration_only_copies_recognized_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            legacy = project / "legacy"
            (legacy / "01_scope").mkdir(parents=True)
            (legacy / "01_scope" / "project_brief.md").write_text("# Legacy\n\nverified content", encoding="utf-8")
            (legacy / "raw-data.sav").write_bytes(b"not-real-data")
            result = json.loads(self.invoke(
                "migrate", "--project", str(project), "--legacy-run", str(legacy),
                "--title", "migrated", "--run-id", "migrated-run",
            ).stdout)
            self.assertEqual("migrated-requires-gates", result["status"])
            run_dir = Path(result["run_dir"])
            migrated = run_dir / "00_项目定标" / "项目定标简报_project_brief.md"
            self.assertIn("verified content", migrated.read_text(encoding="utf-8"))
            self.assertFalse((run_dir / "raw-data.sav").exists())
            self.assertEqual("raw-data.sav", result["unmapped_metadata_only"][0]["path"])

    def test_user_can_audit_and_freeze_clean_panel_data(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            init_payload = json.loads(self.invoke(
                "init", "--project", str(project), "--title", "clean panel",
                "--mode", "strict", "--run-id", "data-run",
            ).stdout)
            run_dir = Path(init_payload["run_dir"])
            data = project / "panel.csv"
            with data.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["id1", "id2", "sex1", "sex2", "y1", "y2"])
                writer.writeheader()
                writer.writerows([
                    {"id1": "p1", "id2": "p1", "sex1": 1, "sex2": 1, "y1": 2, "y2": 3},
                    {"id1": "p2", "id2": "p2", "sex1": 2, "sex2": 2, "y1": 4, "y2": 5},
                ])
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "profile": "clean-test",
                "id_by_wave": {"T1": "id1", "T2": "id2"},
                "sex_by_wave": {"T1": "sex1", "T2": "sex2"},
                "allowed_sex_values": [1, 2],
                "measures": [
                    {"construct": "outcome", "wave": "T1", "variable": "y1", "expected_min": 0, "expected_max": 10},
                    {"construct": "outcome", "wave": "T2", "variable": "y2", "expected_min": 0, "expected_max": 10},
                ],
                "score_relations": [],
            }, ensure_ascii=False), encoding="utf-8")

            audit = json.loads(self.invoke(
                "audit-data", "--run-dir", str(run_dir), "--data", str(data), "--spec", str(spec),
            ).stdout)
            self.assertEqual([], audit["flags"])
            self.assertEqual(2, audit["shape"]["rows"])

            frozen = json.loads(self.invoke(
                "freeze-data", "--run-dir", str(run_dir), "--data", str(data), "--spec", str(spec),
            ).stdout)
            self.assertEqual("frozen", frozen["status"])
            self.assertTrue(Path(frozen["frozen_data"]).is_file())
            self.assertEqual(2, frozen["rows"])

    def test_flagged_data_requires_exact_auditable_decisions_before_freeze(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "decision gate",
                "--run-id", "decision-run",
            ).stdout)["run_dir"])
            data = project / "panel.csv"
            data.write_text("id1,id2,y1\np1,p1,99\n", encoding="utf-8")
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "profile": "decision-test", "id_by_wave": {"T1": "id1", "T2": "id2"},
                "sex_by_wave": {}, "measures": [{
                    "construct": "outcome", "wave": "T1", "variable": "y1",
                    "expected_min": 0, "expected_max": 10,
                }], "score_relations": [],
            }), encoding="utf-8")

            blocked = self.invoke(
                "freeze-data", "--run-dir", str(run_dir), "--data", str(data),
                "--spec", str(spec), check=False,
            )
            self.assertEqual(3, blocked.returncode)
            blocked_payload = json.loads(blocked.stdout)
            self.assertEqual("blocked", blocked_payload["status"])
            flag = blocked_payload["flags"][0]
            audit = run_dir / "06_数据管理" / "数据质量审计_data_audit.json"
            import hashlib
            decisions = project / "decisions.json"
            decisions.write_text(json.dumps({
                "schema_version": 1,
                "audit_sha256": hashlib.sha256(audit.read_bytes()).hexdigest(),
                "decisions": [{
                    "flag": flag, "status": "resolved", "resolution": "verified-valid",
                    "rationale": "源问卷显示该值为经核验的特殊有效编码。",
                    "evidence": "source-form-page-1", "approved_by": "researcher",
                    "decided_at": date.today().isoformat(),
                }],
            }, ensure_ascii=False), encoding="utf-8")
            frozen = json.loads(self.invoke(
                "freeze-data", "--run-dir", str(run_dir), "--data", str(data),
                "--spec", str(spec), "--decisions", str(decisions),
            ).stdout)
            self.assertEqual("frozen", frozen["status"])
            self.assertEqual(1, len(frozen["resolved_flags"]))
            self.assertTrue(Path(frozen["decision_log"]).is_file())

    def test_user_can_generate_auditable_longitudinal_analysis_code(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "RI-CLPM",
                "--mode", "strict", "--run-id", "analysis-run",
            ).stdout)["run_dir"])
            frozen = project / "frozen.csv"
            columns = [
                "conflict_t1", "conflict_t2", "conflict_t3",
                "depression_t1", "depression_t2", "depression_t3",
                "nssi_t1", "nssi_t2", "nssi_t3", "sex", "school",
            ]
            with frozen.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=columns)
                writer.writeheader()
                writer.writerow({name: 1 for name in columns})
            spec = project / "analysis-spec.json"
            spec.write_text(json.dumps({
                "profile": "three-construct-panel",
                "waves": ["T1", "T2", "T3"],
                "constructs": {
                    "conflict": {"variables": {"T1": "conflict_t1", "T2": "conflict_t2", "T3": "conflict_t3"}, "distribution": "continuous"},
                    "depression": {"variables": {"T1": "depression_t1", "T2": "depression_t2", "T3": "depression_t3"}, "distribution": "continuous"},
                    "nssi": {"variables": {"T1": "nssi_t1", "T2": "nssi_t2", "T3": "nssi_t3"}, "distribution": "zero-heavy"}
                },
                "group_variable": "sex",
                "cluster_variable": "school",
                "estimator": "MLR",
                "missing": "FIML"
            }, ensure_ascii=False), encoding="utf-8")

            generated = json.loads(self.invoke(
                "generate-analysis", "--run-dir", str(run_dir),
                "--data", str(frozen), "--spec", str(spec),
            ).stdout)
            self.assertEqual("ready", generated["status"])
            self.assertGreaterEqual(len(generated["code_files"]), 6)
            model_text = Path(generated["code_files"][2]).read_text(encoding="utf-8")
            self.assertIn("RI_conflict", model_text)
            self.assertIn("group.equal", Path(generated["code_files"][3]).read_text(encoding="utf-8"))
            self.assertIn("zero-heavy", Path(generated["code_files"][4]).read_text(encoding="utf-8"))

    def test_item_level_spec_generates_configural_metric_scalar_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "invariance",
                "--run-id", "invariance-run",
            ).stdout)["run_dir"])
            data = project / "frozen.csv"
            waves = ["T1", "T2", "T3"]
            columns = [f"x_{wave.lower()}" for wave in waves] + [f"y_{wave.lower()}" for wave in waves]
            columns += [f"{construct}{item}_{wave.lower()}" for construct in ["x", "y"] for item in [1, 2, 3] for wave in waves]
            with data.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=columns)
                writer.writeheader()
                writer.writerow({name: 1 for name in columns})
            spec = project / "spec.json"
            spec.write_text(json.dumps({
                "waves": waves, "measurement_mode": "item-level",
                "constructs": {
                    construct: {
                        "variables": {wave: f"{construct}_{wave.lower()}" for wave in waves},
                        "indicators": {wave: [f"{construct}{item}_{wave.lower()}" for item in [1, 2, 3]] for wave in waves},
                    } for construct in ["x", "y"]
                },
            }), encoding="utf-8")
            result = json.loads(self.invoke(
                "generate-analysis", "--run-dir", str(run_dir), "--data", str(data),
                "--spec", str(spec),
            ).stdout)
            measurement = Path(result["code_files"][1]).read_text(encoding="utf-8")
            self.assertIn("configural_model", measurement)
            self.assertIn("metric_model", measurement)
            self.assertIn("scalar_model", measurement)
            self.assertIn("delta_cfi", measurement)

    def test_verified_model_output_becomes_machine_readable_results(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "results",
                "--run-id", "results-run",
            ).stdout)["run_dir"])
            model_output = project / "model-output.json"
            model_output.write_text(json.dumps({
                "schema_version": 1, "analysis_id": "model-primary", "sample_n": 882,
                "primary_model": "RI-CLPM", "estimator": "MLR", "converged": True,
                "post_check": True, "fit": {"cfi": 0.96, "rmsea": 0.04, "srmr": 0.05},
                "parameters": [{
                    "result_id": "conflict_to_depression", "term": "T1 conflict -> T2 depression",
                    "role": "primary", "estimate": 0.12, "se": 0.04, "ci_low": 0.04,
                    "ci_high": 0.20, "p_value": 0.003, "standardized": 0.10,
                }], "deviations": [], "robustness": [{"name": "free-lag", "conclusion": "direction consistent"}],
            }), encoding="utf-8")
            verified = json.loads(self.invoke(
                "validate-results", "--run-dir", str(run_dir), "--input", str(model_output),
            ).stdout)
            self.assertEqual("verified", verified["status"])
            verified_results = json.loads(Path(verified["verified_results"]).read_text(encoding="utf-8"))
            self.assertEqual(882, verified_results["sample_n"])
            self.assertEqual(0.12, verified_results["conflict_to_depression.estimate"])
            self.assertTrue(Path(verified["analysis_manifest"]).is_file())

            invalid = project / "invalid-output.json"
            invalid.write_text(json.dumps({
                "schema_version": 1, "analysis_id": "bad", "sample_n": 10,
                "primary_model": "RI-CLPM", "estimator": "MLR", "converged": False,
                "post_check": False, "fit": {}, "parameters": [], "deviations": [],
            }), encoding="utf-8")
            blocked = self.invoke(
                "validate-results", "--run-dir", str(run_dir), "--input", str(invalid), check=False,
            )
            self.assertEqual(3, blocked.returncode)
            self.assertEqual("blocked", json.loads(blocked.stdout)["status"])

    def test_user_can_deduplicate_evidence_with_stable_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "evidence",
                "--run-id", "evidence-run",
            ).stdout)["run_dir"])
            candidates = project / "candidates.csv"
            fields = ["candidate_id", "title", "authors", "year", "doi", "database"]
            with candidates.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows([
                    {"candidate_id": "c1", "title": "A Longitudinal Study", "authors": "Li, A", "year": "2020", "doi": "https://doi.org/10.1000/ABC", "database": "PsycINFO"},
                    {"candidate_id": "c2", "title": "A longitudinal study", "authors": "Li, A", "year": "2020", "doi": "10.1000/abc", "database": "WoS"},
                    {"candidate_id": "c3", "title": "Another Study", "authors": "Wang, B", "year": "2021", "doi": "", "database": "CNKI"},
                ])
            result = json.loads(self.invoke(
                "dedupe-evidence", "--run-dir", str(run_dir), "--input", str(candidates),
            ).stdout)
            self.assertEqual(2, result["unique_records"])
            self.assertEqual(1, result["duplicate_records"])
            with Path(result["deduplicated_file"]).open(encoding="utf-8-sig") as handle:
                deduped = list(csv.DictReader(handle))
            self.assertEqual("10.1000/abc", deduped[0]["doi"])
            self.assertEqual({"study-0001", "study-0002"}, {row["study_id"] for row in deduped})

    def test_user_can_render_only_verified_results_and_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            run_dir = Path(json.loads(self.invoke(
                "init", "--project", str(project), "--title", "manuscript",
                "--run-id", "write-run",
            ).stdout)["run_dir"])
            template = project / "template.md"
            template.write_text(
                "# 论文\n\n## 结果\n\n最终样本量为 {{result.sample_n}}。\n\n"
                "## 讨论\n\n{{claim.claim-0001}}\n",
                encoding="utf-8",
            )
            results = project / "results.json"
            results.write_text(json.dumps({"sample_n": 100}), encoding="utf-8")
            claims = project / "claims.csv"
            claim_fields = ["claim_id", "claim_text", "source_type", "source_ids", "evidence_location", "verification_status"]
            with claims.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=claim_fields)
                writer.writeheader()
                writer.writerow({
                    "claim_id": "claim-0001", "claim_text": "该结果属于纵向预测关联，不构成因果证据。",
                    "source_type": "analysis", "source_ids": "model-primary", "evidence_location": "ri_clpm_parameters.csv",
                    "verification_status": "verified",
                })
            references = project / "references.bib"
            references.write_text("@article{seed2020, title={Seed}}\n", encoding="utf-8")

            rendered = json.loads(self.invoke(
                "render-manuscript", "--run-dir", str(run_dir), "--template", str(template),
                "--results", str(results), "--claims", str(claims), "--references", str(references),
            ).stdout)
            manuscript = Path(rendered["manuscript"]).read_text(encoding="utf-8")
            self.assertEqual("ready", rendered["status"])
            self.assertIn("最终样本量为 100", manuscript)
            self.assertIn("不构成因果证据", manuscript)
            self.assertNotIn("{{", manuscript)
            self.assertTrue(Path(rendered["numeric_audit"]).is_file())

            policy = project / "journal-policy.json"
            policy.write_text(json.dumps({
                "journal": "Test Journal of Psychology", "article_type": "Original Article",
                "checked_at": date.today().isoformat(), "scope_fit": "longitudinal developmental psychology",
                "word_limit": 8000, "ai_policy": "disclose language and coding assistance",
                "data_policy": "restricted adolescent data allowed with a justified statement",
                "submission_url": "https://example.org/submit",
                "source_urls": ["https://example.org/authors"]
            }), encoding="utf-8")
            package = json.loads(self.invoke(
                "build-submission", "--run-dir", str(run_dir), "--journal-policy", str(policy),
                "--manuscript", rendered["manuscript"], "--numeric-audit", rendered["numeric_audit"],
                "--claim-audit", rendered["claim_audit"],
            ).stdout)
            self.assertEqual("ready", package["status"])
            self.assertTrue(Path(package["package_dir"]).is_dir())
            self.assertNotIn(".sav", " ".join(package["files"]).lower())
            self.assertTrue(Path(package["simulated_reviews"]).is_file())


if __name__ == "__main__":
    unittest.main()
